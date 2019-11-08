import snap
import time

#from utils.network_utils import get_num_elem_per_mode

filename = "Graphs/oldMinerNewSNAP.graph"
FIn = snap.TFIn(filename)
Graph = snap.TMMNet.Load(FIn)

print('Modes: %d' % Graph.GetModeNets())
print('Link types: %d' % Graph.GetCrossNets())

crossnetids = snap.TInt64V()
crossneti = Graph.BegCrossNetI()
while crossneti < Graph.EndCrossNetI():
    crossnetids.Add(crossneti.GetCrossId())
    crossneti.Next()

nodeattrmapping = snap.TIntStrStrTr64V()
edgeattrmapping = snap.TIntStrStrTr64V()
start_time = time.time()
DirectedNetwork = Graph.ToNetwork(crossnetids, nodeattrmapping, edgeattrmapping)
end_time = time.time()
print("Converting to TNEANet  takes %s seconds" % (end_time - start_time))

snap.PrintInfo(DirectedNetwork, "Python type PNEANet", "output.txt", False)
map(lambda x: x.replace("\n", ""), open("output.txt").readlines())
