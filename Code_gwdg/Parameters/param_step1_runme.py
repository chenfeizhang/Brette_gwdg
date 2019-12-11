'''

Search for the constant stimulus just about to trigger spikes and the constant stimulus generates 5Hz firing rate.

Determine the final reset threshold.

'''

import sys, os
from neuron import h
import numpy as np

# Load parameters.
foldername = sys.argv[-1]
data = np.load(foldername + '/param.npy', allow_pickle=True)
param = data.item()
for key, val in param.items():
  exec(key + '=val')

# Import model simulation function and parameter searching function.
sys.path.append('%s/scripts'%(codedirectory))
# Import the function for model simulation.
from model_simulation import simulation
# Import the function for stimulus searching.
from firingonset import FiringOnset 

# Search for constant stimulus.
stim_0 = 0
# stim_start: stimulus just about to fire (fr=0Hz)
stim_start = FiringOnset(simulation, param, leftI, rightI, precisionFiringOnset, 0)
# stim_saturate: stimulus that generates 5Hz firing rate (fr=5Hz) 
stim_saturate = FiringOnset(simulation, param, leftI, rightI, precisionFiringOnset, fr) 

# With the constant input stim_saturate, choose the voltage 2ms after the spike detection voltage as the final reset voltage.
va = simulation(model, tau, posNa, 1000, 60, stim_saturate, 0, dt)
threshold = va[np.argmax(np.diff(va)/dt)+1 + int(2.0/dt)]
print("Reset threshold is %f mV"%(threshold))
param['thr'] = int(threshold)
np.save(foldername + '/param',param)
np.save(foldername + '/mean',{'stim_0':stim_0, 'stim_start':stim_start, 'stim_saturate':stim_saturate,})


