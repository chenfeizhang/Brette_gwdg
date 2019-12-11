'''
This module file provides a simulation function of Brette model and a stimulus generation function. 
With the simulation function, the axonal voltage with the maximum votlage derivative (spike time threshold) can be determined. 
With the stimulus generation function, both constant and stochastic stimuli can be generated. The stochastic stimuli are generated with the Ornstein-Uhlenbeck process. When the std of the stochastic stimulus is set to zero, the stimulus is constant.
This file also provides a self-test for model simulation. To run the self-test for Brette model: ~/Code_git/Models/Brette/x86_64/special -python model_simulation.py Brette
'''

def simulation(model, tau, posNa, T, threshold, stim_mean, stim_std, frequency, dt=0.025, seednumber=1): 
  '''
  simulation(object) -> va (axonal voltage at the AP initiation site in mV)
  Simulate the neuron model based on model setup and stimulus parameters.
  
  Parameters: Meanings [Example Values]
  model: model name ['Brette']
  tau: correlation time of stimulus (ms) [5]
  posNa: position of sodium channels (um) [20]
  T: duration of stimulus and simulation (ms) [20000]
  threshold: axonal reset voltage for finishing spikes (mV) [-23]
  stim_mean: mean of stochastic stimulus (nA) [0.0185]
  stim_std: std of stochastic stimulus (nA) [0.046]
  dt: time step of model simulation (ms) [0.025]
  seednumber: random seed number for stimulus generation [1]
  '''
  import os, sys
  from neuron import h
  from math import pi
  import numpy as np

  # Load parameters into NEURON.
  h('dt=%f'%(dt)) 
  h('posNa=%f'%(posNa)) 
  h('threshold=%f'%(threshold))
  
  # Set up neuron model.
  h.load_file('nrngui.hoc') # Load nrngui.
  h.load_file('../Models/%s/Neuron.hoc'%(model)) # Load hoc file of neuron model.
  h('access soma')
  h('objref APgen, stimulus, stim, vAIS, vSoma')
  h('axon APgen = new NetCon(&v(posNa/axon_L), sodiumchan,threshold,0,0)') # Define action potential generation.
  h('axon {sodiumchan.loc(posNa/axon_L)}') # Insert sodium channels in axon.

  # Set up stimulus.
  h.stimulus = h.IClamp(0.5) # Stimulus is injected in the middle of soma.
  h.stimulus.dur = T # duration of simulus
  h.stim = h.Vector()
  sinwave = 0.01*np.sin(2*pi*frequency*np.arange(int(T/dt))*dt/1000.0) # NEW!! sinewave
  h.stim.from_python(sinwave) # Generate the stimulus with the OU process. # !!!
  h('stim.play(&stimulus.amp, dt)') 

  # Axonal voltage recording
  h.vAIS = h.Vector(int(T/dt)) 
  h.vSoma = h.Vector(int(T/dt))
  h('vAIS.record(&axon.v(posNa/axon_L))') # Axonal voltage is recorded at the position of sodium channels.
  h('vSoma.record(&soma.v(0.5))')
  h.tstop = T # duration of simulation

  # Initiate model simulation
  h.finitialize()
  h.frecord_init()
  h.run()

  va = h.vAIS.to_python() # Convert NEURON vector to numpy array.
  vs = h.vSoma.to_python()
  return va, vs


def stimulate(li, frequency): # li = [stim_mean, stim_std, tau, dt, T, seednumber], frequency of sinusoidal signal
  '''
  simulate(object) -> x (stimulus in nA)
  Generate stimulus for model simulation.
  Parameters and related meanings are the same as those defined in function simulation.
  '''
  from random import seed, gauss
  from math import exp, sqrt, pi, sin

  # Load parameters.
  stim_mean = li[0] 
  stim_std = li[1] # When stim_std is zero, stimulus is constant.
  tau = li[2] 
  dt = li[3] 
  T = li[4] 
  seednumber = li[5]

  # Generate stimulus.
  seed(seednumber) # Define random seed.
  x = [stim_mean] # Start stimulus with stim_mean.
  for i in range(int(T/dt)): # Generate stimulus with Ornstein-Uhlenbeck process.
    if tau != 0:
      x.append(x[-1] + (1 - exp(-dt/tau)) * (stim_mean - x[-1]) + sqrt(1 - exp(-2*dt/tau))*stim_std*gauss(0,1) + (stim_std/10.0)*sin(2*pi*frequency*i*dt/1000.0)) # noise and sine wave 0.1 std amplitude
    else:
      x.append(stim_mean + stim_std*gauss(0,1) + (stim_std/10.0)*sin(2*pi*frequency*i*dt/1000.0)) # white noise for tau=0.

  return x


if __name__ == "__main__":
  '''
  Self-test file for model simulation.
  To estimate the axonal voltage with the maximum votlage derivative, set threshold to 60mV. Inject the neuron model with a constant input.
  '''
  import numpy as np
  import sys

  # Load parameters.
  model = sys.argv[-1]
  dt = 0.025
  tau = 5
  posNa = 40
  T = 1000
  threshold = 60
  stim_mean = 0
  stim_std = 0
  frequency = 100
  # Run model simulation.
  [va, vs] = simulation(model, tau, posNa, T, threshold, stim_mean, stim_std, frequency, dt=dt, seednumber=1)
  print("Model name is %s."%(model))
  maxva = max(va)
  print("Maximum voltage is %f mV."%(maxva))
  if maxva>=60: 
    print("Stimulus is too large, choose a smaller stimulus for spike time threshold estimation.")
   
  
  # np.save('%s_posNa%s'%(model, posNa),{'va':va, 'vs':vs})
  import scipy.io as sio
  sio.savemat('%s_posNa%s_sinusoidal_freq%d'%(model, posNa, frequency),{'va_posNa%d'%(posNa):va,'vs_posNa%d'%(posNa):vs})
