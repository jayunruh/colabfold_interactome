import pandas as pd
import glob
import argparse
import os

def main():
    '''
    maps MSA file names to ids from a fasta file
    '''
    parser = argparse.ArgumentParser(description='maps MSA file names to ids from a fasta file')
    parser.add_argument('--fastafile', help='path to fasta file', required=True)
    parser.add_argument('--msadir', help='path to directory with MSA files', required=True)
    args = parser.parse_args()
    #get the list of fasta files
    fastadf = readFASTA(args.fastafile)
    print(fastadf.head())
    #get the list of MSA files
    msas = sorted(glob.glob(args.msadir + '/*.a3m'))
    #map the MSA file names to the fasta ids
    for i in range(len(msas)):
        print(msas[i].split('/')[-1])
        idx=msas[i].split('/')[-1].split('.')[0]
        name=fastadf.loc[int(idx), 'id']
        os.rename(msas[i], args.msadir + '/' + name +'_'+ str(idx)+'.a3m')

def readFASTA(path):
    '''
    reads a fasta file and returns a data frame of ids and sequences
    '''
    with open(path) as f:
        lines=f.readlines()

    #clean things up but removing comments and stripping out whitespace
    lines=[lines[i].strip() for i in range(len(lines)) if (not lines[i].startswith('#'))]
    currid=''
    currseq=''
    ids=[]
    seqs=[]
    for i in range(len(lines)):
        if(lines[i].startswith('>')):
            if(currid==''):
                currid=lines[i][1:]
            else:
                ids.append(currid)
                currid=lines[i][1:]
                seqs.append(currseq)
                currseq=''
        else:
            currseq+=lines[i]
    seqs.append(currseq)
    ids.append(currid)
    return pd.DataFrame({'id':ids,'sequence':seqs})

if __name__ == '__main__':
    main()
