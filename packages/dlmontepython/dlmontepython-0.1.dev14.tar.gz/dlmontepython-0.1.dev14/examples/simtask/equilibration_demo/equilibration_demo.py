# This script uses the equilibration_test function in the dlmontepython.simtask.analysis
# module to determine the equilibration time for a time series in the file 'timesereis.dat'
# contained in the current directory. Moreover, it calculates the post-equilibration correlation
# time and statistical inefficiency for the time series, as well as a mean and standard error 
# using block averaging. The script also uses the pymbar.timeseries.detect_equilibration function
# to determine an equilibration time and inefficiency, allowing a comparison between
# dlmontepython and pymbar to be made. These data are output to stdout. Finally, this script 
# creates plots of the time series illustrating the equilibration times obtained from 
# dlmontepython and pymbar, and the p-value versus time which underpins dlmontepython's 
# equilibration test.
#
# NOTE: This script requires 'pymbar' to be installed (as well as various common packages, e.g.
# 'matplotlib').

import dlmontepython.simtask.analysis as analysis
import matplotlib.pyplot as plt
import numpy.random as random
import numpy as np
import math
from pymbar import timeseries
from matplotlib.ticker import AutoMinorLocator

# 'timeseries.dat' is in the current directory, and is simply a column of numbers which constitutes
# the time series
y = np.loadtxt("timeseries.dat")

# Rescale the time series for the sake of cleaner presentation
y = y / 10000.0


# Analysis using dlmontepyton...

# Apply dlmontepython's equilibration_test to all points along the time series, storing the
# pvalues at all times in the array 'pvalues'. This block of code is simply to gather data for the
# plot of p-value versus time later. A more realistic application of the equilibration_test function
# is performed below
checktimes = np.linspace(0.0,1.0,len(y)//10)
pvalues = -1.0*np.ones(len(checktimes))
for i in range(0,len(checktimes)):
   check = checktimes[i]
   flatslice, slicepos, pvalue, tau = analysis.equilibration_test(y, checktimes=[check], return_details=True)
   pvalues[i] = pvalue

# Apply dlmontepython's equilibration_test to all points along the time series in order to 
# determine whether the time series has equilibrated (stored in 'flatslice'), the equilibration time 
# (stored in 'slicepos'), the p-value at the determined point of equilibration ('pvalue') and the
# correlation time at the point of equilibration ('tau')
flatslice, slicepos, pvalue, tau = analysis.equilibration_test(y, checktimes=checktimes, return_details=True)
# One could salculate the statistical inefficiency ('s') from the correlation time using the 
# appropriate equation. However here I opt to simply calculate it using the 'analysis.inefficiency'
# function applied to the post-equilibration time series
s = analysis.inefficiency(y[slicepos:])

print("dlmontepython...")
print("   equilibration = ",flatslice)
print("   equilibration time = ",slicepos)
print("   pvalue = ",pvalue)
print("   correlation time = ",tau)
print("   inefficiency = ",s)

# Perform block averaging...

# Use correlation time to inform block size in block
# averaging: we use 4 times the correlation time.
blocksize = 4 * math.ceil(tau)
print("   block size = ",blocksize)
# Calculate the mean energy E and standard error dE
# using block averaging -  for post-equilibration data
E, dE = analysis.standard_error(y[slicepos:], blocksize)
print("Mean and standard error = ", E, dE)


# Calculate the equilibration time and inefficiency using pymbar...

nskip = 10 # only try every 10 samples for time origins
t0, g, Neff_max = timeseries.detect_equilibration(y, nskip=nskip)
print("pymbar...")
print("   equilibration time = ",t0)
print("   inefficiency = ",g)
if g>1.0:
    gtau = -1.0/math.log(1.0-2.0/(g+1.0))
else:
    gtau = 0.0
print("   correlation time = ",gtau)
print("   number of uncorrelated samples = ",Neff_max)
    

# Plot the timeseries versus time (upper plot) showing the dlmontepython and
# pymbar equilibration times (horizontal solid red and blue lines, respectively), 
# and the dlmontepython mean (dotted horizontal red line); and the p-value 
# versus time (lower plot) alongside the threshold of 0.05 which signifies
# equilibration (dotted horizontal black line).

fig, ax = plt.subplots(nrows=2, ncols=1)

for i in [0,1]:
    ax[i].tick_params(top=True, bottom=True, left=True, right=True, which='both')
    ax[i].tick_params(axis="x", which='both', direction="in")
    ax[i].tick_params(axis="y", which='both', direction="in")
    ax[i].xaxis.set_minor_locator(AutoMinorLocator())
    ax[i].yaxis.set_minor_locator(AutoMinorLocator())
    ax[i].set_xlim(-len(y)//20,len(y)+len(y)//20)


ax[0].plot(y,c='gray')
ax[0].axvline(x=slicepos, label = 'dlmontepython', color = 'r')
ax[0].axvline(x=t0, label = 'pymbar', color = 'b', linestyle='dashed')
ax[0].set_ylabel("Energy (arb. units)")
ax[0].legend(frameon=False)
ax[0].set_ylim(-4.034,-3.986)
ax[0].axhline(y=E, xmin=slicepos/len(y), color = 'r', linestyle='dotted')


ax[1].plot(len(y)*checktimes,pvalues, c='gray')
ax[1].axhline(y=0.05, linestyle='dotted', c='black')
ax[1].axvline(x=slicepos, label = 'dlmontepython', color = 'r')
ax[1].set_ylim(0,1)
ax[1].set_ylabel("p-value")
ax[1].set_xlabel("MC steps")

plt.show()

