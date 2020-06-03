from scipy.stats import hypergeom
import csv
import os

csv.field_size_limit(100000000)

data_dir = os.path.join(os.path.dirname(os.getcwd()),"data")

with open(os.path.join(data_dir,"filtered_papers_cnt.txt"),'r') as f:
    total_paper_count = int(f.read())


fname = os.path.join(data_dir,"CORD19_co-occurrence_pairs.csv")
outfname = os.path.join(data_dir,"CORD19_co-occurrence_pairs_scored.csv")

cnt = 0
with open(fname,'r') as inf, open(outfname,'w') as outf:
    reader = csv.DictReader(inf)
    writer = csv.DictWriter(outf,['Term1', 'Term2', 'Term1Cnt', 'Term2Cnt', 'Co-occurrenceCnt','Score','Papers'])
    writer.writeheader()
    for d in reader:
        CountTerm1 = int(d['Term1Cnt'])
        CountTerm2 = int(d['Term2Cnt'])
        SharedCount = int(d['Co-occurrenceCnt'])
        if(CountTerm1 < SharedCount or CountTerm2 < SharedCount):raise ValueError("Size of shared count larger then terms",d)
        # The hypergeometric distribution models drawing objects from a bin.
        # For co-occurence, suppose that the number papers with the first term is the number of draws (ndraws)
        # And the total number of papers is total_paper_count, representing how many things could be drawn from (M)
        # Then number of papers with term 2 (n) is total number of Type I objects.
        # The random variate(x) represents the number of Type I objects in N drawn (the number of papers with both)
        #  without replacement from the total population (len curies).
        enrichp = hypergeom.logcdf(SharedCount - 1, total_paper_count, CountTerm2, CountTerm1)
        d['Score'] = enrichp
        writer.writerow(d)
        cnt+=1 
        if(cnt%10000==0):
            print(cnt,d)
