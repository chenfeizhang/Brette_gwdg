'''

This file calls VClamp_runme.py to calculate the stationary axonal voltage and gating variable of sodium channels under voltage clamp at soma.

'''

import os
import numpy as np
import subprocess
from subprocess import call

# model name, code directory and data directory
hostname = 'chenfei'
model = 'Brette'
runs = 1000 # number of jobs
codedirectory = '..'
datafolder = '/scratch/%s/%s/'%(hostname, model)
outputdirectory = '%sOutput/'%(datafolder)
if os.path.isdir(datafolder) == False:
  os.mkdir(datafolder)
if os.path.isdir(outputdirectory) == False:
  os.mkdir(outputdirectory)
rootfolder = datafolder + 'VClamp/'
if os.path.isdir(rootfolder) == False:
  os.mkdir(rootfolder)

# command for submitting jobs
def submit_job_array(num_jobs: int, working_directory: str, programme: str, args: list):
    command = ["sbatch"]
    command += ["-p", "medium"]                 # select the partition (queue)
    command += ["-t", "10:00"]                  # maximum runtime
    command += ["--array=1-{}".format(num_jobs)]  # make this a job array
    command += ["-C", "scratch"]                # request access to scratch2
    command += ["--chdir", working_directory]   # set working directory
    command += ["--output", outputdirectory+"%A_%a.out"]
    command += [programme] + args

    print(" ".join(command))
    subprocess.check_call(command)

for posNa in (20,): 
  appendix = 'posNa%s'%(posNa)
  foldername = datafolder + 'VClamp/' + appendix  
  param = {}
  param['posNa'] = posNa
  param['codedirectory'] = codedirectory   
  param['model'] = model 
  if os.path.isdir(foldername) == False:
    os.mkdir(foldername)
  np.save(foldername+'/param', param)
  submit_job_array(runs, ".", "runme.sh", [model, "VClamp_runme.py", foldername])

