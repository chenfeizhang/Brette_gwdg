'''

Run neuron model simulation. Calculate STA.

This file is adapted from runme.py for running on desktop.

'''

import sys
from neuron import h
import numpy as np

# Load parameters
foldername = sys.argv[-1]
i = int(sys.argv[-2]) # index of the series number
print('i = %d'%(i))
data = np.load(foldername + '/param.npy', allow_pickle=True)
param = data.item()
for key, val in param.items():
  exec(key + '=val')

# Import model simulation function and stimulus generation function.
sys.path.append('%s/Parameters'%(codedirectory))
from model_simulation import simulation, stimulate

# Parameters for STA and linear response curve calculation
STA_L = 0.8 # Length of STA is 0.8s.
N = int(T/dt) # number of time bins    
dt_s = dt*10**-3 # time step in unit of second
sf = 1/dt_s # sampling frequency
maxtau = int(STA_L/2*sf) # The length of half of a STA
L = maxtau*2 # length of the whole STA
param['N'] = N
param['dt_s'] = dt_s
param['sf'] = sf
param['STA_L'] = STA_L
param['maxtau'] = maxtau
param['L'] = L
np.save(foldername + '/param.npy', param)
spiketimelist = [] # list of spike times for calculating STA
nspikes = 0 # number of spikes for calculating STA
STA_tmp = np.zeros(L) # the sum of all spike triggered stimuli
T_all = T + T_relax # simulation time and randomization of initial condition time

for k in range(rep): 
  print('Loop at %d\n' %(k))
  seednumber = i*100+k # i is Series number. k is repitition number. Repetition number is assumed to be smaller than 100.
  va = simulation(model, tau, posNa, T_all, thr, mean, std, dt=dt, seednumber=seednumber)
  a = np.diff((np.array(va)>spthr)*1.0)
  itemindex = np.where(a==1) 
  sp1 = np.array(itemindex[0]*dt) # spike times in T_relax+T
  sp2 = (sp1[sp1>T_relax] - T_relax)/1000.0 # Rule out spikes in T_relax. Deduct T_relax for later spike times. Change unit to second.
  spiketimelist.append(sp2)  
  sp_STA = np.array([sp for sp in sp2 if sp>(STA_L/2.0) and sp<(T/1000.0-STA_L/2.0)]) # spike time in interval (STA_L/2, T-STA_L/2) for STA
  stim = stimulate([mean, std, tau, dt, T_all, seednumber]) # the stimulus that generates spikes
  stim = stim[int(T_relax/dt):] # deduct the stimulus in T_relax
  for sp in sp_STA:
    STA_tmp_add =  stim[(int(sp/dt_s)-maxtau-1):(int(sp/dt_s)+maxtau-1)] # spike triggered stimulus
    STA_tmp = STA_tmp + np.array(STA_tmp_add)

  nspikes = nspikes + len(sp_STA)
  sys.stdout.flush()

STA = STA_tmp/float(nspikes) - mean
np.save(foldername + '/Series' + str(i) + '/STA', {'STA':STA})
np.save(foldername + '/Series' + str(i) + '/spiketimelist', {'spiketimelist':spiketimelist})
