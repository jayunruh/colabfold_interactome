#!/bin/bash
#SBATCH --partition gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=64GB
#SBATCH --time=2-00:00
#SBATCH --gres=gpu:a100:1
#change the last array number to the number of queries and %# for the number of GPU's to use
#SBATCH --array=1-3%1
#SBATCH --output=colabfold_msa_multimer_%A_%a.log
#SBATCH --error=colabfold_msa_multimer_%A_%a.err

querylist=("query1" "query2" "query3")
module load colabfold
#the code below will get run for every job in the array list
selidx=$SLURM_ARRAY_TASK_ID-1
echo "Running ${querylist[$selidx]}"
colabfold_batch --model-type alphafold2_multimer_v3 --num-models 1 --num-recycle 3 interaction_msas/${querylist[$selidx]} outputdir_multimer_msas/${querylist[$selidx]}/
