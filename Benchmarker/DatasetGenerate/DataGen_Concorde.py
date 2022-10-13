"""
    Data generation from concorde   ,
    
    change the solver to concorde , pass the sub-all-pair dijksta matrix to solve problem 
    
    
    subjectecd the all pair dijkstra on sub-adjmatrix to build node feature 
    
        total: 
        node_feature : b*n*n  , all pair dijkstra  adjency matrix 
        edge_index : b*e , all edge in the subgraph , bi-edge , undirection 
        edge_weight : b*e , use the "shortest path" as the weight of edge 
        <! -- y :          b*n*n ,   the label route represent by the node-feature likes shape  -->  no generate 
        y_CE :       b*n  , represent the route by "seqence" of classes   , for crossentropy loss 
        opt :        b , the baseline algorithms cost for same problem       
"""


Path = "/home/croso1024/python_code/Algorithms/Benchmarker"

store_path1 = "/home/croso1024/python_code/GNN/Dataset/"
store_path2 = "/home/croso1024/python_code/Algorithms/Benchmarker/DatasetGenerate/"
store_path3 = "/home/kangli/Ming_ws/GNN/Dataset/"

import sys 
if not Path in sys.path : sys.path.append(Path)

import torch
from Benchmark_ import Benchmarker 
from Branch_Bound  import BranchBound 
from Exhaustive_Slover import Exhaustiver
import json 
import numpy as np
import networkx as nx
import time 
import matplotlib.pyplot as plt 
from tqdm import tqdm 

from concorde.tsp import TSPSolver 


#### Loading map ####
Benchmarker.setting("DatasetGenerate/trainMap.json")
Benchmarker.Source_graphLoading() 
SourceGraph = Benchmarker.SourceGraph
Stations = Benchmarker.station_list  
All_pair_cost = Benchmarker.All_pair_cost 

# add self-loop to graph
for node in Stations: 
    SourceGraph.add_edge(node,node,weight=0)


#print("done")
#print(All_pair_cost)

def Sampler(size=5) : # --> generate the random list  ! just for single vehicle 
    out =  list(np.random.choice(Stations , size , replace=False) )
    #print(f"Debug Sampler:{out}")
    
    return out
    



def GraphFeature(seq) : # --> output the node-feature matrix ( dijksta )
    
    subGraph = nx.subgraph(SourceGraph,seq) 
    sub_dijkstra = dict(nx.all_pairs_dijkstra_path_length(subGraph)) 
    
    ###### Node Feature extract ###############################################
    
    seq_sort = sorted(seq , key = lambda x : int(x)) 
    #print(f"Debug : seq-sort : {seq_sort}")

    reindex = {seq[i] : seq_sort.index(seq[i]) for i in range(len(seq))}    
    
    #print(f"Debug : re-index:{reindex}")
    #print(f"Debug : sub dijkstra :{sub_dijkstra}")

    Dijkstra_nodeFeature = np.zeros( (len(seq),len(seq) ) , dtype = np.float32)
    
    
    # --> src & dst node is "str" node and not yet normalized 
    # --> need use reindex 
    for src_node in sub_dijkstra :
        
        for dst_node in sub_dijkstra[src_node]: 

            Dijkstra_nodeFeature[ reindex[src_node] ][  reindex[dst_node] ]  = sub_dijkstra[src_node][dst_node] 
    
    
    #print(f"Debug : Dijkstra node feature : \n {Dijkstra_nodeFeature}")


    ############ Edge Featrue extract ###########
    edgeIndex = list() 
    edgeWeight = list() 
    
    for u,v in subGraph.edges: 
        
        edgeWeight.append(sub_dijkstra[u][v])
        edgeWeight.append(sub_dijkstra[v][u])
        edgeIndex.append([reindex[u] , reindex[v]])
        edgeIndex.append([reindex[v] , reindex[u]])
    
    return Dijkstra_nodeFeature , edgeIndex , edgeWeight 
    

def concorde_Solver(dist_matrix , vehicle_num=1) -> list:     #--> output opt , y_CE

    Solver = TSPSolver.from_data(dist_matrix=dist_matrix.copy())
    
    output = Solver.solve() 
    
    #print(f"Debug output-tour : {output.tour}")

    #print(f"Debug output cost : {output.optimal_value}")
    return output.tour , int(output.optimal_value/100)


def main(sampleSize = 20 ,dataSize = 1000 , save= True ,savePath =store_path1 ): 
    
    Stations_length = len(Stations) - 1
    inputNodefeature = []  # --> Dijksta matrix  
    inputEdgeindex = []  
    inputEdgeweight = [] 
    y_CE = []
    opt = []

    for i in tqdm(range(dataSize)): 
        
        Input = Sampler(sampleSize)
        
        node_feature , edge_index , edge_weight = GraphFeature(Input) 
        y_ce , optCost = concorde_Solver(node_feature)
        # print(f"node feature : \n{node_feature}" )
        # print(f"edge index {edge_index}" )
        # print(f"edge weight {edge_weight}" )
        # print(f"y_ce :{y_ce}")
        # print(f"opt : {optCost}")


        inputNodefeature.append(node_feature)
        inputEdgeindex.append(edge_index) 
        inputEdgeweight.append(edge_weight)
        y_CE.append(y_ce) 
        opt.append(optCost)

        # covert to tensor 
    tensor_Node_feature = torch.tensor(np.array(inputNodefeature) , dtype=torch.float)
    tensor_Edge_index = torch.tensor(np.array(inputEdgeindex) ,dtype=torch.long)
    tensor_Edge_weight = torch.tensor(np.array(inputEdgeweight) , dtype=torch.float)
    tensor_y_CE = torch.tensor(np.array(y_CE) , dtype=torch.long)  
    tensor_opt = torch.tensor(np.array(opt),dtype=torch.float32)

    print(tensor_Node_feature.shape) 
    print(tensor_Edge_index.shape) 
    print(tensor_Edge_weight.shape)
    print(tensor_y_CE.shape)
    print(tensor_opt.shape) 

    if save :
        torch.save(tensor_Node_feature,  savePath+"node_feature.pt")
        torch.save(tensor_Edge_index,    savePath+"edge_index.pt")
        torch.save(tensor_Edge_weight,   savePath+"edge_weight.pt"  ) 
        torch.save(tensor_y_CE,          savePath+"labels_CE.pt")
        torch.save(tensor_opt,           savePath+"opt.pt")
main()
