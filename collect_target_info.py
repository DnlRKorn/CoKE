import csv
drugs = [] 
drugs = '''
Ipamorelin
   Tilmicosin
      Budipine
         Atazanavir
            Pentagastrin
               Indinavir
                  Vinblastine
                     Afimoxifene
                        Navitoclax
                           Venetoclax
Dibenzyl (carbonylbis{2,1-hydrazinediyl[(2S)-4-methyl-1-oxo-1,2-pentanediyl]})biscarbamate
(E)-(4S,6S)-8-METHYL-6-((S)-3-METHYL-2-{(S)-2-[(5-METHYL-ISOXAZOLE-3-CARBONYL)-AMINO]-PROPIONYLAMINO}-BUTYRYLAMINO)-5-OXO-4-((R)-2-OXO-PYRROLIDIN-3-YLMETHYL)-NON-2-ENOIC ACID BENZYL ESTER
Ruzasvir
N-{[2-({[1-(4-CARBOXYBUTANOYL)AMINO]-2-PHENYLETHYL}-HYDROXYPHOSPHINYL)OXY]ACETYL}-2-PHENYLETHYLAMINE
Ipamorelin
Amitriptylinoxide
ETC-588
GI-181771X
Sufugolix
Rifalazil
Tilmicosin
N2-[(Benzyloxy)carbonyl]-N-[(3R)-1-{N-[(benzyloxy)carbonyl]-L-leucyl}-4-oxo-3-pyrrolidinyl]-L-leucinamide
RU82209
Budipine
L-756423
(S)-2-((S)-3-isobutyl-2,5-dioxo-4-quinolin-3-ylmethyl-[1,4]diazepan-1yl)-N-methyl-3-naphtalen-2-yl-propionamide
Arylomycin A2
Inhibitor Bea322
Atazanavir
Difelikefalin
Inhibitor Bea428
CR665
Elexacaftor
Pentagastrin
Indinavir
(R)-carnitinyl-CoA betaine
Myristoyl-Coa
Vinblastine
Afimoxifene
4-[(10s,14s,18s)-18-(2-Amino-2-Oxoethyl)-14-(1-Naphthylmethyl)-8,17,20-Trioxo-7,16,19-Triazaspiro[5.14]Icos-11-En-10-Yl]Benzylphosphonic Acid
TOP-1288
Navitoclax
Cenicriviroc
3''-(Beta-Chloroethyl)-2'',4''-Dioxo-3, 5''-Spiro-Oxazolidino-4-Deacetoxy-Vinblastine
3,8-Diamino-6-Phenyl-5-[6-[1-[2-[(1,2,3,4-Tetrahydro-9-Acridinyl)Amino]Ethyl]-1h-1,2,3-Triazol-5-Yl]Hexyl]-Phenanthridinium
MK-6325
Venetoclax
Gantacurium
OXIMINOARYLSULFONAMIDE
Proglumetacin
Barasertib
Lurbinectedin

                           '''
l = []
for x in drugs.split("\n"):
  if(len(x.strip())>2):
    l.append(x.strip().lower())
print(l)
l = set(l)

l2 = []
with open("structure_links.csv") as f:
  reader = csv.DictReader(f)
  for d in reader:
    chem = d['ChEMBL ID'].strip()
    name = d["Name"].strip().lower()
    bank = d["DrugBank ID"]
    if(len(chem)<2):continue
    if(name in l):
      print("%s|%s|%s"%(name,chem,bank))
      l2.append(name)
print(len(l2),len(l))
exit()
bank_ids_to_uni = {}

for x in bank_ids:
  bank_ids_to_uni[x] = set()

with open("uniprot_links.csv") as f:
  reader = csv.DictReader(f)
  for d in reader:
    bank = d["DrugBank ID"]
    if(bank in bank_ids):
      s = bank_ids_to_uni[bank]
      s.add(d["UniProt ID"])
      bank_ids_to_uni[bank] = s

for x in bank_ids_to_uni:
  print(x,len(bank_ids_to_uni[x]))

with open("structure_links.csv") as f, open("structure_links_filtered.csv",'w') as f2:
  #header = next(f)
  reader = csv.DictReader(f)
  fields = reader.fieldnames
  fields.append("Targets")
#  writer = csv.DictWriter(f2,reader.fieldnames)
  writer = csv.DictWriter(f2,fields)
  writer.writeheader()
  for d in reader:
    #chem = line.split(",")[13].strip()
    chem = d['ChEMBL ID'].strip()
    if(chem in inter):
      targs = len(bank_ids_to_uni[d["DrugBank ID"]])
      d["Targets"] = targs 
      writer.writerow(d)
    #  f2.write(line)
