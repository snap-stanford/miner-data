#############################################
# XML parser to parse the drugbank database
# Will output a space separated .txt file
# with the following coloumn headers:
# DrugbankId DrugbankId
# Each line represents a drug-drug interatcion
##############################################

from bs4 import BeautifulSoup
soup = BeautifulSoup(open("./drugbank.xml"),"xml")
sep = " " 
with open('edgesD.txt', 'w') as f:
    for drug in soup.findAll("drug"):
        drugName = drug.find("drugbank-id").text 
        interactions = drug.findAll("drug-interaction")
        if not interactions:
            continue
        for i in interactions:
            toPrint = drugName + sep + i.find("drugbank-id").text
            f.write(toPrint.encode('utf-8') + '\n')

    
 
