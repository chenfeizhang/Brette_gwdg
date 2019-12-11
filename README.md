# Brette Code Run on GWDG clusters
Brette code run on gwdg hpc clusters
How to login HPC cluster:
1. ssh -X zhang38@login.gwdg.de
2. ssh gwdu101.gwdg.de
or simply: ssh -X zhang38@gwdu101.gwdg.de

How to install NEURON with Python using conda:
0. module load conda
1. conda install -c conda-forge neuron 
2. conda install gcc_linux-64
Shortcut: conda create --prefix /scratch/chenfei/nrn -c conda-forge python=3.6 gcc_linux-64 neuron

How to activate NEURON with Python on frontend:
1. module load conda
2. source activate /scratch/chenfei/nrn

How to install python package in virtual environment:
1. conda install scipy (pip is not recommended.)

How to login to one node and test your code (interactive queue):
srun --pty -p medium -N 1 -c 1 /bin/bash 
srun --x11 -p medium xterm
attention: copy paste the command above may have ‘--’ become ‘-’ in the terminal
