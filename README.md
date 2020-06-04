# CoKE
Covid Knowledge Extractor


The code is organized to help work through the filtering process of the CORD-19 annotations from SciBiteAI. Each step relies on the previous script in the process having been completed.

Setup:

The following files must be place in the directory data.

<b>cv19_scc.tsv</b>: This is the sentence level co-occurrence annotations from SciBiteAI. Please download from here https://github.com/SciBiteLabs/CORD19. Under <b>sentence-co-occurrence-CORD-19</b>, please select the latest version of the dataset.

<b>structure_links.csv</b>: This file contains data on all chemicals in DrugBank. It is available here https://www.drugbank.ca/releases/5-1-6/downloads/all-structure-links. To enable downloading, a free DrugBank account must be created.

<b>uniprot_links.csv</b>: This is a file from drugbank which describes all DrugBank -> UniProt target ids. Please download from here https://www.drugbank.ca/releases/latest#external-links. Under <b>Target Drug-UniProt Links</b>, Drug Group "All"

<b>human_proteins.tsv</b>: This file comes from UniProt and contains a hand reviewed list of all human proteins. The database may be inspected here https://www.uniprot.org/uniprot/?query=reviewed:yes%20taxonomy:9606, for convience and to keep parameters we suggest running the cURL command below

curl 'https://www.uniprot.org/uniprot/?query=reviewed:yes%20taxonomy:9606&format=tab&force=true&columns=id,entry%20name,reviewed,protein%20names,genes,organism,length&compress=yes'   --compressed > human_proteins.tsv.gz

<b>corona_virus_proteins.tsv</b>: This file comes from UniProt and contains a hand reviewed list of all Corona Virus viral proteins. The database may be inspected here https://www.uniprot.org/uniprot/?query=reviewed:yes%20taxonomy:694009, for convience and to keep parameters we suggest running the cURL command below

curl 'https://www.uniprot.org/uniprot/?query=reviewed:yes%20taxonomy:694009&format=tab&force=true&columns=id,entry%20name,reviewed,protein%20names,genes,organism,length&compress=yes'   --compressed > corona_virus_proteins.tsv.gz
