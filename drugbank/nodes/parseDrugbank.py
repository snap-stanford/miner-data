###########################################
# XML parser to parse the drugbank database
# Will output a space separated .txt file
# with the following coloumn headers:
# DrugbankID PubChem_Compound PubChem_Substance
# Requirements : Assumes that durgbank.xml is in the 
# same folder.
###########################################

from bs4 import BeautifulSoup
soup = BeautifulSoup(open("./drugbank.xml"),"xml")
sep = " "
empty = "NULL"
with open('did_pubC_pubS.txt', 'w') as f:
    for drug in soup.findAll("drug"):
        flag = False
        toPrint = ""
        toPrint += drug.find("drugbank-id").text + sep
        #toPrint += drug.find("name").text + sep
        identifiers = [i for i in drug.findAll("external-identifier")]
        for i in identifiers:
            database = i.find("resource").text
            if database != "PubChem Compound":
                continue
            value = i.find("identifier").text
            flag = True
            toPrint += value + sep
        if not flag:
            toPrint += empty + sep

        for i in identifiers:
            database = i.find("resource").text
            if database != "PubChem Substance":
                continue
            value = i.find("identifier").text
            flag = True
            toPrint += value + sep
        if not flag:
            toPrint += empty + sep
        f.write(toPrint.encode('utf-8') + '\n')
    
 
