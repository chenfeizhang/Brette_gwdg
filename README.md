# How to Calculate the Dynamic Gain Function of Brette's Model on GWDG Clusters
The Python code here simulates a simple multi-compartment model proposed by [Brette 2013](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003338) and calculates its dynamic gain functions.

We first provide a procedure to determine the axonal voltages for spike time detection and voltage reset to finish a spike. We then provide a parameter searching procedure to determine the mean and the std of the stochastic stimulus such that the neuron model realizes the expected firing rate and the coefficient of variation (CV) of inter-spike intervals (ISI) distribution. Thirdly, we implement the method proposed by [Higgs et al. 2009](http://www.jneurosci.org/content/29/5/1285.long) to calculate the dynamic gain functions of the neuron model and examine the impact of neuron morphology, spike initiation dynamics and stimulus properties on population encoding. In the last part, we provide a procedure for calculating bootstrapping confidence intervals and null hypothesis test curves. 

## Log in the frontend and set up the virtual environment of Python with NEURON
### How to log in the frontend gwdg101 (or gwdg102, gwdg103):
1. ```ssh -X username@gwdu101.gwdg.de```
Here username is your gwdg account name.
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

## Run Brette code on GWDG clusters
Download the code folder ``Code_gwdg`` into your home directory
### Activate the virtual environment and compile the neuron model
1. Activate the virtual environment.
2. Go to the model directroy ```cd ~/Code_gwdg/Models/Brette```. Compile the model with the command ```nrnivmodl```, then you will get the folde ``x86_64``. If you get the code from somewhere else, the folde ``x86_64`` may already exist. Please delete the folder and compile the code to get your own folder``x86_64``.

### 
