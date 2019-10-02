'''
file   : miner_get_stats.py
authors : Agrim Gupta
updated by Farzaan Kaiyom with methods and new data

Script to print basic statistics of the miner dataset.

Usage: 
python miner_get_stats.py <input_file>

Positional Arguments:
input_file : Path to the multi-modal network

Example Usage: 
Input file : miner.graph

Command line: 
python miner_get_stats.py ./miner.graph
'''

import sys
sys.path.insert(0, './../../swig/')
import snap
import argparse

parser = argparse.ArgumentParser(description='Print basic statistics of the miner dataset')
parser.add_argument('input_file', help='path to the multi-modal network')
args = parser.parse_args()

#methods to test modes
def chemStats(Graph):
  cm = Graph.GetModeNetByName("Chemical")
  print("Chemical ",cm.GetNodes())
def protStats(Graph):
  pm = Graph.GetModeNetByName("Protein")
  print("Protein ",pm.GetNodes())
def geneStats(Graph):
  gm = Graph.GetModeNetByName("Gene")
  print("Gene ",gm.GetNodes())
def funcStats(Graph):
  fm = Graph.GetModeNetByName("Function")
  print("Function ",fm.GetNodes())
def disStats(Graph):
  dm = Graph.GetModeNetByName("Disease")
  print("Disease ",dm.GetNodes())
  
#methods to test nets
def chemChem(Graph):
  ccc = Graph.GetCrossNetByName("Chemical-Chemical")
  print("Chemical-Chemical ",ccc.GetEdges())
def chemGene(Graph):
  cgc = Graph.GetCrossNetByName("Chemical-Gene")
  print("Chemical-Gene ",cgc.GetEdges())
def funcFunc(Graph):
  ffc = Graph.GetCrossNetByName("Function-Function")
  print("Function-Function ",ffc.GetEdges())
def geneFunc(Graph):  
  gfc = Graph.GetCrossNetByName("Gene-Function")
  print("Gene-Function ",gfc.GetEdges())
def geneProt(Graph):  
  gpc = Graph.GetCrossNetByName("Gene-Protein")
  print("Gene-Protein ",gpc.GetEdges())
def disDis(Graph):
  ddc = Graph.GetCrossNetByName("Disease-Disease")
  print("Disease-Disease",ddc.GetEdges())
def disGene(Graph):
  dgc = Graph.GetCrossNetByName("Disease-Gene")
  print("Disease-Gene",dgc.GetEdges())
def disFunc(Graph):
  dfc = Graph.GetCrossNetByName("Disease-Function")
  print("Disease-Function ",dfc.GetEdges())
def disChem(Graph):
  dcc = Graph.GetCrossNetByName("Disease-Chemical")
  print("Disease-Chemcial ",dcc.GetEdges())
def protProt(Graph):
  ppc = Graph.GetCrossNetByName("Protein-Protein")
  print("Protein-Protein ",ppc.GetEdges())
  
print("Printing Modes")
FIn = snap.TFIn(args.input_file)
Graph = snap.TMMNet.Load(FIn)
try: 
  geneStats(Graph)
except:
  print("Skipped genes")
try:
  protStats(Graph)
except:
  print("Skipped proteins")
try:
  chemStats(Graph)
except:
  print("Skipped chem")
try:
  funcStats(Graph)
except:
  print("Skipped func")
try:
  disStats(Graph)
except:
  print("Skipped dis")

print("Printing CrossNets")
try:
  geneProt(Graph)
except:
  print("Skipped geneProt")
try:
  chemChem(Graph)
except:
  print("Skipped chemChem")
try:
  funcFunc(Graph)
except:
  print("Skipped funcFunc")
try:
  chemGene(Graph)
except:
  print("Skipped chemGene")
try:
  geneFunc(Graph)
except:
  print("Skipped geneFunc")
try:
  geneProt(Graph)
except:
  print("Skipped geneProt")
try:
  disDis(Graph)
except:
  print("Skipped disDis")
try:
  disGene(Graph)
except:
  print("Skipped disGene")
try:
  disFunc(Graph)
except:
  print("Skipped disFunc")
try:
  disChem(Graph)
except:
  print("Skipped disChem")
#protProt(Graph)




