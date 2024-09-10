import pandas as pd
import numpy as np
import sys
#change this to the location of pdbtools on your system
sys.path.append('/n/projects/jru/public/IPython_Notebooks/pdbtools/')
import jpdbtools2 as jpt
import glob
import os
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor

def makeAFmsa2(msa1,msa2,limitlen=-1):
    '''
    this takes two msa dataframes and merges them into a single msa
    the first line has #len1,len2\t1,1 (don't output that)
    the first dataframe id is >101\t102 with the two sequences pasted together
    then we paste the first msa with padding
    then we paste the second msa with pre-padding
    if limitlen is >0 then we limit the length of the msa
    returns a dataframe with the new msa and the lengths of the two sequences
    '''
    #let's make the assumption that the msa headers are unchanged
    #also assume that the msa's are from monomers (no padding)
    len1=len(msa1.loc[0,'sequence'])
    len2=len(msa2.loc[0,'sequence'])
    totlen=len1+len2
    padding1=''.join(['-']*len2)
    padding2=''.join(['-']*len1)
    #make a copy of the first msa
    #optionally limit the length of the msa list
    if(limitlen>0 and len(msa1)>limitlen):
        outmsa=msa1.iloc[:limitlen].copy()
        #if we decide to randomly sample (takes longer)
        #outmsa=msa1.sample(n=limitlen,axis=0).reset_index(drop=True)
    else:
        outmsa=msa1.copy()
    #append the padding
    outmsa.loc[:,'sequence']=outmsa.loc[:,'sequence']+padding1
    #prepend the first line in the dataframe
    outmsa=pd.concat([pd.DataFrame({'id':'101\t102','sequence':msa1.loc[0,'sequence']+msa2.loc[0,'sequence']},index=[0]),outmsa])
    #append the second msa with padding
    #optionally limit the length of the msa list
    if(limitlen>0 and len(msa2)>limitlen):
        tmsa2=msa2.iloc[:limitlen].copy()
        #if we decide to randomly sample (takes longer)
        #tmsa2=msa2.sample(n=limitlen,axis=0).reset_index(drop=True)
    else:
        tmsa2=msa2.copy()
    tmsa2.loc[:,'sequence']=padding2+tmsa2.loc[:,'sequence']
    outmsa=pd.concat([outmsa,tmsa2])
    return outmsa,len1,len2

def writeAFmsa(fname,msadf,len1,len2):
    '''
    this writes an updated msa data frame to an a3m file
    inputs are filename, the msa dataframe, and the lengths of the two sequences
    '''
    msadf['id']='>'+msadf['id']
    outstr='\n'.join(msadf.values.flatten())
    with open(fname,'w') as f:
        f.write('#'+str(len1)+','+str(len2)+'\t1,1\n')
        f.write(outstr)
        #for i in range(len(msadf)):
        #    f.write('\n>'+msadf.iloc[i]['id'])
        #    f.write('\n'+msadf.iloc[i]['sequence'])

def analyzeFiles(msa1,file2,name1,name2,outdir,limitlen=-1):
    '''
    this function takes two msa files and makes a multimer msa
    inputs are the msa1 df, the msa2 file, the names of the two msas, and the output directory
    '''
    #load the first msa
    #msa1=jpt.getFASTA(file1)[0]
    #load the second msa
    msa2=jpt.getFASTA(file2)[0]
    #make the multimer msa
    designedmsa,len1,len2=makeAFmsa2(msa1,msa2,limitlen)
    #write the msa to file
    dname=name1+'_'+name2
    writeAFmsa(outdir+'/'+dname+'.a3m',designedmsa,len1,len2)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a set of multimer msas from two msa directories')
    parser.add_argument('--msa1_dir',type=str,required=True,help='directory of query msas')
    parser.add_argument('--msa2_dir',type=str,required=True,help='directory of target msas')
    parser.add_argument('--limitlen',type=int,default=-1,required=False,help='limit the length of the msas')
    parser.add_argument('--max_folder_msas',type=int,default=500,required=False,help='maximum number of msas in an output folder')
    parser.add_argument('--out_dir',type=str,required=True)
    args = parser.parse_args()
    #get the first set of msas
    msa1files=glob.glob(args.msa1_dir+'/*.a3m')
    #get the second set of msas
    msa2files=glob.glob(args.msa2_dir+'/*.a3m')
    #make the output directory if necessary
    os.makedirs(args.out_dir,exist_ok=True)
    limitlen=args.limitlen
    print('length limit is ',limitlen)
    #loop through the first set of msas
    for j in range(len(msa1files)):
        print('working on '+msa1files[j])
        #get the first sequence msa
        msa1=jpt.getFASTA(msa1files[j])[0]
        name1=msa1files[j].split('/')[-1].split('.')[0]
        with ThreadPoolExecutor(max_workers=16) as executor:
            for i in range(len(msa2files)):
                outdir2=args.out_dir+'/'+name1+'_'+str(i//args.max_folder_msas)
                os.makedirs(outdir2,exist_ok=True)
                name2=msa2files[i].split('/')[-1].split('.')[0]
                dname=name1+'_'+name2 #make the name of the output file
                if(i%100==0):
                    print('file ',i,' of ',len(msa2files))
                if not os.path.exists(outdir2+'/'+dname+'.a3m'):
                    #make this multithreaded
                    executor.submit(analyzeFiles,msa1,msa2files[i],name1,name2,outdir2,limitlen)
