inFNm = 'STRING_protein_nodelist.tsv'
outFNm = 'STRING_nodelist.tsv'
with open(inFNm, 'r') as inF:
  with open(outFNm, 'a') as outF:
        for line in inF:
            cur = str(line).replace('\n','')
            organism = cur.split('.')[0]
            cur = cur + '\t' + organism
            outF.write(cur+'\n')
