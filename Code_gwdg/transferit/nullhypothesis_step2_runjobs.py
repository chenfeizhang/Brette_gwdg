'''

This file calls nullhypothesis_step2_runme.py. Take shuffled STAs from series folders, calculate linear response curves for null hypothesis test.

'''

import os
import subprocess
from subprocess import call

# model name, code directory and data directory
hostname = 'chenfei'
model = 'Brette'
runs = 100 # null hypothesis runs
codedirectory = '..'
datafolder = '/scratch/%s/%s/'%(hostname, model)
outputdirectory = '%sOutput/'%(datafolder)

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

for tau in (5,): 
  for (thr,posNa) in ((-23,20),): 
    for fr in (5, ): 
      appendix = 'tau%sfr%sthreshold%sposNa%s'%(tau, fr, thr, posNa)
      foldername = datafolder + appendix
      if os.path.isdir(foldername+'/nullhypothesis') == False:
        os.mkdir(foldername+'/nullhypothesis')
      submit_job_array(runs, ".", "runme_step2.sh", [model, "nullhypothesis_step2_runme.py", appendix, datafolder])

