#! /bin/bash
hostname
module load conda
source activate /scratch/chenfei/nrn
CODEDIR=${HOME}/Code_gwdg
${CODEDIR}/Models/$1/x86_64/special -python $2 $3

