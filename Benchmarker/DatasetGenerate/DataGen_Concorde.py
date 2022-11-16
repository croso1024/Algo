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


#Path = "/home/croso1024/python_code/Algorithms/Benchmarker"
Path =  "/home/kangli/Ming_ws/Algorithms/Benchmarker"
import sys 
if not Path in sys.path : sys.path.append(Path)

import torch
from Benchmark_ import Benchmarker 
import numpy as np
import networkx as nx
from tqdm import tqdm 
from concorde.tsp import TSPSolver 
from multiprocessing import Process  
import argparse  
from DataGen_utils import * 



if __name__ == "__main__": 
    
    argument = argparse.ArgumentParser()
    
    argument.add_argument("--m_path",type=str , default=None)
    argument.add_argument("--s_path",type=str , default=None) 
    argument.add_argument("--node_dim",type=int , default=20) 
    argument.add_argument("--num_samples",type=int , default=10)
    argument.add_argument("--num_workers",type=int , default=1)
    argument.add_argument("--save",action="store_true",default=False)
    arg = argument.parse_args()
    assert arg.s_path[-1] == "/" , "Store path lost the '/'   " 
    #### Loading map ####
    Benchmarker.setting(arg.m_path)
    Benchmarker.Source_graphLoading() 
    SourceGraph = Benchmarker.SourceGraph
    Stations = Benchmarker.station_list  
    All_pair_cost = Benchmarker.All_pair_cost 
    print(type(SourceGraph))
    print(type(All_pair_cost))

    # add self-loop to graph
    for node in Stations: 
        SourceGraph.add_edge(node,node,weight=0)
    
    process_pool = []
    for i in range(arg.num_workers): 
        
        parameter = (
            SourceGraph.copy(),
            Stations.copy() , 
            All_pair_cost.copy() , 
            arg.node_dim, 
            arg.num_samples//arg.num_workers, 
            arg.save, 
            # arg._num_workers , 
            #i , 
            np.random.randint(low=1,high=99999),
            arg.s_path
        )
        
        p = Process(target=Generator , args=parameter) 
        
        process_pool.append(p)

    
    
    
    for i , process in enumerate(process_pool):
        process.start() 
        print(f"process {i} start !")
        
    for i , process in enumerate(process_pool):
        process.join() 
        print(f"process {i} end !")
        
    
    
    Assembly(arg.num_workers , arg.s_path , "node_feature","edge_index","edge_weight","labels_COO","labels_CE","opt")
    