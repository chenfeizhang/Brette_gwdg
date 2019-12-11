'''

Generate axonal voltages and stimuli for calculating electrotonic filtering.

'''
import time
start_time = time.time()

import os, sys
from neuron import h
import numpy as np

# Load parameters
foldername = sys.argv[-1]
os.environ.keys()
i = int(os.environ['SLURM_ARRAY_TASK_ID'])
print('i = %d'%(i))
frequency = i # frequency is the run number
data = np.load(foldername + '/param.npy', allow_pickle=True)
param = data.item()
for key, val in param.items():
  exec(key + '=val')

# Import model simulation function and stimulus generation function.
sys.path.append('%s/Parameters'%(codedirectory))
from model_simulation_sinusoidal import simulation

T_all = T + T_relax # simulation time and randomization of initial condition time
L = int(T/dt) + 1
ftout = np.zeros(int(L/2+1))

for k in range(rep): 
  print('Loop at %d\n' %(k))
  seednumber = i*100+k # i is Series number. k is repitition number.
  [va, vs] = simulation(model, tau, posNa, T_all, 60, mean, std, frequency, dt=dt, seednumber=seednumber) # change the reset threshold to 60mV
  ftout = ftout + np.fft.fft(va[int(T_relax/dt):])[:int(L/2+1)]/L

np.save(foldername + '/freq_%d'%(i), {'ftout':abs(ftout[frequency])})
print('--- %s seconds ---' % (time.time() - start_time))
