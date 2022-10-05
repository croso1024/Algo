import sys

Path = "/home/croso1024/python_code/Algorithms/Benchmarker"

store_path1 = "/home/croso1024/python_code/GNN/Dataset/"
store_path2 = "/home/croso1024/python_code/Algorithms/Benchmarker/DatasetGenerate/"


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
Benchmarker.setting("map/EncodeMap.json")
Benchmarker.Source_graphLoading() 


# Dataset generate script : 
# 1. loading map 
# 2. sample(request) and solve(cost , sequence)  
# 3. overwrite . 


#### Loading map ####
SourceGraph = Benchmarker.SourceGraph
Stations = Benchmarker.station_list  
All_pair_cost = Benchmarker.All_pair_cost 

# add self-loop to graph
for node in Stations: 
    SourceGraph.add_edge(node,node,weight=0)


#### create container ####
Stations_length = len(Stations) - 1
inputNodefeature = [] 
inputEdgeindex = [] 
inputEdgeweight = [] 
y = [] 
y_CE = []
opt = []



def Solver(input_sequence,vehicle_num=1) -> list : 
    
    sol = Exhaustiver(initial_solution=list(input_sequence),iteration_num=362880,vehicle_num=1,early_stop=False,GenerateMode=True)
    optimal_cost , optimal_solution = sol.evaluate(plotting=False)
    
    return optimal_cost ,optimal_solution 


Sampling  = lambda size,v_num=1 : (np.random.choice(Stations,size , replace=False) , 1)

# return node featrues which be selected as sample request 
# the second arg in "'to_numpy_array()" is the order that adjency matrix col/row  !!!

def sub_graphFeature(sampleNodes,table,useDijkstra = False): 
    # table --> {  sample[0]:index ... }
    # ex. table[samplenode] --> corresponding index in subgraph 
    
    subGraph = nx.subgraph(SourceGraph,sampleNodes)

    ## the key type of sub_apc is "string" , but sequence table key is "int" !
    #subGraph_all_pair_cost = dict(nx.all_pairs_dijkstra_path_length(subGraph))
    
    #print(subGraph_all_pair_cost)
    edgeIndex = list() 
    edgeWeight = list() 

    if useDijkstra: 
        for i,j in subGraph.edges: 
            edgeWeight.append(All_pair_cost[i][j])
            edgeWeight.append(All_pair_cost[j][i])
            i , j = int(i) , int(j) 
            edgeIndex.append([table[i],table[j]])
            edgeIndex.append([table[j],table[i]])
        
        
        node_feature = np.zeros((len(sampleNodes),len(sampleNodes))  , dtype=np.float32 )

        for source_node in sampleNodes:  

            s_idx = table[int(source_node)]
    
            for target_node in sampleNodes: 
                
                t_idx = table[int(target_node)]
                node_feature[s_idx][t_idx] = All_pair_cost[source_node][target_node]
                
        # print("-------")
        # print(node_feature)
        
    
    # there is not complete for non-dijkstra version  --- 1003 
    else: 
        for i,j in subGraph.edges: 
            edgeWeight.append(SourceGraph[i][j]["weight"])
            edgeWeight.append(SourceGraph[j][i]["weight"])
            i , j = int(i) , int(j) 
            edgeIndex.append([table[i],table[j]])
            edgeIndex.append([table[j],table[i]])
        
    
    
    return node_feature , edgeIndex , edgeWeight

# return the adjency representation of those sample Nodes by solution 
def sol_to_adjency(sampleSize , solutionNodes,table , cycle=True): 
    

    solutionNodes = [int(i) for i in solutionNodes]  # covert node to int 

    init = np.zeros(shape=(sampleSize,sampleSize)  ) 
    for idx in range(len(solutionNodes) - 1): 
        init[table[solutionNodes[idx]]][table[solutionNodes[idx+1]]] = 1
    
    
    crossEntropylabels = [] 
    for row in init : 
        crossEntropylabels.append(list(row).index(1)) 
    
        
      
    return init ,crossEntropylabels
        
            
            

def Generate(Dataset_size=4000 ,save=False ,  output_path="./Testdata.json",savePath=store_path1): 
    
    for i in range(Dataset_size): 
      
        sample , vehicleNum = Sampling(8)  
        #sample = [str(i) for i in range(6)]
        vehicleNum = 1 
        sample = list(sample)
        sequence = sorted(list(set(sample)),key = lambda i : int(i)) 
        sequenceTable = {int(i):sequence.index(i) for i in sample }
        # print(f"sample :{sample}")
        # print(f"sequence : {sequence}")
        # print(f"sequence table : {sequenceTable}")

        
        
        optCost,labels  = Solver(sample)
        print(f"Sample input = {sample}, y = {labels}")
        


        # sample --> 需要單獨建立一張grpah ,
        # 但要remapping node的編碼  對應的label也需要重新mapping  
        # 重建的grpah要嘗試看看全連接或raw graph 
   
        node_features ,edge_index , edge_weight= sub_graphFeature(sample,sequenceTable,useDijkstra=True) 
        labels,CElabels = sol_to_adjency(len(sample) , labels , sequenceTable) 
        
        #print(f"node_feature:  {node_features} ")
        print(f"y : {labels}, y_CE : {CElabels} opt:{optCost}" )
        #print("#######################")
        
        
        inputNodefeature.append(node_features) 
        inputEdgeindex.append(edge_index)
        inputEdgeweight.append(edge_weight)
        y.append(labels)
        y_CE.append(CElabels)
        opt.append(optCost)
        #print(edge_index)
        #print(edge_weight)

    # Data = {"input":inputDataset , "y":y} 
    # with open(output_path , "w") as file : 
    #     file.write(json.dumps(Data))

    # covert to tensor 
    tensor_Node_feature = torch.tensor(np.array(inputNodefeature) , dtype=torch.float)
    tensor_Edge_index = torch.tensor(np.array(inputEdgeindex) ,dtype=torch.long)
    tensor_y = torch.tensor(np.array(y) , dtype=torch.float)
    tensor_Edge_weight = torch.tensor(np.array(inputEdgeweight) , dtype=torch.float)
    tensor_y_CE = torch.tensor(np.array(y_CE) , dtype=torch.long)  
    tensor_opt = torch.tensor(np.array(opt),dtype=torch.float32)
    
    print(tensor_Node_feature.shape) 
    print(tensor_Edge_index.shape) 
    print(tensor_Edge_weight.shape)
    print(tensor_y.shape)
    print(tensor_y_CE.shape)
    print(tensor_opt.shape) 
    
    
    # print(tensor_Node_feature[5])
    # print(tensor_Edge_index[5])
    # print(tensor_y[5])
    if save :
        torch.save(tensor_Node_feature,  savePath+"node_feature.pt")
        torch.save(tensor_Edge_index,    savePath+"edge_index.pt")
        torch.save(tensor_Edge_weight,   savePath+"edge_weight.pt"  ) 
        torch.save(tensor_y,             savePath+"labels.pt")
        torch.save(tensor_y_CE,          savePath+"labels_CE.pt")
        torch.save(tensor_opt,           savePath+"opt.pt")


Generate(save=1)

    
        