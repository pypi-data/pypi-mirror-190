r"""TaskInterface class corresponding to the program DL_MONTE"""


import logging
import os
import shutil

import dlmontepython.simtask.task as task

import dlmontepython.htk.sources.dlmonte as dlmonte
import dlmontepython.htk.sources.dlconfig as dlconfig
import dlmontepython.htk.sources.dlmove as dlmove
import dlmontepython.htk.sources.dlfedmethod as dlfedmethod




logger = logging.getLogger(__name__)




class DLMonteInterface(task.TaskInterface):

    r"""TaskInterface class corresponding to the program DL_MONTE

    TaskInterface class corresponding to the program DL_MONTE. This
    uses Kevin Stratford's DL_MONTE Python toolkit to do the heavy 
    lifting.

    See the `extract_data` function for the list of data types which
    this supports to read from DL_MONTE output files, and for the
    expected form for the `Observable` objects which correspond to these
    data types. Similarly, see the `amend_input_parameter` function for
    a list of input parameters which this interface supports to change
    in DL_MONTE input files.

    Examples demonstrating usage of this class can be found in the
    function-level documentation below.

    Attributes
    ----------
    runner : htk.sources.dlmonte.DLMonteRunner
        htk.sources.dlmonte.DLMonteRunner object used to execute 
        DL_MONTE simulations. In the constructor for this class the
        path of the executable is used to initialise `runner`

    """

    def __init__(self, executable):

        r"""Constructor 

        Constructor which links to the DL_MONTE executable in the
        specified location.

        Parameters
        ----------
        executable : str
            The path to the DL_MONTE executable

        Examples
        --------
        Create an interface instance which is linked to an executable
        called 'DLMONTE-SRL.X' (which can be found by the system due to
        appropriate set up of the environment, e.g. in unix systems
        including the directory containing the executable in the PATH 
        environmental variable).

        >>> dlmlinker = dlmonteinterface.DLMonteInterface('DLMONTE-SRL.X')    

        """

        self.runner = dlmonte.DLMonteRunner(executable)




    def copy_input_files(self, fromdir, todir):

        r"""Copy simulation input files between directories

        Copy simulation input files between directories

        Parameters
        ----------
        fromdir : str
            The directory containing the input files
        todir : str
            The target directory for the input files

        Examples
        --------
        Create an interface instance which is linked to an executable
        called 'DLMONTE-SRL.X' (which can be found by the system due to
        appropriate set up of the environment, e.g. in unix systems
        including the directory containing the executable in the PATH 
        environmental variable), and copy input files from a directory
        `dir1` to `dir2`

        >>> dlmlinker = dlmonteinterface.DLMonteInterface('DLMONTE-SRL.X')
        >>> dlmlinker.copy_input_files(dir1,dir2)
       
        """

        siminput = dlmonte.DLMonteInput.from_directory(fromdir)
        siminput.to_directory(todir)




    def run_sim(self, simdir):

        r"""Run a simulation

        Run a simulation in a specified directory

        Parameters
        ----------
        simdir : str
            The directory in which the simulation is to be executed

        Examples
        --------
        Create an interface instance which is linked to an executable
        called 'DLMONTE-SRL.X' (which can be found by the system due to
        appropriate set up of the environment, e.g. in unix systems
        including the directory containing the executable in the PATH 
        environmental variable), and initiate a DL_MONTE simulation in the
        directory `dir1` using the input files therein.

        >>> dlmlinker = dlmonteinterface.DLMonteInterface('DLMONTE-SRL.X')
        >>> dlmlinker.run_sim(dir1)
       
        """

        self.runner.directory = simdir
        self.runner.execute()


    
    def resume_sim(self, oldsimdir, simdir):

        r"""Resume a simulation from a checkpointed state

        Resume a simulation whose checkpointed state is located in the
        directory `oldsimdir`, and run the resumed/new simulation in
        the directory `simdir`

        Parameters
        ----------
        oldsimdir : str
            The directory in which the files from the 'old' simulation
            to be resumed reside
        simdir : str
            The directory in which the new/resumed simulation is to be
            executed

        Examples
        --------
        Create an interface instance which is linked to an executable
        called 'DLMONTE-SRL.X' (which can be found by the system due to
        appropriate set up of the environment, e.g. in unix systems
        including the directory containing the executable in the PATH 
        environmental variable), and initialise a new simulation in a 
        directory `dir2` based on the input and output files from
        a previous simulation located in a directory `dir1`

        >>> dlmlinker = dlmonteinterface.DLMonteInterface('DLMONTE-SRL.X')
        >>> dlmlinker.resume_sim(dir1,dir2)

        """

        siminput = dlmonte.DLMonteInput.from_directory(oldsimdir)
        siminput.config=dlconfig.from_file(os.path.join(oldsimdir,"REVCON.000"))

        # If FED is in use...
        if not siminput.control.use_block.fed_block is None:
            
            # Copy the latest FEDDAT.000_??? file to the file FEDDAT.000 file in the new simulation directoy
            # to use as input
            with open(os.path.join(simdir,"FEDDAT.000"),"w") as feddatinput:
                feddatinput.write(dlmonte.DLMonteOutput.load(oldsimdir).feddat.str_iteration())

            # Set the appropriate flag on the 'fed order' line to '-1' to signify that we are reading 
            # the bias function from FEDDAT.000
            siminput.control.use_block.fed_block.orderparam.npow = -1

        # If transition matrix FED method in use
        if isinstance(siminput.control.use_block.fed_block.method, dlfedmethod.TransitionMatrix):
            # Modify the input in CONTROL so that it corresponds to a resumed simulation
            siminput.control.use_block.fed_block.method.mode="resume"
            # A bit hacky... 
            # For the FED output file TMATRX.000 copy it to the new directory and rename them it so
            # it becomes an imput file for the next simulation
            shutil.copyfile(os.path.join(oldsimdir,"TMATRX.000"),os.path.join(simdir,"TMATRX"))

        # Output the modified input files (CONTROL,CONFIG,FIELD) to the new simulation directoy
        siminput.to_directory(simdir) 

        self.run_sim(simdir)




    def extract_data(self, observable, simdir):

        r"""Extract simulation data corresponding to a specified observable
        
        Extract data corresponding to a specified observable from output
        files generated by a simulation in the directory `simdir`

        Current supported observables in DL_MONTE and the syntax is as follows:
        * Scalar quantities output in the YAMLDATA file, e.g. 'energy', are supported.
          To access such a quantity the Observable object must have a descriptor which 
          is a tuple corresponding to the name of the quantity, e.g. ("energy",) for the energy.
        * The number of molecules belonging to a given molecular species is supported.
          To access this the Observable object descriptor must have a descriptor which
          is a tuple with two elements, where the first is "nmols" and the second is
          the index corresponding to the molecular species (where 0 maps to the 1st
          species, 1 maps to the 2nd, etc.). Similar would apply for any other quantities
          output in YAMLDATA which, like 'nmols', are data structures 'of depth 2'. Structures
          of depth 3 or more are not supported.
        * The Observable objects whose descriptors are ("fedparam",), ("fedbias",) and ("fedhist",) 
          retrieve arrays corresponding to the latest, respectively, order parameter bin centres, 
          bias function and histogram of visited bins, for a FED calculation; these are retreved
          from the FEDDAT file with the highest iteration. Analogous data from other FEDDAT files
          can be retrieved by specifying the iteration index as a second element to the tuple, e.g.
          ("fedhist",3) returns the histogram array for the 4th FEDDAT file (noting that iteration 0
          corresponds to the 1st FEDDAT file, 1 corresponds to the 2nd, etc.). Negative iteration
          indices are supported, e.g. ("fedbias",-2) yields the bias function array for the 2nd to last
          iteration.

        Parameters
        ----------
        observable : task.Observable
            An observable
        simdir : str
            The directory containing the output files to extract data from

        Returns
        -------
        array
            An array containing one or more values corresponding to 
            `observable`.
       
        Raises
        ------
        ValueError
            If `observable` is not recognised or supported by this function

        Notes
        -----
        * Normally the returned array would be a time series, e.g., if
          `observable` is "energy" then the returned array would contain
          the observed values of the energy vs. simulation time obtained
          from the simulation. However the array need not necessarily be
          a time series. E.g. it could be a radial distribution function.
          The nature of the values will depend on `observable`

        Examples
        --------
        Create an interface instance which is linked to an executable
        called 'DLMONTE-SRL.X' (which can be found by the system due to
        appropriate set up of the environment, e.g. in unix systems
        including the directory containing the executable in the PATH 
        environmental variable). Then, extract the energy as a time
        series, and store it in a 1D numpy array `energies`, from the 
        output files from a previous simulation performed in a directory 
        `dir1`

        >>> dlmlinker = dlmonteinterface.DLMonteInterface('DLMONTE-SRL.X')
        >>> energies = dlmlinker.resume_sim( ("energy",), dir1)

        Similarly, extract the number of molecules belonging to the 2nd
        molecular species defined in the FIELD file in `dir1` as a time
        series and store it in an array `nmol`

        >>> dlmlinker = dlmonteinterface.DLMonteInterface('DLMONTE-SRL.X')
        >>> nmol = dlmlinker.resume_sim( ("nmols",1), dir1)

        """

        # Load data - including YAMLDATA, and FEDDAT data if applicable
        # After this 'simoutput.yamldata.metadata' contains the metadata
        # and 'simoutput.yamldata.data' contains the data
        simoutput = dlmonte.DLMonteOutput.load(simdir)


        # Catch FEDDAT-related variables first...
        iteration = -1
        if observable.descriptor[0] == "fedparam":
            if len(observable.descriptor)>1:
                iteration = observable.descriptor[1]
            return simoutput.feddat.param(iteration)

        elif observable.descriptor[0] == "fedbias":
            if len(observable.descriptor)>1:
                iteration = observable.descriptor[1]
            return simoutput.feddat.bias(iteration)

        elif observable.descriptor[0] == "fedhist":
            if len(observable.descriptor)>1:
                iteration = observable.descriptor[1]
            return simoutput.feddat.hist(iteration)



        # If the observable is not FEDDAT-related, look for YAMLDATA-related variables...
       
        # Gather data corresponding to the observable of interest
        data = []
        for frame in simoutput.yamldata.data:

            # How to map the elements of observable.descriptor to the
            # appropriate element in 'frame'...
            #
            # To get, e.g., frame['energy'], assume observable.descriptor = ('energy',),
            # and that len(observable.descriptor)==1
            #
            # To get, e.g., frame['nmol'][2], assume observable.descriptor = ('nmol',2),
            # and that len(observable.descriptor)==2.
            #

            if len(observable.descriptor) == 1:
                
                data.append(frame[observable.descriptor[0]])

            elif len(observable.descriptor) == 2:
                
                data.append( frame[observable.descriptor[0]][observable.descriptor[1]] )

            elif len(observable.descriptor) > 2:

                raise NotImplementedError("Depth in YAML frame greater than 2 not supported")

        return data




    def amend_input_parameter(self, dir, param, value):

        r"""Amend a specific simulation input parameter

        Amend the parameter `parameter` in the input files in `dir` to 
        take the value `value`.

        Supported parameters are currently limited to the following parameters
        in the DL_MONTE CONTROL file:
        * Parameters corresponding to 'a key word followed by a value' in the 'main' block of
          the CONTROL file, e.g. 'pressure', 'temperature'. In this case the name of the
          key word should be used as `param`. 
        * The thermodynamic activity or chemical potential for the molecule in a grand-canonical
          Monte Carlo simulation involving insertion and deletion of *only one* molecular species.
          In this case `param` should be 'molchempot'.
        * If `param` is 'flavour', 'method' or 'orderparam', then, respectively, the flavour,
          method or order parameter in the FED block of CONTROL will be set to `value`.

        Parameters
        ----------
        dir : str
            The directory containing the input files
        parameter : str
            Name of parameter to amend
        value : str
            New value of the parameter

        Raises
        ------
        ValueError
            If `parameter` is not recognised or supported by this function

        Examples
        --------
        Create an interface instance which is linked to an executable
        called 'DLMONTE-SRL.X' (which can be found by the system due to
        appropriate set up of the environment, e.g. in unix systems
        including the directory containing the executable in the PATH 
        environmental variable). Then, change the pressure to be considered
        in the simulation whose input files are contained in a directory 
        `dir1` to 10.0

        >>> dlmlinker = dlmonteinterface.DLMonteInterface('DLMONTE-SRL.X')
        >>> dlmlinker.amend_input_parameter(dir1, 'pressure', 10.0 )


        """

        # This is not general and a bit scrappy, and should be improved
        
        # As a special case catch the thermodynamic activity or chemical potential in DL_MONTE
        # for a molecule. THIS WORKS ON THE FIRST MOLECULE ONLY IN GCMC INSERT MOLECULE MOVES.
        siminput = dlmonte.DLMonteInput.from_directory(dir)

        if param=="molchempot":

            # The relevant location is siminput.control.main_block.moves.
            # Search through the moves and locate the molecule GCMC move
            for move in siminput.control.main_block.moves:
                
                if isinstance(move,dlmove.InsertMoleculeMove):
                    move.movers[0]["molpot"] = value
                    

        elif param in ['flavour', 'method', 'orderparam']:
            if param == 'flavour':
                import dlmontepython.htk.sources.dlfedflavour as fedf
                siminput.control.use_block.fed_block.flavour = fedf.from_string(value)
            elif param == 'method':
                import dlmontepython.htk.sources.dlfedmethod as fedm
                siminput.control.use_block.fed_block.method = fedm.from_string(value)
            elif param == 'orderparam':
                import dlmontepython.htk.sources.dlfedorder as fedo
                siminput.control.use_block.fed_block.orderparam = fedo.from_string(value)

        else:
            # Amend CONTROL file for now only
            siminput.control.main_block.statements[param] = value

        siminput.to_directory(dir)


        
