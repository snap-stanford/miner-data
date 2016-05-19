STRING contains both the protein nodes and the protein-protein interaction edges.

Note that nodes are specified using the ENSEMBL peptide id, with the species identifier
prepended.

This directory contains scripts for extracting unique nodes (proteins) given a protein-protein interaction
file and edges, given a protein-protein interaction file with much extraneous information.
See extract_protein_nodes.py and extract_protein_edges.py. Note that, the default separator may have to be
changed in these files before use on the data (assumes spaces for edge extraction - the original format of
the STRING data - and tabs for the node extraction, as it should use the result of edge extraction as input).

It also contains scripts for creating tsv files for creating the tsv files with snap ids, equivalence tables,
and dataset specific ids.
