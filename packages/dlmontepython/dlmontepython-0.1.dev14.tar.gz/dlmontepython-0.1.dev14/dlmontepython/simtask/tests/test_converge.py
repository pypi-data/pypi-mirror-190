"""Tests for Converge class"""

import unittest
import os
import shutil

import numpy as np

import dlmontepython.simtask.dlmonteinterface as dlmonteinterface
import dlmontepython.simtask.converge as converge
import dlmontepython.simtask.task as task


class ConvergeSweepTestCase(unittest.TestCase):

    """Tests for ConvergeSweep class"""

    def test_converge_sweep(self):

        """Tests for ConvergeSweep class using DL_MONTE as the simulation
        engine. Note that this test requires DL_MONTE to be installed on the
        local system, and the PATH environment variable to be set to include 
        the path to the serial DL_MONTE executable 'DLMONTE-SRL.X'. 
        WARNING: This overwrites the 'converge_test_data_output.tmp' directory
        if it exists."""


        # This test runs a transition matrix GCMC simulations for the Lennard-Jones 
        # system in a sweep over various thermodynamic activities and compares the 
        # results to benchmark.

        # Link to serial DL_MONTE executable, which must be visible via the
        # PATH environment variable.
        interface = dlmonteinterface.DLMonteInterface("DLMONTE-SRL.X")

        bias_obs = task.Observable( ("fedbias",) )
        observables = [ bias_obs ]
        
        # ... corresponding threshold precision for bias
        precisions= { bias_obs : float(0.05) }

        # Set the name of the directory for the output files, and delete any old
        # versions of it before running the simulations
        # Use the subdirectory 'converge_test_data_output.tmp' relative to the directory
        # containing this script as the directory.
        outputdir = os.path.join( os.path.dirname(__file__), "converge_test_data_output.tmp")
        if os.path.isdir(outputdir):
            shutil.rmtree(outputdir)

        
        # Use the subdirectory 'converge_test_data' relative to the directory
        # containing this script as the directory containing the input files
        inputdir = os.path.join( os.path.dirname(__file__), "converge_test_data")
        converge_template = converge.Converge(interface, observables, precisions=precisions,
                                              inputdir=inputdir)

        # Thermodynamic activities to consider in sweep
        activities = np.logspace(-3.0, 1.3333333333, 5)  

        sweep = converge.ConvergeSweep(param="molchempot", paramvalues=activities,
                                       converge_template=converge_template,
                                       outputdir=outputdir)
        
        # Run the calculations
        sweep.run()


        # Compare the results to a benchmark - specifically, the 'fedbias_converge.dat' file for the
        # highest activity considered
        benchdata = np.array([[2, 9.937395735899997],
                              [3, 2.38804647180001],
                              [4, 0.7915801930999891],
                              [5, 0.37262001500000963],
                              [6, 0.20332088050000152],
                              [7, 0.12824797269999522],
                              [8, 0.09043006240000295],
                              [9, 0.06570662250000225],
                              [10, 0.049849814699996386]])

        simfile = os.path.join( os.path.dirname(__file__), "converge_test_data_output.tmp", 
                                "param_"+str(activities[-1]), "fedbias_converge.dat")
        simdata = np.loadtxt( simfile )

        np.testing.assert_almost_equal( simdata, benchdata, decimal=10 )
            



if __name__ == '__main__':

    unittest.main()
