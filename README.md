# CoKE
Covid Knowledge Extractor


The code is organized to help work through the filtering process of the CORD-19 annotations from SciBiteAI. Each step relies on the previous script in the process having been completed.

Setup:

The following files must be place in data.

cv19_scc.tsv: This is the sentence level co-occurrence annotations from SciBiteAI. Please download from here https://github.com/SciBiteLabs/CORD19. Under <b>sentence-co-occurrence-CORD-19</b>, please select the latest version of the dataset.

uniprot_links: This is a file from drugbank which describes all DrugBank -> UniProt target ids. Please download from here https://www.drugbank.ca/releases/latest#external-links. Under <b>Target Drug-UniProt Links</b>, Drug Group "All"

