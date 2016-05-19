import sys

def main(fileIn, fileOut):
  with open(fileIn, 'r') as inF:
    with open(fileOut, 'w') as outF:
      for line in inF:
        if line[0] == '!':
          continue
        vals = line.strip().split('\t')
        new_str = '\t'.join(vals[1:5])
        outF.write('%s\n' % new_str)

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print 'Usage: python extract_fields.py <in_file> <out_file>'
  else:
    main(sys.argv[1], sys.argv[2])
