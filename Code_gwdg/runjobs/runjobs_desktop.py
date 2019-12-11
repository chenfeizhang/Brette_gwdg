'''

This file calls runme.py to run neuron model simulation and calculate spike triggered average (STA).

STA calculation methods are the same with that in runjobs.py except that this file can be run on desktop to generate a small fraction of data for a preliminary linear response curve.

'''

import os, sys
import numpy as np
import subprocess
from subprocess import call

# model name, code directory and data directory
hostname = 'chenfei'
model = 'Brette_ka01'  
i = 10 # Series number instead of runs
codedirectory = '..'
datafolder = '/scratch/%s/%s/'%(hostname, model)
outputdirectory = '%sOutput/'%(datafolder)
if os.path.isdir(datafolder) == False:
  os.mkdir(datafolder)
  os.mkdir(outputdirectory)

sys.path.append('%s/scripts'%(codedirectory))
from addparam import addparam # Import function addparam for loading parameters from IparamTable.txt.
IparamTableFile = '%s/Models/%s/IparamTable.txt'%(codedirectory,model) # txt file for stimulus parameters

# command for submitting jobs, remove queue options, call runme_desktop.py
programme = '%s/Models/%s/x86_64/special -python' %(codedirectory, model)
script = 'runme_desktop.py'
command = programme + ' ' + script   

for tau in (5, ): 
  for posNa in (20,): 
    for fr in (5,):
      param = {'tau':tau, 'fr':fr, 'posNa':posNa}
      param = addparam(param, IparamTableFile) # add thr, spthr, mean, std to param.
      param['T'] = 20000 # duration of model simulation for STA (ms)
      param['T_relax'] = 500 # duration of initial condition randomization (ms)
      param['rep'] = 1 # repetition number
      param['codedirectory'] = codedirectory   
      param['model'] = model 
      param['dt'] = 0.025
      appendix = 'tau%dfr%dthreshold%dposNa%d'%(tau, fr, param['thr'], posNa)
      foldername = datafolder + appendix
      if os.path.isdir(foldername) == False:
        os.mkdir(foldername)
      # make directory for bootstrapping confidence interval
      if os.path.isdir(foldername+'/bootstrapping') == False:
        os.mkdir(foldername+'/bootstrapping')
      # make directory for null hypothesis test
      if os.path.isdir(foldername+'/nullhypothesis') == False:
        os.mkdir(foldername+'/nullhypothesis')
      call('mkdir -p ' + foldername + '/Series' + str(i) + '/', shell=True)
      np.save(foldername+'/param.npy', param)        
      # send series number i into runme_desktop.py
      call(command + ' ' + str(i) + ' ' + foldername, shell=True) 
   
        
