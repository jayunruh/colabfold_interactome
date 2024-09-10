#!/bin/bash
#SBATCH --partition compute
#SBATCH --cpus-per-task=70
#SBATCH --mem=680GB
#SBATCH --nodes=1
#SBATCH --time=1-00:00
#SBATCH --output=run_mmseqs2.log
#SBATCH --error=run_mmseqs2.err

#change this to the colabfold database path on your file system
CFDBPATH=/n/data1/colabfold

#note that the msas folder needs to be executable here (chmod -R +x msas/)
module load colabfold
colabfold_search fasta_file.fa $CFDBPATH msas/
