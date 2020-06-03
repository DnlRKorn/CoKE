human_proteins = set()
corona_proteins = set()

with open("data/human_proteins.tsv") as f:
  next(f)
  for line in f:
    prot_idx = line.split('\t')[0]
    human_proteins.add(prot_idx)

with open("data/corona_virus_proteins.tsv") as f:
  next(f)
  for line in f:
    prot_idx = line.split('\t')[0]
    corona_proteins.add(prot_idx)


prot_idxs = set()

with open('data/pair_counts_dtd_1_2.txt') as f:
  for line in f:
    targ = line.split(',')[0]
    prot_idx = targ.split('#')[1]
    if(prot_idx not in human_proteins and prot_idx not in corona_proteins):
      raise ValueError("The follow ID is not present in the UniProt human or corona virus datasets", prot_idx)


