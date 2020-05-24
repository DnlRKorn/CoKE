from scipy.stats import hypergeom
import sys

total_sentence_count = 51859
#Doc count 29275

fname = sys.argv[1]
outfname = fname.split(".")[0] + "_scored.txt"
cnt = 0
#with open('advanced_pair_counts.txt','r') as inf, open('advanced_pair_counts_scored.txt','w') as outf:
with open(fname,'r') as inf, open(outfname,'w') as outf:
#    header = inf.readline().strip()
#    outf.write(header)
    outf.write(f'term1,term2,count1,count2,overlap,score,papers\n')
    for line in inf:
        parts = line.strip().split(',')
        Term1 = parts[0]
        Term2 = parts[1]
        CountTerm1 = int(parts[2])
        CountTerm2 = int(parts[3])
        SharedCount = int(parts[4])
        # The hypergeometric distribution models drawing objects from a bin.
        # For co-occurence, suppose that the number papers with the first term is the number of draws (ndraws)
        # And the total number of papers is total_paper_count, representing how many things could be drawn from (M)
        # Then number of papers with term 2 (n) is total number of Type I objects.
        # The random variate(x) represents the number of Type I objects in N drawn (the number of papers with both)
        #  without replacement from the total population (len curies).
        enrichp = hypergeom.logcdf(SharedCount - 1, total_sentence_count, CountTerm2, CountTerm1)
        #parts.append(str(enrichp))
        parts.insert(5,str(enrichp))
        outf.write(','.join(parts))
        outf.write('\n')
        
        if(cnt%1000==0):
          print(cnt)
          print("Term1",Term1,"Term2",Term2,"count 1",CountTerm1,"count 2",CountTerm2,"Shared",SharedCount,"score",enrichp)
        cnt+=1
