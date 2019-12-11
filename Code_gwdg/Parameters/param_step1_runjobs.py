''' 

Search for constant input to realize expected firing rate.

Current file defines model name and parameters, calls param_step1_runme.py, and submits jobs to clusters for constant input searching. 

With the knowledge of spike time threshold, temporarily choose reset threshold slightly larger than spike time threshold. Search for the constant input based on the temporary reset threshold. Final reset threshold is defined as the axonal voltage 2ms after the spike time threshold under the constant input.

'''
import numpy as np
import os
import subprocess
from subprocess import call 

# model name, code directory and data directory
hostname = 'chenfei'
model = 'Brette' # model name
codedirectory = '..' # code directory
datafolder = '/scratch/%s/%s/'%(hostname, model) # data directory
outputdirectory = '%sOutput/'%(datafolder) # output directory

# command for submitting jobs
def submit_job_array(num_jobs: int, working_directory: str, programme: str, args: list):
    command = ["sbatch"]
    command += ["-p", "medium"]                 # select the partition (queue)
    command += ["-t", "60:00"]                  # maximum runtime
    command += ["--array=1-{}".format(num_jobs)]  # make this a job array
    command += ["-C", "scratch"]                # request access to scratch2
    command += ["--chdir", working_directory]   # set working directory
    command += ["--output", outputdirectory+"%A_%a.out"]
    command += [programme] + args

    print(" ".join(command))
    subprocess.check_call(command)


# Make directories for data and output files.
if os.path.isdir(datafolder) == False:
  os.mkdir(datafolder)
if os.path.isdir(outputdirectory) == False:
  os.mkdir(outputdirectory)
rootfolder = datafolder + 'Param/'
if os.path.isdir(rootfolder) == False:
  os.mkdir(rootfolder)

# Define parameters and submit jobs to clusters.
# tau: correlation time of stimulus (ms)
# thr: reset threshold (mV)
# spthr: spike time threshold (mV)
# posNa: position of sodium channels (um)
# fr: firing rate (Hz)
# leftI: lower bound of constant stimulus searching range (nA)
# rightI: upper bound of constant stimulus searching range (nA)
# precisionFiringOnset: precision of stimulus searching
# T: duration of stimulus and simulation (ms)
# dt: time step of model simulation (ms)

for tau in (5, ):
  for (thr, spthr, posNa) in ((-33, -34, 40),): 
    for fr in (5,): 
      leftI = 0.00001 # chosen by hand
      rightI = 0.05 # chosen by hand
      precisionFiringOnset = 1e-2 # Searching stops when the upper and lower bounds are close enough.
      T = 20000 
      dt = 0.025
      param = {}
      param['tau'] = tau
      param['thr'] = thr
      param['spthr'] = spthr
      param['posNa'] = posNa
      param['fr'] = fr
      param['T'] = T
      param['codedirectory'] = codedirectory   
      param['model'] = model 
      param['leftI'] = leftI
      param['rightI'] = rightI
      param['precisionFiringOnset'] = precisionFiringOnset
      param['dt'] = dt
      appendix = 'tau%dfr%dspthr%dposNa%d'%(tau, fr, spthr, posNa)
      foldername = rootfolder + appendix
      param['foldername'] = foldername
      call('mkdir -p ' + foldername, shell=True) 
      np.save(foldername+'/param', param) # save data in param.npy
      submit_job_array(1, ".", "runme.sh", [model, "param_step1_runme.py", foldername]) # Submit jobs, pass foldername into the job script.



