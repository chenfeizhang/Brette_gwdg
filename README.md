# Brette Code Run on GWDG clusters


## How to login HPC cluster:
ssh -X username@gwdu101.gwdg.de

## How to install NEURON with Python using conda:
1. module load conda
2. conda create --prefix /scratch/username/nrn -c conda-forge python gcc_linux-64 neuron

## How to activate NEURON with Python on gwdu101:
1. module load conda
2. source activate /scratch/chenfei/nrn

## How to install python package in virtual environment:
1. Make sure you have activated the virtual environment (see above). 
2. conda install scipy (pip is not recommended.)

## How to login to one node and test your code (interactive queue):
1. srun --pty -p medium -N 1 -c 1 /bin/bash
