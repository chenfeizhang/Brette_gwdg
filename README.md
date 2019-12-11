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

### 2. Determine the Axonal Voltages for Spike Time Dectection and Voltage Reset

Brette's model is a simple multi-compartment model composed of a soma and an axon. Only sodium channels are located at point on the axon for spike generation (AP initiation site). The rest of the neuron model is passive. To finish a spike, the voltage values of the whole neuron model need to be reset by hand when the axonal voltage at the AP initiation site reaches some specific value. We call this value reset threshold. We choose the axonal voltage with the maximum voltage derivative for spike time dectection. We choose the axonal voltage 2ms after the spike detection voltage as the reset voltage.

1. Go to direcotry ```~/Code_git/Parameters```. ``model_simulation.py`` provides a function for model simulation and a function for stimulus generation. It also provides the self-test code to simulate the model. 

2. Set up the parameters in ``model_simulation.py`` in the self-test part. To determine the spike time dectection voltage, we first set the reset threshold ``threshold`` to 60mV. Then set ``stim_std`` to 0, and set ``stim_mean`` to a large enough value such that the axonal voltage is larger than -40mV but not larger than 60mV. The spike detection voltage is quite insensitive to the constant stimulus amplitude. Then type the following command in the terminal:
```
~/Code_git/Models/Brette/x86_64/special -python model_simulation.py Brette
```
Here make sure the model name in the programme ``~/Code_git/Models/Brette/x86_64/special -python`` is the same with the model being simulated (shown in the end).

With the spike detection voltage, the reset threshold is temporarily set to be slightly larger in following simulations.

3. Use ``param_step1_runjobs.py``, ``param_step2_runme.py`` and ``runme.sh`` to submit jobs to the clusters and find the constant input that generates 5Hz firng rate and the constant input that is just to trigger spikes. In this step, the scripts also use the constant input that generates 5Hz firing rate to determine the reset threshold, and save the reset threshold to ``param.npy``.

In ``param_step1_runjobs.py``, set your hostname and the model name. Make sure you already have created your directory on ``/scratch``. You can also set your own data folder and output file folder. 

Type the following command to submit jobs:
```
python param_step1_runjobs.py
```

