'''

Take the 95 percent bound of these linear response curves as the final null hypothesis test curve. 

'''

import numpy as np

hostname = 'chenfei'
model = 'Brette'
runs = 100 # null hypothesis runs
codedirectory = '..'
datafolder = '/scratch/%s/%s/'%(hostname, model)

for tau in (5,): 
  for (thr,posNa) in ((-23,20),): 
    fr = 5 
    appendix = 'tau%sfr%sthreshold%sposNa%s'%(tau, fr, thr, posNa)
    foldername = datafolder + appendix
    gain = []
    for i in range(1,runs+1):
      data = np.load(datafolder+appendix+'/nullhypothesis/transferdata_nullhypothesis_run%d.npy'%(i), allow_pickle=True)
      dic = data.item()
      gain.append(dic['gain'])
    
    gain = np.array(gain)
    gain = np.sort(gain, axis=0)
    nullgain = gain[int(runs*0.95)]
    if thr<0:
      thr = 'n%d'%(abs(thr))
    else:
      thr = '%d'%(thr)
    data_appendix = 'tau%dfr%dthreshold%sposNa%d'%(tau, fr, thr, posNa)
    data = np.load(datafolder+'/dynamic_gain_Hz_per_nA_%s.npy'%(data_appendix), allow_pickle=True)
    dic = data.item()
    dic['nullgain_%s'%(data_appendix)] = nullgain
    np.save(datafolder+'dynamic_gain_Hz_per_nA_%s.npy'%(data_appendix), dic)
