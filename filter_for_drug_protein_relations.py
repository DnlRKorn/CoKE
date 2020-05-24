import sys
if(len(sys.argv)==1):
  fname = "CORD19_co-occurrence_pairs.csv.txt"
else:
  fname = sys.argv[1]
with open(fname) as f:
  for line in f:
    x = line.split(',')[0]
    y = line.split(',')[1]
    if( ("CVPROT#" in x and "DRUG#" in y) or ("CVPROT#" in y and "DRUG#" in x)):
      sys.stdout.write(line)
