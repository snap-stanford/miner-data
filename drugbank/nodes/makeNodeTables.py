#######################################################
# Takes input a .txt file with the following col headers
# DrugbankID PubChem_Compound PubChem_Substance
# Ouputs the following files:
# 1. Master Node table : SnapChemID SubTableID
# 2. Sub tables : 
#    1. SanpChemID DrugbankID
#    2. SnapChemID PubChem_Compound
#    3. SanpChemID PubChem_Substance
# 3. Equvialence Table : SnapChemID SnapChemID
#######################################################
import itertools
sep = " "
empty = "NULL"
snapIdPrefix = "SC"
# Names/handles for the output tables
idNum = 0
masterTable = "snapChemical.txt"
subTable = ["subSnapDrugbank.txt", "subSnapPubCompound.txt", "subSnapPubSubstance.txt"]
subHandle = [open(subTable[i], 'w') for i in xrange(len(subTable))]
eqTable = "snapEqChem.txt"
with open('did_pubC_pubS.txt', 'r') as input, open(masterTable, 'w') as master,open(eqTable, 'w') as eqTable:
    for line in input:
        line = line.strip().split(" ")
        currId = []
        for num,id in enumerate(line):
            if id == "NULL":
                continue
            snapId = snapIdPrefix + str(idNum)
            idNum += 1
            master.write(snapId + sep + str(num) + '\n')
            subHandle[num].write(snapId + sep + id + '\n')
            currId.append(snapId)
        allPerms = list(itertools.permutations(currId,2))
        for perm in allPerms:
            toWrite = ' '.join(perm)
            eqTable.write(toWrite + '\n')

[handle.close() for handle in subHandle]

            

            


