
import networkx as nx 
import json 
import numpy as np 
import matplotlib.pyplot as plt




with open("map/EncodeMap.json" , "r") as file  :
    Mapfile = json.load(file) 

stationList = Mapfile["station"]
adjencyMatrix = Mapfile["adjencyMatrix"]


sourceGraph = nx.Graph() 

for  node in stationList: sourceGraph.add_node(node) 

print(sourceGraph.nodes)

for i, node in enumerate(stationList): 
            for j in range(i+1,len(stationList)): 
                cost = adjencyMatrix[i][j]
                if cost: 
                    sourceGraph.add_edge(node,stationList[j],weight=cost)
                    
                    
print(sourceGraph.edges())
                    

                    
# extract the sub-graph by nx.subgraph method   
# then covert it to numpy array 
subG = nx.subgraph(sourceGraph,np.array(["2","5","12"]))
subG2 = nx.subgraph(sourceGraph,["5","2","12"])
### !!! subgraph和給node的type, order無關

np_subG = nx.to_numpy_array(subG)
np_subG2 = nx.to_numpy_array(subG2,["2","5","12"])
### 在用to_numpy_array生成adjency的時候 , 第二個參數可以輸入要的順序 , 否則生成的順序詭異 !
# print(np_subG)
# print(np_subG2)


# when subgraph be covert to numpy array , the sequency of col/row will be arranged as small 2 high 


# if the solution of above request is 2 -> 12 ->5 ->1 
# the currect adjency matrix have 2 representation method 

# 1. directed  & not self-loop 
[
   # 1 , 2 , 5 , 12  
    [0,0,0,0] ,   # 1 -> nothing 
    [0,0,0,1] ,   # 2 -> 12 
    [0,0,1,0] ,   # 12 -> 5
    [1,0,0,0] ,   # 5 -> 1
]

# 2. bidirected & not self-loop 
[
   # 1 , 2 , 5 , 12  
    [0,0,1,0] ,   # 1 <-> 5 
    [0,0,0,1] ,   # 2 <-> 12 
    [0,1,1,0] ,   # 12 <-> 5
    [1,0,0,0] ,   # 5 <-> 1
]


def sub_graphFeatute(sampleNodes): 
    subGraph = nx.subgraph(sourceGraph,sampleNodes)
    return nx.to_numpy_array(subGraph,sorted(sampleNodes,key=lambda i : int(i)))

def sol_to_adjency(sampleSize , solutionNodes): 
    
    init = np.zeros(shape=(sampleSize,sampleSize)  ) 
    solutionNodes = [int(i) for i in solutionNodes]
    seq = sorted(solutionNodes)

    for idx in range(len(solutionNodes) -1): init[seq.index(solutionNodes[idx])][seq.index(solutionNodes[idx+1])] = 1 
       
    return init 

#print(sol_to_adjency(5 , ["2","12","5","1","9"]))
# currect adj  , follow the seqence of ascending power

# [
#     [0. 0. 0. 0.]  1-> nothing 
#     [0. 0. 0. 1.]  2-> 12 
#     [1. 0. 0. 0.]  5-> 1 
#     [0. 0. 1. 0.]  12-> 5 
# ]