'''

Summarize the mean-std and mean-CV relation. Find the mean and std that reproduce expected firing rate and CV by hand.

'''

import numpy as np
import os.path

hostname = 'chenfei'
model = 'Brette'
codedirectory = '..'
datafolder = '/scratch/%s/%s/'%(hostname, model)
outputdirectory = '%sOutput/'%(datafolder)
runs = 100

for tau in (5,): 
  for (spthr,posNa) in ((-35, 20),):
    for fr in (5,):
      appendix = 'tau%dfr%dspthr%dposNa%d'%(tau, fr, spthr, posNa)
      foldername = datafolder + 'Param/' + appendix  
      data = np.load(foldername + '/param.npy', allow_pickle=True)
      param = data.item()
      thr = param['thr']
      mean =  []
      std = []
      cv = []
      for i in range(1,runs+1):
        if os.path.isfile(foldername+'/mean%d/std_mean_cv.npy'%(i)) == True:
          data = np.load(foldername+'/mean%d/std_mean_cv.npy'%(i), allow_pickle=True)
          dic = data.item()
          mean.append(dic['mean'])
          std.append(dic['std'])
          cv.append(dic['cv'])
        else: continue

      if thr<0:
        spthr = 'n%d'%(abs(spthr))
      else:
        spthr = '%d'%(spthr)
      data_appendix = 'tau%sfr%sspthr%sposNa%s'%(tau, fr, spthr, posNa)
      np.save(foldername+'_mean_std_cv',{'mean_%s'%(data_appendix):mean, 'std_%s'%(data_appendix):std, 'cv_%s'%(data_appendix):cv, 'thr_%s'%(data_appendix):thr})
