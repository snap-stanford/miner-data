Generate Edges from Drugbank Database
-------------------------------------

1. Models the following interactions from the drugbank database:
   1. Drug-Drug interaction
   2. Drug-Gene interacion
2. External Dependencies:
   1. Requires mapping from SnapGeneID<->UniportKB
3. Steps:
   I. Download drugbank.xml
   II. Ensure that gene mapping from 2 is in the current folder.
   III. Run make-edges.sh
3. If BeautifulSoup is not installed or you don't have permissions to install:
   I. Follow steps mentioned on http://docs.python-guide.org/en/latest/dev/virtualenvs/ 
   II. Next launch the env as : source /env/bin/activate
   III. Run make-edges.sh
