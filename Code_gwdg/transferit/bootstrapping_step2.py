'''

Determine bootstrapping boundaries from 1000 bootstrapping linear response curves.

Linear response curves should be calculated with transferit.py before running this file.

'''

import numpy as np

hostname = 'chenfei'
model = 'Brette'
runs = 10
codedirectory = '..'
datafolder = '/scratch/%s/%s/'%(hostname, model)

for tau in (5, ): 
  for (thr,posNa) in ((-23,20),):
    for fr in (5, ): 
      appendix = 'tau%sfr%sthreshold%sposNa%s'%(tau, fr, thr, posNa)
      foldername = datafolder + appendix
      gain = []
      # Load linear response curves
      for i in range(1,runs+1):
        data = np.load(datafolder+appendix+'/bootstrapping/transferdata_bootstrapping_%d.npy'%(i), allow_pickle=True)
        dic = data.item()
        gain.append(dic['gain'])
      
      # Sort all curves to determine the 95 percent boundary.
      gain_all = np.array(gain)
      gain = np.sort(gain_all, axis=0)
      bootstrapping_gain_lower = gain[int(runs*0.025)] # take the 95 percent in the middle as the confidence interval
      bootstrapping_gain_upper = gain[int(runs*0.975)]
      if thr<0:
        thr = 'n%d'%(abs(thr))
      else:
        thr = '%d'%(thr)
      data_appendix = 'tau%sfr%sthreshold%sposNa%s'%(tau, fr, thr, posNa)
      data = np.load(datafolder+'dynamic_gain_Hz_per_nA_%s.npy'%(data_appendix), allow_pickle=True)
      dic = data.item()
      dic['bootstrapping_gain_lower_%s'%(data_appendix)] = bootstrapping_gain_lower
      dic['bootstrapping_gain_upper_%s'%(data_appendix)] = bootstrapping_gain_upper
      # Save bootstrapping boundaries in linear response curve data file.
      np.save(datafolder+'dynamic_gain_Hz_per_nA_%s.npy'%(data_appendix), dic)
