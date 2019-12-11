'''

This file is called after VClamp_runjobs.py. Save data into one file.

'''

import numpy as np

hostname = 'chenfei'
model = 'Brette'
codedirectory = '..'
datafolder = '/scratch/%s/%s/'%(hostname, model)
runs = 1000

for posNa in (20, ): 
  appendix = 'posNa%s'%(posNa)
  foldername = datafolder + 'VClamp/' + appendix  
  va_all = []
  vs_all = []
  m_all = []
  for i in range(1, runs+1):
    data = np.load(foldername+'/VClamp_run_%d.npy'%(i), allow_pickle=True)
    data = data.item()
    va_all.append(data['va'])
    vs_all.append(data['vs'])
    m_all.append(data['m'])
  np.save(datafolder + 'VClamp/' + appendix + '_va_vs_m', {'va':va_all, 'vs':vs_all, 'm':m_all})
