This directory contains script(s) for getting the mapping between protein and genes.
Note that running this script requires connecting to the ENSEMBL server.

To download the ENSEMBL mapping, the following dependences are required.
1. biomart python interface (https://pypi.python.org/pypi/biomart/0.9.0)

This mapping is needed because STRING specifies peptide ensembl ids and HUGO uses
gene ensembl ids.
