r"""
Base classes for performing molecular simulation workflows.

Base classes for performing molecular simulation workflows. The `Task` class
represents a workflow which employs molecular simulation to perform a certain
task, e.g. calculating the density of a system at a range of temperatures.
It is high-level, in principle agnostic to the choice of molecular simulation 
program used to perform the simulations in the workflow. This is achieved by
abstracting out code pertaining to input/output for the molecular simulation
program. Such code is contained within a `TaskInterface` object which contains
functions to perform such operations, e.g. changing simulation parameters,
invoking a simulation, extracting data from the simulation output files. This
interface is linked to a `Task` instance, thus telling the `Task` object how to
perform the input/output operations for the considered simulation program.

Note that the `Task` and `TaskInterface` classes here are abstract, i.e. they 
provide a template for subclasses which can actually be used to solve problems. 
Subclasses of `Task` will describe particular workflows, and should conform to
the structure of the class given here. Specifically, a subclass of `Task` should
have a `TaskInterface` as an atribute, and have a function `run` which can be
used to instigate the workflow. Subclasses of `TaskInterface` will describe how
to perform input/output operations pertaining to a given molecular simulation
program, and should contain the functions defined in `TaskInterface` here. `Task`
objects should use only these functions to communicate with a molecular simulation
program. This is what enables `Task` objects to be agnostic to the choice of
molecular simulation program. 

"""


import logging




logger = logging.getLogger(__name__)








class Observable(object):

    r"""Class describing data which can be extracted from a molecular simulation 
    program

    Class describing data which can be extracted from a molecular simulation 
    program. Specifically, this is used in the `extract_data` function in the
    `TaskInterface` class. See that function for further details.

    Attributes
    ----------
    descriptor : tuple
        Tuple of variables (normally strings and integers) which characterise
        the observable. For example the observable energy could have `descriptor`
        as ( "energy", ), and the number of molecules belonging to the 2nd
        molecular species in the system could be ( "nmols", 2 )

    """

    def __init__(self, descriptor):

        self.descriptor = descriptor




    def __str__(self):

        r"""Return a readable string representation of an Observable object

        Return a readable string representation of an Observable object, namely,
        string representations of each element in the `descriptor` all joined 
        together by underscores. This whitespace-free string representation is
        useful because the string representation of an Observable will be used
        in constructing names of output files pertaining to that observable,
        for which whitespace is undesirable
        """

        tojoin = []
        for i in range(0,len(self.descriptor)):
            tojoin.append( str(self.descriptor[i]) )
        return "_".join(  tuple(tojoin) )




    # Required for Observable objects to be keys in dictionaries
    def __hash__(self):

        return hash( self.descriptor )




    # Required for Observable objects to be keys in dictionaries
    def __eq__(self, other):

        return self.descriptor == other.descriptor








class TaskInterface(object):

    r"""Base class for interfacing with specific simulation codes

    Base class for interfacing with specific simulation codes. A `Task` object
    must be initialised using a `TaskInterface` object: the latter tells the former
    how to perform various tasks pertaining to the specific molecular 
    simulation code in question. A subclass of `TaskInterface` should be created
    for the particular simulation code one wishes to use with the `Task `class,
    where the functions in this class are overwritten by functions which correspond
    to the simulation code in question. 

    Regarding the `extract_data` function, the class `Observable` corresponds to a
    data type which can be extracted from the output of a molecular simulation program
    using its corresponding `TaskInterface` object. For instance there may be an 
    `Observable` instance which corresponds to the energy time series in the simulation
    directory `simdir`: passing this instance to `extract_data` would result in the 
    function returning the energy time series. Different `TaskInterfaces` objects may
    support different 'libraries' of `Observable` instances, since different molecular 
    simulation programs may be able to generate different types of data. `TaskInterface`
    subclasses should provide in their documentation what `Observable` instances are 
    'supported'.

    Similarly to the `Observable` argument to the function `extract_data`, the meaning of 
    the `parameter` string in `amend_input_parameter` will depend on the `TaskInterface`, 
    since different simulation programs support different types of input parameters. 
    For example, `parameter` might be the pressure to be used in a simulation. 
    `TaskInterface` subclasses shoudl provide in their documentation what `parameter`
    strings are supported.      

    See the module-level documentation for further details.

    """

    def __init__(self):

        # Don't through a NotImplementedError - simple testing is easier
        # if we can create these objects
        pass




    def __str__(self):

        r"""Return a readable string representation of a TaskInterface object

        Return a readable string representation of a TaskInterface object. This
        is simply the class' name
        """

        return self.__class__.__name__




    def copy_input_files(self, fromdir, todir):

        r"""Copy simulation input files between directories

        Copy simulation input files between directories

        Parameters
        ----------
        fromdir : str
            The directory containing the input files
        todir : str
            The target directory for the input files
       
        """

        raise NotImplementedError




    def run_sim(self, simdir):

        r"""Run a simulation

        Run a simulation in a specified directory

        Parameters
        ----------
        simdir : str
            The directory in which the simulation is to be executed
       
        """

        raise NotImplementedError


    

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

        """

        raise NotImplementedError




    def extract_data(self, observable, simdir):

        r"""Extract simulation data corresponding to a specified observable
        
        Extract data corresponding to a specified observable from output
        files generated by a simulation in the directory `simdir`. See the class
        level documentation for more details.

        Parameters
        ----------
        observable : Observable
            The observable to extract
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
          `observable` is an energy then the returned array would contain
          the observed values of the energy vs. simulation time obtained
          from the simulation. However the array need not necessarily be
          a time series. E.g. it could be a radial distribution function.
          The nature of the values will depend on `observable`

        """

        raise NotImplementedError




    def amend_input_parameter(self, dir, parameter, value):
        
        r"""Amend a specific simulation input parameter

        Amend the parameter `parameter` in the input files in `dir` to 
        take the value `value`. See the class level documentation for more 
        details.

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

        """

        raise NotImplementedError








class Task(object):

    r"""Base class corresponding to a workflow.

    Base class corresponding to a workflow. 

    See the module-level documentation for further details.

    Attributes
    ----------
    interface : task.TaskInterface
        TaskInterface object corresponding to the molecular simulation code to
        be used

    """

    def __init__(self, task_interface):

        self.interface = task_interface



    
    def run(self):

        r"""Invoke the workflow

        Invoke the workflow
        """

        raise NotImplementedError













