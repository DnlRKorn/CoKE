import os

data_dir = os.path.join(os.path.dirname(os.getcwd()),"data")

fname = os.path.join(data_dir,"CORD19_co-occurrence_pairs_scored.csv")
outfname = os.path.join(data_dir,"CORD19_co-occurrence_pairs_scored_filtered.csv")

cnt=0
total_cnt=0
with open(fname,'r') as f, open(outfname,'w') as outf:
    header = next(f)
    outf.write(header)
    for line in f:
        total_cnt+=1
        x = line.split(',')[0]
        y = line.split(',')[1]
        if( "CVPROT#" in x and "DRUG#" in y ):
            outf.write(line)
            cnt+=1

print("We read in %d tuples." % total_cnt)
print("We have %d tuples after filtering for protein/drug relationships!" % cnt)
