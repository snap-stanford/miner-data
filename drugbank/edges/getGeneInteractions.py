###########################################
# XML parser to parse the drugbank database
# Will output a space separated .txt file
# with the following coloumn headers:
# DrugbankId Gene1 Gene2 ...
# Currently UniportID is used for genes.
###########################################

from bs4 import BeautifulSoup
soup = BeautifulSoup(open("./../drugbank.xml"),"xml")
sep = " "
empty = "NULL"
#geneIdentifier = "HUGO Gene Nomenclature Committee (HGNC)"
geneIdentifier = "UniProtKB"
with open('drugGene.txt', 'w') as f:
    for drug in soup.findAll("drug"):
        toPrint = ""
        toPrint += drug.find("drugbank-id").text + sep
        # Get target Genes
        targets = drug.findAll("target")
        targetGene = []
        if targets:
            for target in targets:
                externIden = target.findAll("external-identifier")
                if not externIden:
                    continue
                for iden in externIden:
                    if iden.find("resource").text == geneIdentifier:
                        targetGene.append(iden.find("identifier").text)
        # Get Enzyme Gene
        enzymes = drug.findAll("enzyme")
        enzymeGene = []
        if enzymes:
            for enzyme in enzymes:
                externIden = enzyme.findAll("external-identifier")
                if not externIden:
                    continue
                for iden in externIden:
                    if iden.find("resource").text == geneIdentifier:
                        enzymeGene.append(iden.find("identifier").text)
        allGene = targetGene + enzymeGene
        if len(allGene) == 0:
            toPrint += empty
        else:
            toPrint += ','.join(allGene)
        f.write(toPrint.encode('utf-8') + '\n')
    
 
