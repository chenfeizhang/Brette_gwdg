'''

Calculate null hypothesis test curve.

This file calls nullhypothesis_runme.py. For each series folder, reproduce the stimuli that generate spikes for each simulation duration T in runme.py. Load corresponding spike times in T, add a random number to all spike times and mod them by T. In this way, the spike times are shuffled, but the spiking pattern (CV of ISI) is kept. Calculate STA and linear response curve with shuffled spike times. Repeat this procedure 500 times to get 500 linear response curves. Final null hypothesis test curve is the 95 percent upper bound of these curves. Reducing the repetition time to 100 provides a similar result, except that the curve is more noisy.

In figures of our paper, only the linear response curves above the null hypothesis test curves are shown. Null hypothesis test curves are not shown.

'''
import subprocess
from subprocess import call

hostname = 'chenfei'
model = 'Brette'
runs = 400 # number of series folders
codedirectory = '..'
datafolder = '/scratch/%s/%s/'%(hostname,model)
outputdirectory = '%sOutput/'%(datafolder)

def submit_job_array(num_jobs: int, working_directory: str, programme: str, args: list):
    command = ["sbatch"]
    command += ["-p", "medium"]                 # select the partition (queue)
    command += ["-t", "300:00"]                  # maximum runtime
    command += ["--array=1-{}".format(num_jobs)]  # make this a job array
    command += ["-C", "scratch"]                # request access to scratch2
    command += ["--chdir", working_directory]   # set working directory
    command += ["--output", outputdirectory+"%A_%a.out"]
    command += [programme] + args

    print(" ".join(command))
    subprocess.check_call(command)
 
for tau in (5,): #  
    for (thr,posNa) in ((-23, 20),): # 
      f = 5 
      appendix = 'tau%dfr%dthreshold%dposNa%d'%(tau, f, thr, posNa)
      foldername = datafolder + appendix
      submit_job_array(runs, ".", "runme.sh", [model, "nullhypothesis_runme.py", foldername])
