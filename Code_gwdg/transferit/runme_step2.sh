#! /bin/bash
hostname
module load conda
source activate /scratch/chenfei/nrn
CODEDIR=${HOME}/Code_gwdg
python $2 $3 $4

