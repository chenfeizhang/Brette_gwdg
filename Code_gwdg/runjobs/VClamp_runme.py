'''

This file returns axonal voltage and gating variable of sodium channels under voltage clamp.

Threshold is set to 60mV to avoid spike generation. Simulation duration is set to 1000ms such that axonal voltage and gating variable is stationary.

'''

import os, sys
from neuron import h
import numpy as np

# Load parameters
os.environ.keys()
i = int(os.environ['SLURM_ARRAY_TASK_ID'])
print('i = %d'%(i))
foldername = sys.argv[-1]
data = np.load(foldername + '/param.npy', allow_pickle=True)
param = data.item()
for key, val in param.items():
  exec(key + '=val')

h('posNa=%f'%(posNa))
h('T=1000') # duration of voltage clamp, long enough for stationary axonal voltage.
h('threshold=60') # Set threshold high enough to avoid spike generation.

# Set up neuron model.
h('load_file("nrngui.hoc")')
h.load_file('%s/Models/%s/Neuron.hoc'%(codedirectory, model))
h('access soma')
h('objref APgen, stimulus, vAIS, vSoma, m')
h('axon APgen = new NetCon(&v(posNa/axon_L), sodiumchan,threshold,0,0)')
h('axon {sodiumchan.loc(posNa/axon_L)}')

# Set up voltage clamp.
h.stimulus = h.VClamp(0.5) # voltage clamp at the middle of soma
h.stimulus.dur[0] = h.T # duration of voltage clamp
h.stimulus.amp[0] = -75 + 0.075*i # voltage amplitude

# Recording of axonal voltage, somatic voltage, and gating variable of sodium channels.
h.vAIS = h.Vector(int(h.T/h.dt)) # axonal voltage at the position of sodium channels
h.vSoma = h.Vector(int(h.T/h.dt)) # somatic voltage at the middle of soma
h.m = h.Vector(int(h.T/h.dt)) # gating variable of sodium channels
h('vAIS.record(&axon.v(posNa/axon_L))')
h('vSoma.record(&soma.v(0.5))')
h('m.record(&sodiumchan.m)')
h.tstop = h.T # duration of simulation

# Initiate model simulation.
h.finitialize()
h.frecord_init()
h.run()

va = h.vAIS.to_python()
vs = h.vSoma.to_python()
m = h.m.to_python()
# Save stationary voltage values and gating variable.
np.save(foldername + '/VClamp_run_%d'%(i),{'va':va[-1], 'vs':vs[-1], 'm':m[-1]})


