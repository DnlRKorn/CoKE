# CoKE
Covid Knowledge Extractor


The code is organized to help work through the filtering process of the CORD-19 annotations from SciBiteAI. Each step relies on the previous script in the process having been completed.

Setup:

The following files must be place in the directory data.

<b>cv19_scc.tsv</b>: This is the sentence level co-occurrence annotations from SciBiteAI. Please download from here https://github.com/SciBiteLabs/CORD19. Under <b>sentence-co-occurrence-CORD-19</b>, please select the latest version of the dataset.

<b>structure_links.csv</b>: This file contains data on all chemicals in DrugBank. It is available here https://www.drugbank.ca/releases/5-1-6/downloads/all-structure-links. To enable downloading, a free DrugBank account must be created.

<b>DBCAT000021</b>:This is the website hosted https://www.drugbank.ca/categories/DBCAT000021 which contains a list of all amino acids currently in DrugBank.

<b>uniprot_links.csv</b>: This is a file from drugbank which describes all DrugBank -> UniProt target ids. Please download from here https://www.drugbank.ca/releases/latest#external-links. Under <b>Target Drug-UniProt Links</b>, Drug Group "All"

<b>human_proteins.tsv</b>: This file comes from UniProt and contains a hand reviewed list of all human proteins. The database may be inspected here https://www.uniprot.org/uniprot/?query=reviewed:yes%20taxonomy:9606, for convience and to keep parameters we suggest running the cURL command below

curl 'https://www.uniprot.org/uniprot/?query=reviewed:yes%20taxonomy:9606&format=tab&force=true&columns=id,entry%20name,reviewed,protein%20names,genes,organism,length&compress=yes'   --compressed > human_proteins.tsv.gz

<b>corona_virus_proteins.tsv</b>: This file comes from UniProt and contains a hand reviewed list of all Corona Virus viral proteins. The database may be inspected here https://www.uniprot.org/uniprot/?query=reviewed:yes%20taxonomy:694009, for convience and to keep parameters we suggest running the cURL command below

curl 'https://www.uniprot.org/uniprot/?query=reviewed:yes%20taxonomy:694009&format=tab&force=true&columns=id,entry%20name,reviewed,protein%20names,genes,organism,length&compress=yes'   --compressed > corona_virus_proteins.tsv.gz

<b>metadata.csv</b>: This file comes from Kaggle and contains metadata on all papers present in CORD19. https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge?select=metadata.csv.



Here are the different sections of the code:

<b>Step 1</b>: This step takes in cv19_scc.tsv and finds all papers in which a SARSCOV ontological tag is found. It then removes all papers without this tag. This filtered dataset is placed in data/cv19_scc_filtered_for_COVID.tsv.

<b>Step 2</b>: This step takes in cv19_scc_filtered_for_COVID.tsv and runs our co-occurrence algorithm against it. Once these co-occurrence counts are found they are placed in data/CORD19_co-occurrence_pairs.csv.

<b>Step 3</b>: This step takes in CORD19_co-occurrence_pairs.csv and runs our hypergeometric scoring algorithm against it. This then adds that as a column on the csv and outputs that to data/CORD19_co-occurrence_pairs_scored.csv

<b>Step 4</b>: This step takes in CORD19_co-occurrence_pairs_scored.csv and filters for any pairing which is not a protein->chemical relationship. This is then saved as data/CORD19_co-occurrence_pairs_scored_filtered.csv

<b>Step 5</b>: This step requires all of the DrugBank and UniProt files mentioned in setup to be placed in the data directory. It takes in CORD19_co-occurrence_pairs_scored_filtered.csv matches the UniProt identifiers and ChEMBL identifiers against those in the provided datasets, if a match is not found the pair will be removed. This is outputted in data/CORD19_co-occurrence_pairs_scored_filtered_db_uniprot.csv

<b>Step 6</b>: This step generates csvs of all pair information to be downloaded by the users of the site. It also calculates number of known drug targets for a specific compound, to perform this calculation the DrugBank information on uniprot targets must be placed in the data directory. This step takes in CORD19_co-occurrence_pairs_scored_filtered_db_uniprot.csv and outputs as many csvs as there are viable targets into data/csvs.

<b>Step 7</b>: This step generates static HTML and JSON files for the website. The files take in the csvs generated in Step6 and output "index.html","dtd_table.html","dtd_table_singleton.html","target_info.html", and "downloads.html" into the data/html directory. It also outputs as many jsons as there are viable targets into data/jsons. 
