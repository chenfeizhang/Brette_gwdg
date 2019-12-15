# How to Calculate the Dynamic Gain Function of Brette's Model on GWDG Clusters
The Python code here simulates a simple multi-compartment model proposed by [Brette 2013](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003338) and calculates its dynamic gain functions.

We first provide a procedure to determine the axonal voltages for spike time detection and voltage reset to finish a spike. We then provide a parameter searching procedure to determine the mean and the std of the stochastic stimulus such that the neuron model realizes the expected firing rate and the coefficient of variation (CV) of inter-spike intervals (ISI) distribution. Thirdly, we implement the method proposed by [Higgs et al. 2009](http://www.jneurosci.org/content/29/5/1285.long) to calculate the dynamic gain functions of the neuron model and examine the impact of neuron morphology, spike initiation dynamics and stimulus properties on population encoding. In the last part, we provide a procedure for calculating bootstrapping confidence intervals and null hypothesis test curves. 

## Log in the frontend and set up the virtual environment of Python with NEURON
### How to log in the frontend gwdg101 (or gwdg102, gwdg103):
1. ```ssh -X username@gwdu101.gwdg.de```
Here ``username`` is your gwdg account name.
### How to use conda to install Python with NEURON as a package:
1. ```module load conda```
2. ```conda create --prefix /scratch/username/nrn -c conda-forge python gcc_linux-64 neuron```
Here ```/scratch/username/nrn``` is the directory of the virtual environment.
### How to activate Python with NEURON on gwdu101:
1. ```module load conda```
2. ```source activate /scratch/username/nrn```
### How to install python packages in the virtual environment:
1. Make sure you have activated the virtual environment (see above). 
2. ```conda install scipy``` (pip is not recommended.)
### How to use interactive queue (log in to one node and run simulations):
1. ```srun --pty -p medium -N 1 -c 1 /bin/bash```

## Simulate Brette's Model on GWDG Clusters
Download the code folder ``Code_gwdg`` to your home directory.
### 1. Activate the virtual environment and compile the neuron model
1. Activate the virtual environment.
2. Go to the model directroy ```cd ~/Code_gwdg/Models/Brette```. Compile the model with the command ```nrnivmodl```, then you will get the folde ``x86_64``. If you get the code from somewhere else, the folde ``x86_64`` may already exist. Please delete the folder and compile the code to get your own folder``x86_64``.

### Note: All the following steps are executed in the virtual environment. 

### 2. Determine the Axonal Voltages for Spike Time Dectection and Voltage Reset and Determine the Mean and the Std of Stimulus to Realize Target Firing Rate and CV of ISI Distribution.

Brette's model is a simple multi-compartment model composed of a soma and an axon. Only sodium channels are located at point on the axon for spike generation (AP initiation site). The rest of the neuron model is passive. To finish a spike, the voltage values of the whole neuron model need to be reset by hand when the axonal voltage at the AP initiation site reaches some specific value. We call this value reset threshold. We choose the axonal voltage with the maximum voltage derivative for spike time dectection. We choose the axonal voltage 2ms after the spike detection voltage as the reset voltage.

In ```~/Code_gwdg/Paramters```, ``param_step1_runjobs.py`` calls ``param_step1_runme.py`` to find the constant input that is about to trigger spikes and the constant input that generates 5Hz firing rate. To find targer stimuli, we set the upper bound and lower bound of the stimuli by hand, and use middle point searching method. ``firingonset.py`` in ```~/Code_gwdg/scripts``` contains the function that implements this searching method. When the upper bound and lower bound are close enough, we assume the parameter searching is precise enough. The programme will stop and return the constant input value and the final reset threshold for later simulation.
    
To find target mean and std of stimulus, ``param_step2_runjobs.py`` calls ``param_step2_runme.py`` for parameter searching. In this step, it picks 200 mean values between zero and the constant input of 5Hz firing, and uses midde point searching method to find correponding std to generate 5Hz firing. ``Determinestd.py`` in ```~/Code_gwdg/scripts``` provides the function for std searching. param_step3.py summarizes the data. The mean and std that reproduce expected CV are determined by hand from the scatter plots of mean-std and mean-CV relation. Mean and std values are written in the txt file ``IparamTable.txt`` in ```~/Code_gwdg/Models/Brette```.

1. Go to direcotry ```~/Code_gwdg/Parameters```. ``model_simulation.py`` provides a function for model simulation and a function for stimulus generation. It also provides the self-test code to simulate the model. 

2. Set up the parameters in ``model_simulation.py`` in the self-test part. To determine the spike time dectection voltage, we first set the reset threshold ``threshold`` to 60mV. Then set ``stim_std`` to 0, and set ``stim_mean`` to a large enough value such that the axonal voltage is larger than -40mV but not larger than 60mV. The spike detection voltage is quite insensitive to the constant stimulus amplitude. Then type the following command in the terminal:
```
~/Code_gwdg/Models/Brette/x86_64/special -python model_simulation.py Brette
```
Here make sure the model name in the programme ``~/Code_gwdg/Models/Brette/x86_64/special -python`` is the same with the model being simulated (shown in the end).

With the spike detection voltage, the reset threshold is temporarily set to be slightly larger in following simulations. 

3. Use ``param_step1_runjobs.py``, ``param_step1_runme.py`` and ``runme.sh`` to submit jobs to the clusters and find the constant input that generates 5Hz firng rate and the constant input that is just to trigger spikes. In this step, the scripts also use the constant input that generates 5Hz firing rate to determine the reset threshold, and save the reset threshold to ``param.npy``.

In ``param_step1_runjobs.py``, set your hostname and the model name. Make sure you already have created your directory on ``/scratch``. You can also set your own data folder and output file folder. Then set the parameters of the stimulus and the neuron model. ``param_step1_runjobs.py`` calls ``param_step1_runjobs.py`` and ``runme.sh`` to run the simulation.

In ``param_step1_runme.py``, the script uses the function ``simulate`` and ``FiringOnset`` for parameter searching.

In ``runme.sh``, the script activates the virtual environment in the cluster node, and specifies the programme used for simulation. Please change the username in ``/scratch/username/nrn``

Type the following command to submit jobs:
```
python param_step1_runjobs.py
```
4. Use ``param_step2_runjobs.py``, ``param_step2_runme.py`` and ``runme.sh`` to submit jobs to the clusters and find the correponding std of stochastic stimulus for each mean stimulus, such that the average firing rate is 5Hz.

Set the hostname and model name in ``param_step2_runjobs.py``. In ``param_step2_runme.py``, one can set the range of mean values by hand if necessary.

Type the following command to submit jobs:
```
python param_step2_runjobs.py
```

5. Use ``param_step3.py`` to save the data generated in step 4 into one file and manually find the mean and std that reproduce target firing rate and firing pattern.

Type the following command to save the data:
```
python param_step3.py
```

6. Write the the mean and the std of stimulus manually into the txt file ``IparamTable.txt`` in ```~/Code_gwdg/Models/Brette```.

### 3. Calculate Dynamic Gain Functions.

Dynamic gain functions of Brette's model are calculated by the Fourier transform of spike triggered average (STA) divided by the power spetral density of stochastic stimulus. In ```~/Code_git/runjobs```, runjobs.py calls runme.py to generate 400 pieces of STA. Each piece of STA is an average of about 5000 pieces of stochastic stimuli centered at their spike times. The final STA of the dynamic gain function is an average of these 400 pieces of STA. ``addparam.py`` in ```~/Code_git/scripts``` provides the function for loading parameters from ``IparamTable.txt``. ``runjobs_desktop.py`` and ``runme_desktop.py`` provides a desktop version of the code. With these two script, one can generate a small fraction of STA data and obtain a preliminary linear response curve.

``transferit.py`` in ```~/Code_git/transferit``` provides the function ``STA_average`` for calculating the final STA and the function for calculating dynamic gain functions. STA_average is also used for averaging randomly sampled STA data to calculate bootstrapping confidence interval. In function gain, STA is first suppressed to zero at its two ends before Fourier transform. For Fourier transform, the STA is cut from the middle and attaches its two ends.  

1. Go to direcotry ```~/Code_gwdg/runjobs```. Use ``runjobs.py``, ``runme.py`` and ``runme.sh`` to submit jobs to the clusters and calculate 400 pieces of STA. Please change the hostname in ``runjobs.py`` and ``runme.sh``.

Type the following command to submit jobs:
```
python runjobs.py
```

Or type the following command to run small jobs on the desktop:
```
python runjobs_desktop.py
```

2. When the simulation in 1 is finished, go to direcotry ```~/Code_gwdg/transferit```. Use ``transferit.py`` to calculate the dynamic gain function.

Type the following command to calculate the dynamic gain function:
```
python transferit.py
```

### 4. Bootstrapping Confidence Interval and Null Hypothesis Test.

To calculate the bootstrapping confidence interval, ``bootstrapping_runjobs.py`` in ```~/Code_git/transferit/``` calls ``bootstrapping_runme.py``. In each job, it randomly samples 400 pieces of STA with replacement and averages them to get a new final STA. A new dynamic gain function is calculated with the new final STA. There are 1000 new curves generated in total. Bootstrapping boundaries are the upper bound and lower bound of middle 95 percent of these curves. ``bootstrapping_step2.py`` finds the boundary curves and writes them into the dynamic gain function data file.

1. Go to direcotry ```~/Code_gwdg/transferit```. Use ``bootstrapping_runjobs.py``, ``bootstrapping_runme.py`` and ``runme.sh`` to submit jobs to the clusters and calculate 1000 dynamic gain functions. Please change the hostname in ``bootstrapping_runjobs.py`` and ``runme.sh``.

Type the following command to submit jobs:
```
python bootstrapping_runjobs.py
```

2. When the simulation in 1 is finished, use ``bootstrapping_step2.py`` to calculate the bootstrapping confidence interval and save the data.

Type the following command to submit jobs:
```
python bootstrapping_step2.py
```

To calculate the null hypothesis test curve, ``nullhypothesis_runjobs.py`` in ```~/Code_git/transferit/``` calls ``nullhypothesis_runme.py``. In each job, it reproduces the stimuli and loads corresponding spike time lists. Adding a different random number to each spike time list shuffles spike times. STA data are calculated with the stimuli and new spike time lists. ``nullhypothesis_step2_runjobs.py`` calls ``nullhypothesis_step2_runme.py`` to calculate dynamic gain functions with these STA data. ``nullhypothesis_step3.py`` takes the 95 percent upper bound of these curves as the final null hypothesis test curve and writes it into the dynamic gain function data file.

1. Use ``nullhypothesis_runjobs.py``, ``nullhypothesis_runme.py`` and ``runme.sh`` to submit jobs to the clusters and calculate STA generated by shuffled spike times. Please change the hostname in ``nullhypothesis_runjobs.py`` and ``runme.sh``.

Type the following command to submit jobs:
```
python nullhypothesis_runjobs.py
```

2. When the simulation in 1 is finished, use ``nullhypothesis_step2_runjobs.py``, ``nullhypothesis_step2_runme.py`` and ``runme_step2.sh`` to submit jobs to the clusters and calculate "dynamic gain functions". Please change the hostname in ``nullhypothesis_step2_runjobs.py`` and ``runme_step2.sh``.

Type the following command to submit jobs:
```
python nullhypothesis_step2_runjobs.py
```

3. When the simulation in 2 is finished, use ``nullhypothesis_step3.py`` to calculate the null hypothesis curve and save the data.

Type the following command to submit jobs:
```
python bootstrapping_step3.py
```
