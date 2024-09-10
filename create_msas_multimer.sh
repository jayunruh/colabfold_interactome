#!/bin/bash
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=100G
#SBATCH --time=24:00:00
#SBATCH --output=create_msa_multimer.log
#SBATCH --error=create_msa_multimer.err
#SBATCH --cpus-per-task=16
#

module load python
python create_msas_multimer.py --msa1_dir query_msas/ --msa2_dir bait_msas/ --out_dir interaction_msas/ --max_folder_msas 500
#optional version to limit the size of the msas to 4096
#python create_msas_multimer.py --msa1_dir query_msas/ --msa2_dir bait_msas/ --out_dir interaction_msas/ --limitlen 4096 --max_folder_msas 500
