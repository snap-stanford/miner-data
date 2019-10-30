'''
file   : miner_get_stats.py
authors : Farzaan Kaiyom, Agrim Gupta

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
def modeStats(Graph,name):
  try:
    gp = Graph.GetModeNetByName(name)
    print(name,": ",gp.GetNodes())
  except:
    print(name," skipped")

def crossStats(Graph,name):
  try:
    gp = Graph.GetCrossNetByName(name)
    print(name,": ",gp.GetEdges()) # use getEdges for older versions of SNAP.py
  except:
    print(name," skipped")
  
print("Printing Modes")
FIn = snap.TFIn(args.input_file)
Graph = snap.TMMNet.Load(FIn)

modeStats(Graph,"Chemical")
modeStats(Graph,"Protein")
modeStats(Graph,"Gene")
modeStats(Graph,"Function")
modeStats(Graph,"Disease")

print("Printing CrossNets")

crossStats(Graph,"Chemical-Chemical")
crossStats(Graph,"Chemical-Gene")
crossStats(Graph,"Function-Function")
crossStats(Graph,"Gene-Function")
crossStats(Graph,"Gene-Protein")
crossStats(Graph,"Disease-Disease")
crossStats(Graph,"Disease-Gene")
crossStats(Graph,"Disease-Function")
crossStats(Graph,"Disease-Chemical")
crossStats(Graph,"Protein-Protein")
