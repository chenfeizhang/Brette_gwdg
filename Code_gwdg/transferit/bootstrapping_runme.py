'''

This file defines neuron models for bootstrapping and the range of series folders for random selection of STA.

'''

import os, sys, math
from subprocess import call
import numpy as np
from random import randint

runs = 400 # number of series folders
datafolder = sys.argv[-1]
os.environ.keys()
ii = int(os.environ['SLURM_ARRAY_TASK_ID'])
print('ii = %d'%(ii))

from transferit import firing_rate_estimate, STA_average, gain

for tau in (5,):  
  for (thr,posNa) in ((-23,20),): 
    for fr in (5,):
      appendix = 'tau%sfr%sthreshold%sposNa%s'%(tau, fr, thr, posNa)
      fr_estimated = firing_rate_estimate(range(1, runs+1), datafolder, appendix)
      List = [randint(1,runs) for i in range(runs)] # Randomly select STA with replacement.
      STA = STA_average(List, datafolder, appendix) # averaged STA
      [f, gain_filt] = gain(fr_estimated, STA, datafolder, appendix) 
      transferdata = {'f':f, 'gain':gain_filt}
      if os.path.isdir(datafolder+'/%s/bootstrapping'%(appendix)) == False:
        os.mkdir(datafolder+'/%s/bootstrapping'%(appendix))
      np.save(datafolder+'/%s/bootstrapping/transferdata_bootstrapping_%d'%(appendix,ii), transferdata)

