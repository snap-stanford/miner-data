########################################################
# Takes as input a .txt file of drug-gene interactions.
# and subSnapDrugbank.txt which contains mapping from
# snapChemicalId to DrugbankId.
# Depends on the mapping of Genes to SnapGeneID.
# Outputs : 
# 1. Master Edge Table: SnapCGId EdgeTableNo SrcId DstId
# 2. Sub Tables: 
#     1. SnapCGId SrcId (DrugbankID) DstId (UniportId)
# All edges are undirected. Hence A-B is reported only 
# once. 
#########################################################
from collections import defaultdict

sep = " "
snapIdPrefix = "SCG"
edgeFile = "drugGene.txt"
nodeMap = "./../nodes/subSnapDrugbank.txt"
masterTable = "snapChemicalCG.txt"
subTable = "subSnapDrugbankCG.txt"
geneMap = "./snap.genes.0.go"
idNum = 0
# Make a dict mapping from drugbankId to snapChemId
drugbankSnap = {}
with open(nodeMap, 'r') as f:
    for line in f:
        line = line.strip().split(sep)
        drugbankSnap[line[1]] = line[0]

# Make a dict mapping from UniProtKB to snapGeneId
geneSnap = {}
with open(geneMap, 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        geneSnap[line[1]] = line[0]

with open(edgeFile, 'r') as f, open(masterTable, 'w') as master, open(subTable, 'w') as sub:
    for line in f:
        line = line.strip().split(sep)
        if line[0] not in drugbankSnap:
            continue
        geneList = line[1].split(",")
        if geneList[0] == "NULL":
            continue
        for gene in geneList:
            snapId = snapIdPrefix + str(idNum)
            idNum += 1
            if gene not in geneSnap:
                print gene
                continue
            master.write(snapId + sep + "0 " + drugbankSnap[line[0]] + sep + geneSnap[gene] + '\n')
            sub.write(snapId + sep + line[0] + sep + gene + '\n')


