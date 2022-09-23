import sys
Path = "/home/croso1024/python_code/Algorithms/Benchmarker"
if not Path in sys.path : sys.path.append(Path)

import torch
from Benchmark_ import Benchmarker 
from Branch_Bound  import BranchBound 
from Exhaustive_Slover import Exhaustiver
import json 
import numpy as np
import networkx as nx
import time 

Benchmarker.setting("map/EncodeMap.json")
Benchmarker.Source_graphLoading() 


# Dataset generate script : 
# 1. loading map 
# 2. sample(request) and solve(cost , sequence)  
# 3. overwrite . 

SourceGraph = Benchmarker.SourceGraph


Stations = Benchmarker.station_list  

# add self-loop to graph
for node in Stations: 
    SourceGraph.add_edge(node,node,weight=0)



Stations_length = len(Stations) - 1
inputNodefeature = [] 
inputEdgeindex = [] 
inputEdgeweight = [] 
y = [] 



def Solver(input_sequence,vehicle_num=1) -> list : 
    
    #sol = BranchBound(initial_solution=list(input_sequence),vehicle_location=None,GenerateMode=True)
    #optimal_solution = sol.main(plotting=False) 
    sol = Exhaustiver(initial_solution=list(input_sequence),iteration_num=362880,vehicle_num=1,early_stop=False,GenerateMode=True)
    optimal_solution = sol.evaluate(plotting=False)
    
    return optimal_solution 

def Sampling(sample_size=6 ,vehicle_num = 1 ):
    sample = ( np.random.choice(Stations  , sample_size,replace=False)  , 1) 
    
    return sample


# return node featrues which be selected as sample request 
# the second arg in "'to_numpy_array()" is the order that adjency matrix col/row  !!!
def sub_graphFeatute(sampleNodes,table): 
    subGraph = nx.subgraph(SourceGraph,sampleNodes)
    
    edgeIndex = list()
    edgeWeight = list() 
    for i,j in subGraph.edges : 
        
        if not i == j :
            
            edgeWeight.append(SourceGraph[i][j]["weight"])
            edgeWeight.append(SourceGraph[j][i]["weight"])
            i , j = int(i) , int(j)
            edgeIndex.append([table[i],table[j]])  
            edgeIndex.append([table[j],table[i]])

            

    # for u,v in edgeIndex: 
    #     edgeWeight.append()
    
    return nx.to_numpy_array(subGraph,sorted(sampleNodes,key=lambda i : int(i))) , edgeIndex ,edgeWeight

# return the adjency representation of those sample Nodes by solution 
def sol_to_adjency(sampleSize , solutionNodes,table): 
    

    solutionNodes = [int(i) for i in solutionNodes]

    init = np.zeros(shape=(sampleSize,sampleSize)  ) 
    for idx in range(len(solutionNodes) - 1): 
        init[table[solutionNodes[idx]]][table[solutionNodes[idx+1]]] = 1
    
        
      
    return init 
        
            
            

def Generate(Dataset_size=1000 , output_path="./Testdata.json"): 
    
    for i in range(Dataset_size): 
      
        sample , vehicleNum = Sampling(6)  
        sample = list(sample)
        sequence = sorted(list(set(sample)),key = lambda i : int(i)) 
        sequenceTable = {int(i):sequence.index(i) for i in sample }
            
        
        
        labels = Solver(sample)[1]
        print(f"Sample input = {sample}, y = {labels}")
        


        # sample --> 需要單獨建立一張grpah ,
        # 但要remapping node的編碼  對應的label也需要重新mapping  
        # 重建的grpah要嘗試看看全連接或raw graph 
   
        node_features ,edge_index , edge_weight= sub_graphFeatute(sample,sequenceTable) 
        labels = sol_to_adjency(len(sample) , labels , sequenceTable) 
        
        #print(f"node_feature:  {node_features} ")
        #print(f"y : {labels}")
        #print("#######################")
        
        
        
        inputNodefeature.append(node_features) 
        inputEdgeindex.append(edge_index)
        inputEdgeweight.append(edge_weight)
        y.append(labels)
        print(edge_index)
        print(edge_weight)

    # Data = {"input":inputDataset , "y":y} 
    # with open(output_path , "w") as file : 
    #     file.write(json.dumps(Data))

    # covert to tensor 
    tensor_Node_feature = torch.tensor(np.array(inputNodefeature) , dtype=torch.float)
    tensor_Edge_index = torch.tensor(np.array(inputEdgeindex) ,dtype=torch.long)
    tensor_y = torch.tensor(np.array(y) , dtype=torch.float)
    tensor_Edge_weight = torch.tensor(np.array(inputEdgeweight) , dtype=torch.float)
    
    
    print(tensor_Node_feature.shape) 
    print(tensor_Edge_index.shape) 
    print(tensor_Edge_weight.shape)
    print(tensor_y.shape)
    
    
    # print(tensor_Node_feature[5])
    # print(tensor_Edge_index[5])
    # print(tensor_y[5])
    torch.save(tensor_Node_feature,"./DatasetGenerate/node_feature.pt")
    torch.save(tensor_Edge_index,"./DatasetGenerate/edge_index.pt")
    torch.save(tensor_Edge_weight,"./DatasetGenerate/edge_weight.pt"  ) 
    torch.save(tensor_y,"./DatasetGenerate/labels.pt")
    


Generate()

    
        