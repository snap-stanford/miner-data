'''
file   : miner_get_stats.py
author : Agrim Gupta

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

print "Printing Modes"
FIn = snap.TFIn(args.input_file)
Graph = snap.TMMNet.Load(FIn)
cm = Graph.GetModeNetByName("Chemical")
print "Chemical ",cm.GetNodes()
pm = Graph.GetModeNetByName("Protein")
print "Protein ",pm.GetNodes()
gm = Graph.GetModeNetByName("Gene")
print "Gene ",gm.GetNodes()
fm = Graph.GetModeNetByName("Function")
print "Function ",fm.GetNodes()
dm = Graph.GetModeNetByName("Disease")
print "Disease ",dm.GetNodes()

print "Printing CrossNets"
ccc = Graph.GetCrossNetByName("Chemical-Chemical")
print "Chemical-Chemical ",ccc.GetEdges()
cgc = Graph.GetCrossNetByName("Chemical-Gene")
print "Chemical-Gene ",cgc.GetEdges()
ffc = Graph.GetCrossNetByName("Function-Function")
print "Function-Function ",ffc.GetEdges()
gfc = Graph.GetCrossNetByName("Gene-Function")
print "Gene-Function ",gfc.GetEdges()
gpc = Graph.GetCrossNetByName("Gene-Protein")
print "Gene-Protein ",gpc.GetEdges()
ddc = Graph.GetCrossNetByName("Disease-Disease")
print "Disease-Disease",ddc.GetEdges()
dgc = Graph.GetCrossNetByName("Disease-Gene")
print "Disease-Gene",dgc.GetEdges()
dfc = Graph.GetCrossNetByName("Disease-Function")
print "Disease-Function ",dfc.GetEdges()
dcc = Graph.GetCrossNetByName("Disease-Chemical")
print "Disease-Chemcial ",dcc.GetEdges()
ppc = Graph.GetCrossNetByName("Protein-Protein")
print "Protein-Protein ",ppc.GetEdges()
