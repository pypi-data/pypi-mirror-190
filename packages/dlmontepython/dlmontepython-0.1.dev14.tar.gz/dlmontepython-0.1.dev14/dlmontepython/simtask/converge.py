r"""
Classes corresponding to a measurement of one or more observables at a given set of
conditions or thermodynamic ensemble until they converge to specified precisions.
"""




import logging
import os
import time
import numpy as np
import copy

import dlmontepython.simtask.task as task
import dlmontepython.simtask.analysis as analysis




logger = logging.getLogger(__name__)








class Converge(task.Task):

    r"""
    Class corresponding to the task of 'converging' one or more observables at a given set of
    conditions or thermodynamic ensemble

    Class corresponding to the task of 'converging' one or more observables at a given set of
    conditions or thermodynamic ensemble. Here `run` performs back-to-back simulations, and
    convergence of target observables is checked after each simulation. 

    The `run` function performs one or more simulations, gathering data from the output
    of the simulations which is then checked for convergence. Each simulation is performed in a separate
    directory, whose name is determined by `simdir_header`. If `simdir_header` were 'sim_',
    then the first simulation would be performed in 'sim_1', the second in 'sim_2', etc. 
    Each subsequent simulation corresponds to a continuation of the previous simulation, 
    and simulations are performed until one of the following three conditions is met:
 
    * A maximum number of simulations `maxsims` has been completed
    * A maximum time limit `maxtime` has been exceeded after any simulation
    * The changes in all observables are less than threshold values specified 
      in `precisions`. To elaborate, for a scalar observable :math:`x` the change in the observable, :math:`\Delta`,
      is :math:`|x^{(n)}-x^{(n-1)}|`, where :math:`|x^{(i)}|` is the value of the observable at the end of
      the simulation :math:`i` and :math:`n` is the index of the simulation which has just 
      been completed. For vector observables :math:`\Delta` is similarly the largest change in any one
      element of the vector: :math:`\Delta=|x_k^{(n)}-x_k^{(n-1)}|`, where :math:`x_j^{(i)}` is element :math:`j`
      of the observable for simulation :math:`i` simulation and :math:`k` is the element of the vector which
      yields the largest value for :math:`|x_j^{(n)}-x_j^{(n-1)}|` over all :math:`j`.
      Obviously this condition cannot be fulfilled until at least the completion of the
      2nd simulation.

    `run` creates a number of output files. After each simulation the change for observable 'obs' 
    (defined above) is output to the file 'obs_convergence.dat' in the directory in 
    which `run` is invoked. Specifically, each line of the file contains the simulation number,
    followed by the change. Thus 'obs_convergence.dat' contains details of the convergence 
    of the observable 'obs' throughout the task.


    Attributes - for controlling the nature of the task
    ---------------------------------------------------
    interface : task.TaskInterface
        TaskInterface object corresponding to the molecular simulation code to
        be used
    observables : tuple
        A set of observables (task.Observable objects) to be measured
    maxsims : int
        The maximum number of simulations to perform (default = 10)
    maxtime : int
        The maximum time this function is to run for, in seconds 
        (default = 604800, which corresponds to one week)
    precisions : dict
        A dictionary containing threshold precisions (floats) for 
        observables: no more simulations will be performed if the changes in
        all observables corresponding to keys in
        `precisions` are below the values associated with the keys
        E.g., { task.Observable('energy') : 1.0E-6, task.Observable('volume') : 1.0E-4}
        corresponds to a precision of 1.0E-6 and 1.0E-4 for the energy
        and volume respectively. Here by 'change' we mean the difference between
        the value of the observable in the latest simulation relative to the previous
        simulation. If an observable constitutes an array of values, then 'change' means
        the largest change in any one element of the array between the latest and previous
        simulations. (default = {}, i.e., an empty dictionary)
    simdir_header : str
        The header for the names of the directories for the simulations to
        be performed as part of this task. E.g. if `simdir_header` were 'sim_',
        then the 1st simulation would be performed in 'sim_1', the second in
        'sim_2', etc. (default = 'sim_')
    inputdir : str
        The name of the directory containing the input files for the first
        simulation. (default = os.curdir, i.e., the current directory)
    outputdir : str
        The name of the directory where output files and simulation directories
        created by this task will be created. 
        (default = os.curdir, i.e., the current directory)

    Attributes - 'read only'
    ------------------------
    data : dict
        'data[obs][i]' is the data pertaining to observable 'obs' obtained from the '(i+1)'th
        simulation
    diff : dict
        'diff[obs]' is the scalar change in observable 'obs' relative to the previous simulation.
    simdirs : list
        List of directories in which simulations were completed

    """




    def __init__(self, task_interface, 
                 observables, 
                 maxsims=10, maxtime=604800, precisions={}, 
                 simdir_header="sim_", inputdir=os.curdir, outputdir=os.curdir,
                ):

        # Control variables
        self.interface = task_interface
        self.observables = observables
        self.maxsims = maxsims
        self.maxtime = maxtime
        self.precisions = precisions
        self.simdir_header = simdir_header
        self.inputdir = inputdir
        self.outputdir = outputdir

        # 'Read-only' variables 
        self.data = {}
        self.diff = {}
        self.simdirs = []




    def __str__(self):

        r"""Return a readable string representation of a Convergence object

        Return a string representation of Convergence object. Note that
        this does not output the `data` attribute.
        """
        
        string = "Class : "+self.__class__.__name__+"\n"
        string += "Control attributes:\n"
        string += "  interface : "+str(self.interface)+"\n"
        string += "  observables : "+", ".join("%s" % str(obs) for obs in self.observables)+"\n"
        string += "  maxsims : "+str(self.maxsims)+"\n"
        string += "  maxtime : "+str(self.maxtime)+"\n"
        string += "  precisions :\n"+"".join("    %s : %s\n" % (obs,self.precisions[obs]) for obs in self.precisions)
        string += "  simdir_header : "+str(self.simdir_header)+"\n"
        string += "  inputdir : "+str(self.inputdir)+"\n"
        string += "  outputdir : "+str(self.outputdir)+"\n"
        string += "Data attributes:\n"
        string += "  diff : "+", "+str(self.diff)+"\n"
        string += "Other attributes:\n"
        string += "  simdirs : "+", ".join("%s" % dir for dir in self.simdirs)+"\n"

        return string




    def run(self):

        r"""Perform the convergence task

        Perform the convergence task. See the class-level documentation for 
        details.

        """

        logger.info("")
        logger.info("Beginning convergence task...")
        logger.info("")

        logger.debug("Snapshot of this task:\n")
        logger.debug(self)
        logger.debug("")

        # Start time in seconds
        start_time = time.time()


        # Delete old task output files if they exist
        for obs in self.observables:

            # More pythonic to use try statement to remove file and catch OSError
            # if the file doesn't exist, then pass

            convergefilename = str(self.outputdir)+"/"+str(obs)+"_converge.dat"

            if os.path.exists(convergefilename):

                logger.warning("WARNING: Deleting file '"+str(convergefilename)+"'")
                os.remove(convergefilename)


        logger.info("")
        logger.info("Beginning simulations...")

        for i in range(0,self.maxsims):
            
            simno = i+1

            logger.info("")
            logger.info("")
            logger.info("On simulation "+str(simno)+" of max. "+str(self.maxsims)+"...")
            logger.info("")

            simdir = self.outputdir+"/"+self.simdir_header+str(simno)
            logger.info("Setting up directory '"+simdir+"' for simulation...")
            if not os.path.exists(self.outputdir):
                logger.debug("Creating directory '"+self.outputdir+"'...")
                os.mkdir(self.outputdir)
            logger.debug("Creating directory '"+simdir+"'...")
            os.mkdir(simdir)

            if simno==1:

                # We must start a new simulation...

                logger.debug("Copying input files to '"+simdir+"'...")
                self.interface.copy_input_files(self.inputdir, simdir)

                logger.info("Running simulation in '"+str(simdir)+"'...")
                self.interface.run_sim(simdir)
                logger.info("Simulation complete")

                self.simdirs.append(simdir)

            else:

                # We are resuming the previous simulation...

                logger.info("Running simulation in '"+str(simdir)+"'...")
                prevsimdir = self.outputdir+"/"+self.simdir_header+str(simno-1)
                logger.debug("(Resuming simulation from '"+str(prevsimdir)+"')")
                self.interface.resume_sim(prevsimdir, simdir)
                logger.info("Simulation complete")
            

            # Extract and analyse the data for each observable...
            for obs in self.observables:

                logger.info("")
                logger.info("Extracting data for observable '"+str(obs)+"'...")

                try:
                
                    simdata = self.interface.extract_data(obs, simdir)

                except:

                    logger.error("ERROR: Problem extracting data for observable '"+str(obs)+"' from '"+str(simdir)+"'")
                    raise
                
                
                # Check that there actually is data before proceeding with the analysis, and that it is an array

                assert hasattr(simdata, "__len__"), "ERROR: Data for observable '"+str(obs)+"' in '"+str(simdir)+"' is not an arrray"

                if len(simdata)==0:

                    logger.error("ERROR: No data was found for observable '"+str(obs)+"' in '"+str(simdir))
                    raise

                # It is assumed that the data is an array, though the significance of the elements in
                # the array depends on the nature of the variable
                logger.debug("Info regarding data for '"+str(obs)+"' extracted from last simulation:")
                logger.debug("  number of data points = "+str(len(simdata)))
                logger.debug("  up to first 10 data points = "+str(simdata[:10]))
                logger.debug("  last data point = "+str(simdata[len(simdata)-1]))

                logger.debug("Appending to cummulative data for this observable...")

                # Recall that self.data[obs][i] is the data array corresponding to simulation number (i+1)
                if simno==1:

                    self.data[obs] = np.vstack((simdata,))

                else:

                    # To calculate the change in the observable relative to the previous simulation it is necessary
                    # that the sizes of the data arrays obtained from each iteration are all the same. Check this is
                    # the case
                    assert len(simdata) == len(self.data[obs][0]), "ERROR: Data array for observable '"+str(obs)+\
                        "' in '"+str(simdir)+"' is not same size as in initial simulation"

                    # ... otherwise the below will fail!
                    self.data[obs] = np.vstack((self.data[obs],simdata))


                logger.debug("Info regarding all extracted data for '"+str(obs)+"':")
                logger.debug("  data from most first simulation (up to 10 elements)  = "+str(self.data[obs][0]))
                logger.debug("  data from most recent simulation (up to 10 elements) = "+str(self.data[obs][simno-1]))

                logger.info("Extraction complete")

                if simno > 1:

                    logger.info("Quantifying change in observable '"+str(obs)+"' from previous simulation...")

                    # Here the change in the observable is the largest change in the data array relative to the previous iteration
                    logger.debug("Calculating 'diff' in observable as largest change in any element of the observable...")
                    diffvec = self.data[obs][simno-1]-self.data[obs][simno-2]
                    logger.debug("    diffvec (up to 10 elements) = "+str(diffvec[0:10]))
                    self.diff[obs] = np.amax(np.abs(diffvec))
                    logger.debug("    diff = "+str(self.diff[obs]))
                    logger.info("Difference is = "+str(self.diff[obs]))

                    # Output change to file
                    convergefilename = str(self.outputdir)+"/"+str(obs)+"_converge.dat"
                    logger.debug("Outputting change to file '"+str(convergefilename)+"'...")
                    convergefile = open(convergefilename, "a")
                    convergefile.write(str(simno)+" "+str(self.diff[obs])+"\n")
                    convergefile.close()


                else: 

                    logger.info("Bypassing calculation of change in observable '"+str(obs)+"' from previous simulation since only one simulation has been performed")


            logger.info("Calculation of changes in observables is complete")

            logger.debug("")
            logger.debug("Snapshot of this task:\n")
            logger.debug(self)
            logger.debug("")

            logger.info("")
            logger.info("Checking end-of-task criteria...")

            # Cycle over all keys in 'precisions' and check if the analogous 'diff' 
            # is less than it

            logger.debug("Cycling over observables in 'precisions'...")

            reached_precisions = {}

            for obs in self.precisions:

                logger.debug("Considering observable '"+str(obs)+"'")

                # The keys in self.precisions may not actually correspond to any observables in
                # self.diff. Assuming the user has not made an error in setting self.precisions
                # (e.g. by putting 'enerhy' as the key for the observable 'energy'), a KeyError
                # exception would occur below only if self.diff[obs] has not been set, i.e., 
                # there have not been enough iterations yet to calculate self.diff[obs]
                try:

                    obs_diff = self.diff[obs]

                except KeyError:
                    
                    logger.debug("A diff value for this observable has not been found")

                else:

                    logger.debug("A difff value for this observable has been found: "+str(self.diff[obs]))
                    
                    logger.debug("Checking value against threshold of "+str(self.precisions[obs])+"...")
                    
                    if np.abs(self.diff[obs]) < self.precisions[obs]:

                        reached_precisions[obs] = True
                        logger.info("Threshold precision for change in observable '"+str(obs)+"' reached")

                    else:

                        reached_precisions[obs] = False
                        logger.debug("Threshold precision for change in observable '"+str(obs)+"' not yet reached")


            # Check that if the dictionary 'reached_precisions' has any keys,
            # then are they all True. If so then all observables tracked for
            # precision have been calculated to the desired precision
            logger.debug("Dictionary holding booleans for precision threshold criteria:")
            logger.debug("  reached_precisions = "+str(reached_precisions))

            if len(reached_precisions) > 0  and  all( v==True for v in reached_precisions.values() ):

                logger.info("Precision threshold reached for all observables")
                break

            else:

                logger.debug("Precision threshold has not been reached for all observables, or threshold is not in play")


            elapsed_time = time.time() - start_time

            if elapsed_time > self.maxtime:

                logger.info("Task time threshold of "+str(self.maxtime)+"s exceeded:")
                logger.info("  elapsed time = "+str(elapsed_time)+"s")
                break

            
            if(simno==self.maxsims):
                
                logger.info("Reached maximum number of simulations")

            else:

                logger.info("End-of-task criteria not yet reached. Proceeding to next simulation...")


        logger.info("")
        logger.info("")
        logger.info("Completed converge task")

        



# This class is almost identical to MeasurementSweep in measurement.py. Combine into one Sweep object which works
# on both?

class ConvergeSweep(task.Task):

    r"""
    Class corresponding to the task of performing multiple similar 'converge' measurements of
    one or more observables at various values of a control parameter

    Class corresponding to the task of performing multiple similar 'converge' measurements of
    one or more observables at various values of a control parameter

    Attributes - for controlling the nature of the task
    ---------------------------------------------------
    param : str
        The name of the 'control parameter' which will be varied between
        measurements
    paramvalues : list
        The values of the control parameter to be explored
    converge_template : Converge
        A Converge object whose control attributes will be used as a template
        for the measurement at each control parameter listed in `paramvalues` 
    paramdir_header : str
        The header for the name of the directories to contain the simulations
        for each control parameter. (default = 'param_')
    outputdir : str
        The name of the directory where output files and simulation directories
        created by this task will be created. 
        (default = os.curdir, i.e., the current directory)

    Attributes - 'read only'
    ------------------------
    converges : list
        A list of Converge objects corresponding to each control parameter
        in `paramvalues`

    """




    def __init__(self, param, paramvalues, converge_template, 
                 paramdir_header="param_", outputdir=os.curdir):

        self.param = param
        self.paramvalues = paramvalues
        self.converge_template = converge_template
        self.paramdir_header = paramdir_header
        self.outputdir = outputdir
        
        self.converges = []




    def __str__(self):
        
        r"""Return a readable string representation of a ConvergeSweep object

        """

        string = "Class : "+self.__class__.__name__+"\n"
        string += "Simple control attributes:\n"
        string += "  param : "+str(self.param)+"\n"
        string += "  paramvalues : "+str(self.paramvalues)+"\n"
        string += "  paramdir_header : "+str(self.paramdir_header)+"\n"
        string += "START OF TEMPLATE CONVERGE TASK INFO\n"+str(self.converge_template)+"END OF TEMPLATE CONVERGE TASK INFO\n"
        string += "".join( "START OF CONVERGE TASK %s INFO (for paramval = %s)\n%sEND OF CONVERGE TASK %s INFO\n" 
                           % (str(i), str(self.paramvalues[i]), str(self.converges[i]), str(i)) 
                           for i in range(0,len(self.converges)) 
                          )

        return string




    def run(self):

        r"""Perform the task

        Perform the task. See the class-level documentation for 
        details.

        """

        # TO DO: IMPROVE ERROR HANDLING

        logger.info("")
        logger.info("Beginning converge sweep task...")
        logger.info("")
        
        logger.debug("Snapshot of this task:\n")
        logger.debug(self)
        logger.debug("")


        # Delete old task output files if they exist
        for obs in self.converge_template.observables:

            # More pythonic to use try statement to remove file and catch OSError
            # if the file doesn't exist, then pass
            filename = self.outputdir+"/"+str(obs)+"_sweep.dat"
            if os.path.exists(filename):
                logger.warning("WARNING: Deleting file '"+str(filename)+"'")
                os.remove(filename)


        for val in self.paramvalues:
            
            logger.info("")
            logger.info("Beginning converge for control parameter value "+str(val)+"...")
            logger.info("")

            paramdir = self.outputdir+"/"+self.paramdir_header+str(val)
            logger.info("Setting up directory '"+paramdir+"' for control parameter value "+str(val)+"...")
            if not os.path.exists(self.outputdir):
                logger.debug("Creating directory '"+self.outputdir+"'...")
                os.mkdir(self.outputdir)
            logger.debug("Creating directory '"+paramdir+"'...")
            os.mkdir(paramdir)

            # ERROR HANDLING FOR BAD USER INPUT, E.G., NON-EXISTENT CONTROL PARAMETERS?

            logger.debug("Copying input files from '"+self.converge_template.inputdir+"' to '"+paramdir+"'...")
            self.converge_template.interface.copy_input_files(self.converge_template.inputdir, paramdir)

            logger.debug("Amending control parameter in "+str(paramdir)+" to correspond to value "+str(val)+"...")
            self.converge_template.interface.amend_input_parameter(paramdir, self.param, val)
            
            logger.info("Running converge for control parameter "+str(val)+"...")

            logger.debug("Creating new Converge object from template to hold results...")
            converge = copy.deepcopy(self.converge_template)
            logger.debug("Amending new Converge object's input directory to be '"+str(paramdir)+"'...")
            converge.inputdir = paramdir
            logger.debug("Amending new Converge object's output directory to be '"+str(paramdir)+"'...")
            converge.outputdir = paramdir
            logger.debug("Attributes of new Converge object for this control parameter:")
            logger.debug(str(converge))
            logger.debug("")

            logger.debug("Calling run() for Converge object...")
            converge.run()

            logger.info("")                
            logger.info("")
            logger.info("Completed converge for control parameter "+str(val))
            logger.info("")
            logger.info("")

            logger.info("Extracting convergence quantities of all observables for control parameter "+str(val)+"...")

            for obs in converge.observables:

                logger.info("")
                logger.debug("Considering observable "+str(obs)+"...")
                    
                # Only output if there is more than one simulation which has been performed
                if len(converge.data[obs]) >= 1:

                    logger.info("Observable '"+str(obs)+"' diff from previous simulation = "+str(converge.diff[obs]))
                    if np.abs(converge.diff[obs]) < converge.precisions[obs]: 
                        logger.info("Observable '"+str(obs)+"' IS deemed converged")
                    else:
                        logger.info("Observable '"+str(obs)+"' IS NOT deemed converged")

                logger.info("")
                logger.info("Completed extraction of mean and standard error for control parameter "+str(val))
                logger.info("")

                logger.debug("Snapshot of this task:\n")
                logger.debug(self)
                logger.debug("")

        logger.info("")
        logger.info("Convergence sweep task complete")
        logger.info("")



