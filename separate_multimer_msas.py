import glob
import os
import argparse

#parse the folder name we want to split
parser = argparse.ArgumentParser(description='Split a folder of multimer msas into subfolders by peptide')
parser.add_argument('--dir', type=str ,help='the directory of the folder to split')
args = parser.parse_args()
prefix = args.dir
#get all the files in the directory
files = glob.glob(prefix+"*.a3m")
#get the peptide names
peptides = [file.split('/')[-1].split("_")[0] for file in files]
#get the unique peptide names
peptides = list(set(peptides))
print(peptides)
#for each peptide make a sub directory and move the files into it
for peptide in peptides:
    print(peptide)
    #make the sub directory
    os.mkdir(prefix + peptide)
    os.makedirs(prefix + peptide,exist_ok=True)
    #move the files into it
    os.system("mv "+prefix + peptide + "_*.a3m "+prefix + peptide + "/")
