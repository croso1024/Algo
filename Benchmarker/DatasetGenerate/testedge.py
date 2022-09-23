import networkx as nx 
import numpy as np 
import matplotlib.pyplot as plt 


G = nx.Graph() 

node = [str(i) for i in range(9)]

G.add_nodes_from(node) 

print(G.nodes)

G.add_edge("0","1")
G.add_edge("0","1")
G.add_edge("1","0") 
G.add_edge("1","1")
subG = nx.subgraph(G,["0","1","5"])

print(subG.nodes)
print(subG.edges)