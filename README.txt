Scripts used to extract nodes and edges from MINER data.


The Utils directory consists of general scripts that can be used to process multiple datasets.

In addition, there are directories (with readmes on how to generate the respective snap tables) for each of the following Modes and CrossNets:

Modes
- Genes
	- HUGO (http://www.genenames.org/cgi-bin/statistics)
	- GeneOntology (http://geneontology.org/page/download-go-annotations)
- Proteins
	- STRING (http://string-db.org/cgi/download.pl)
- Functions
	- GeneOntology (http://geneontology.org/page/download-ontology)
- Chemicals
        - Drugbank (http://www.drugbank.ca/)
- Diseases
	- DiseaseOntology (http://disease-ontology.org/)
	- CTD (http://ctdbase.org)
	- OMIM (http://www.omim.org/)

CrossNets
- Gene-Protein
	- ENSEMBL Genes, Human genes (http://www.ensembl.org/biomart/martview)
- Protein-Protein
	- STRING (http://string-db.org/cgi/download.pl)
- Gene-Function
	- GeneOntology (http://geneontology.org/docs/download-go-annotations/)
- Function-Function
	- GeneOntology (http://geneontology.org/page/download-ontology)
- Chemical-Chemical
        - Drugbank (http://www.drugbank.ca/)
- Chemical-Gene
        - Drugbank (http://www.drugbank.ca/)
- Disease-Disease
	- DiseaseOntology (http://disease-ontology.org/)
- Disease-Gene
	- CTD (http://ctdbase.org)
- Disease-Chemical
	- CTD (http://ctdbase.org)
- Disease-Function
	- CTD (http://ctdbase.org)

Datasets can be found at /dfs/scratch2/MINER-BIO/data-miner. 

Here's a quick look at the new miner dataset:
-------------------------------
   Modes     |     Nodes
-------------------------------
Chemical     |   *in progress*
Protein      |   22,406,877
Gene         |   106,536
Function     |   48,969
Disease      |   25.969

--------------------------------------
    Cross-Nets     |     Edges
--------------------------------------
Chemical-Chemical  |     *in progress*
Chemical-Gene      |     *in progress*
Function-Function  |     249,828
Gene-Function      |     481,543
Gene-Protein       |     18,650
Disease-Disease    |     9,383
Disease-Gene       |     *33,167*
Disease-Function   |     2,138,340
Disease-Chemical   |     *in progress*
Protein-Protein    |     2,147,483,643
* Disease-Gene number may be incorrect

The old miner-dataset at a glance:
-------------------------------
   Modes     |     Nodes
-------------------------------
Chemical     |     22,486 
Protein      |  8,254,694
Gene         |    104,004
Function     |     46,564
Disease      |     22,299

--------------------------------------
    Cross-Nets     |     Edges
--------------------------------------
Chemical-Chemical  |         95,246
Chemical-Gene      |         15,424
Function-Function  |        119,464
Gene-Function      |        481,733
Gene-Protein       |         17,930
Disease-Disease    |          6,877
Disease-Gene       |     42,475,361
Disease-Function   |        784,457
Disease-Chemical   |      1,334,088
Protein-Protein    |  1,847,117,370
