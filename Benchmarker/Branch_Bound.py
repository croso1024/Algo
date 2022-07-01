from Benchmark_ import Benchmarker 
import numpy as np 
import time ,json 
import heapq as minheap 

Benchmarker.setting() 
Benchmarker.Source_graphLoading() 
print(Benchmarker.All_pair_cost)
class Node: 
    def __init__(self,sub_solution): 
        self.nodebound = np.inf 

        self.parent = None 
        
        self.location = None 

class DFS_list: 
    def __init__(self): 
        self.subProblem = [] 
        self.node_forSearch = 0 
    def _insert(self,node): 
        self.subProblem.append(node) 
        self.node_forSearch +=1  
    
    def _delete(self,node): 
        self.subProblem.remove(node) 

    
class Branch_Bound: 
    
    def __init__(self,initial_solution): 
        self.search_set = minheap() 
        self.optimal_solution = np.inf 
    
    def evaluate(self) :  # evaluate current node bound  
        self.nodebound = self.paraent.nodebound + Benchmarker.All_pair_cost[self.parent.location][self.location] 
        
    def search(self) : # findout all branch that node can search , and evaluate them