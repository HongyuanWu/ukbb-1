#identifies snp's below a p-value in discovery and replication cohort.
import argparse
from os import listdir
from os.path import isfile,join

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("--discovery_dir")
    parser.add_argument("--replication_dir")
    parser.add_argument("--pval_discovery_thresh",type=float,default=5e-8)
    parser.add_argument("--pval_validation_thresh",type=float,default=0.01) 
    parser.add_argument("--outf")
    parser.add_argument("--bidirectional",action='store_true',default=False) 
    return parser.parse_args()

def main():
    args=parse_args()
    discovery_features=[f for f in listdir(args.discovery_dir)]
    outf_summary=open(args.outf+"."+"summary",'w')
    for feature in discovery_features:
        outf=open(args.outf+"."+feature,'w')
        for chrom in range(1,23):
            discovery_dict=dict()
            cur_file=open(args.discovery_dir+'/'+feature+'/'+feature+'.'+str(chrom)+'.'+'continuous.assoc.linear').read().strip().split('\n')
            for line in cur_file[1::]:
                tokens=line.split()
                if len(tokens)<3:
                    print(str(tokens))
                    continue 
                pval=tokens[-1]
                try:
                    pval=float(pval)
                except:
                    continue 
                rs=tokens[1]
                if pval<=args.pval_discovery_thresh:
                    discovery_dict[rs]=tokens
            print("finished discovery set for chrom:"+str(chrom))
            replication_dict=dict()
            if args.replication_dir!=None: 
                cur_file=open(args.replication_dir+'/'+feature+'/'+feature+'.'+str(chrom)+'.'+'continuous.assoc.linear').read().strip().split('\n')
                for line in cur_file[1::]:
                    tokens=line.split()
                    if len(tokens)<3:
                        print(str(tokens))
                        continue 
                    pval=tokens[-1]
                    try:
                        pval=float(pval)
                    except:
                        continue 
                    rs=tokens[1]
                    if pval<=args.pval_validation_thresh:
                        replication_dict[rs]=tokens
                print("finished replication set for chrom:"+str(chrom))
            num_discovered=0
            num_replicated=0
            if args.bidirectional==True: 
                num_new=0 
            for snp in discovery_dict:
                num_discovered+=1
                outf.write('\t'.join(discovery_dict[snp]))
                if snp in replication_dict:
                    num_replicated+=1
                    outf.write('\t'+'\t'.join(replication_dict[snp]))
                outf.write('\n')
            if args.bidirectional==True:
                if len(discovery_dict.values())>0: 
                    num_to_skip=len(discovery_dict.values()[0])
                else:
                    num_to_skip=9 
                for snp in replication_dict:
                    if snp not in discovery_dict:
                        snp_pval=float(replication_dict[snp][-1])
                        if snp_pval <= args.pval_discovery_thresh:
                            outf.write('\t'*num_to_skip+'\t'.join(replication_dict[snp])+'\n')
                            num_new+=1 
            outf_summary.write(feature+'\t'+str(chrom)+'\t'+str(num_discovered)+'\t'+str(num_replicated))
            if args.bidirectional==True:
                outf_summary.write('\t'+str(num_new))
            outf_summary.write('\n')
            
if __name__=="__main__":
    main()
    
