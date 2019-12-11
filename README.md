# How to Run Brette Code on GWDG clusters

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
