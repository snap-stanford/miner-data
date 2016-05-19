########################################################
# Takes as input a .txt file of drug-drug interactions.
# and subSnapDrugbank.txt which contains mapping from
# snapChemicalId to DrugbankId. 
# Outputs : 
# 1. Master Edge Table: SnapCCId EdgeTableNo SrcId DstId
# 2. Sub Tables: 
#     1. SnapCCId SrcId DstId (DrugbankId)
# All edges are undirected. Hence A-B is reported only 
# once. 
#########################################################
from collections import defaultdict

sep = " "
snapIdPrefix = "SCC"
edgeFile = "edgesD.txt"
nodeMap = "./../nodes/subSnapDrugbank.txt"
masterTable = "snapChemicalCC.txt"
subTable = "subSnapDrugbankCC.txt"
idNum = 0
# Make a dict mapping from drugbankId to snapChemId
drugbankSnap = {}
with open(nodeMap, 'r') as f:
    for line in f:
        line = line.strip().split(sep)
        drugbankSnap[line[1]] = line[0]

drugsDone = defaultdict(list)
with open(edgeFile, 'r') as f, open(masterTable, 'w') as master, open(subTable, 'w') as sub:
    for line in f:
        line = line.strip().split(sep)
        if line[1] in drugsDone[line[0]]:
            continue
        if line[0] not in drugbankSnap or line[1] not in drugbankSnap:
            continue
        drugsDone[line[0]].append(line[1])
        snapId = snapIdPrefix + str(idNum)
        idNum += 1
        master.write(snapId + sep + "0 " + drugbankSnap[line[0]] + sep + drugbankSnap[line[1]] + '\n')
        sub.write(snapId + sep + line[0] + sep + line[1] + '\n')


