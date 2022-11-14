

import matplotlib.pyplot as plt 
import numpy as np 
import torch 



def Edge_distribution(batch_of_graph:np.array , plot = True) : 
    statistic = [] 
    for graph in batch_of_graph : 
        print(graph)
        edges = compute_edge(graph) 
        for i in edges: statistic.append(i) 
    if plot : 
        plt.hist(statistic,bins=20) 
        plt.show()
    else : 
        pass

def compute_edge(graph) : 
    container = list() 
    for i in range(len(graph)): 
        for j in range(i+1,len(graph)):   
            
            container.append(graph[i][j].item()      )  
    return container 

