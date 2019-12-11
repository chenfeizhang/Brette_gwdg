import subprocess
import os, sys
import numpy as np

# model name, code directory and data directory
hostname = 'chenfei'
model = 'Brette'  
runs = 400 # number of jobs
codedirectory = '..'
datafolder = '/scratch/%s/%s/'%(hostname, model)

outputdirectory = '%sOutput/'%(datafolder)
if os.path.isdir(datafolder) == False:
  os.mkdir(datafolder)
  os.mkdir(outputdirectory)

def submit_job_array(num_jobs: int, working_directory: str, programme: str, args: list):
    command = ["sbatch"]
    command += ["-p", "medium"]                 # select the partition (queue)
    command += ["-t", "180:00"]                  # maximum runtime
    command += ["--array=1-{}".format(num_jobs)]  # make this a job array
    command += ["-C", "scratch"]                # request access to scratch2
    command += ["--chdir", working_directory]   # set working directory
    command += ["--output", outputdirectory+"%A_%a.out"]
    command += [programme] + args

    print(" ".join(command))
    subprocess.check_call(command)

sys.path.append('%s/scripts'%(codedirectory))
from addparam import addparam # Import function addparam for loading parameters from IparamTable.txt.
IparamTableFile = '%s/Models/%s/IparamTable.txt'%(codedirectory,model) # txt file for stimulus parameters

# commsubmit_joband for submitting jobs 
# queue_option = 'sbatch -p medium-fas --array=1:%d:1 -o %s'%(runs, outputdirectory, outputdirectory)
# programme = '%s/Models/%s/x86_64/special -python' %(codedirectory, model)
# script = '%s/runjobs/runme.py'%(codedirectory)
# command = queue_option + ' ' + programme + ' ' + script

for tau in (5, ): 
  for posNa in (20,): 
    for fr in (5,):
      param = {'tau':tau, 'fr':fr, 'posNa':posNa}
      param = addparam(param, IparamTableFile) # add thr, spthr, mean, std to param.
      param['T'] = 20000 # duration of model simulation for STA (ms)
      param['T_relax'] = 500 # duration of initial condition randomization (ms)
      param['rep'] = 50 # repetition number
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
      for i in range(1,runs+1):
        subprocess.call('mkdir -p ' + foldername + '/Series' + str(i) + '/', shell=True) 
      np.save(foldername+'/param.npy', param)        
      submit_job_array(runs, ".", "runme.sh", [model, "runme.py", foldername]) 
