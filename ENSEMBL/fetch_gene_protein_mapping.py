import sys
from biomart import BiomartServer

def main(newfile):
  atts = ['external_gene_name','external_gene_source','ensembl_gene_id',
          'ensembl_transcript_id','ensembl_peptide_id']
  url = 'http://www.ensembl.org/biomart'
  server = BiomartServer(url )
  hge = server.datasets['hsapiens_gene_ensembl']
  with open(newfile, 'w') as outF:
    s = hge.search({'attributes': atts}, header=1)
    for l in s.iter_lines():
      outF.write('%s\n' % l.strip())

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print 'Usage: python fetch_gene_protein_mapping.py <output_file>'
  else:
    main(sys.argv[1])
