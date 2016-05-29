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

FIn = snap.TFIn(args.input_file)
Graph = snap.TMMNet.Load(FIn)
cm = Graph.GetModeNetByName("Chemical")
print cm.GetNodes()
pm = Graph.GetModeNetByName("Protein")
print pm.GetNodes()
gm = Graph.GetModeNetByName("Gene")
print gm.GetNodes()
fm = Graph.GetModeNetByName("Function")
print fm.GetNodes()
dm = Graph.GetModeNetByName("Disease")
print dm.GetNodes()

ccm = Graph.GetCrossNetByName("Chemical-Chemical")
print ccm.GetEdges()
cgm = Graph.GetCrossNetByName("Chemical-Gene")
print cgm.GetEdges()
ffc = Graph.GetCrossNetByName("Function-Function")
print ffc.GetEdges()
gfc = Graph.GetCrossNetByName("Gene-Function")
print gfc.GetEdges()
gpc = Graph.GetCrossNetByName("Gene-Protein")
print gpc.GetEdges()
ddc = Graph.GetCrossNetByName("Disease-Disease")
print ddc.GetEdges()
dgc = Graph.GetCrossNetByName("Disease-Gene")
print dgc.GetEdges()
dfc = Graph.GetCrossNetByName("Disease-Function")
print dfc.GetEdges()
dcc = Graph.GetCrossNetByName("Disease-Chemical")
print dcc.GetEdges()
