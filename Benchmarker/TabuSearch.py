from itertools import combinations ,permutations
from shutil import move
import numpy as np 
from Benchmark_ import Benchmarker
import time 
from collections import namedtuple 

class Tabu_Search: 

    cost_function = Benchmarker._routeCost
    tabu_size = 30 
    iteration_num = 10
    move = namedtuple("move",["index1","value1","index2","value2"])

    def __init__(self,initial_solution):
        self.best_solutionCost = np.inf 
        self.best_solution = None 
        self.tabu = []  
        self.current_solution = initial_solution  # --> represent the current position (solution) 
        
    def get_Neighborhood(self):     
        # 找到一個解的所有neighborhood作為generator
        # 這裡直接用list後相當於沒有generator的特性了, 是一次列出所有可能 C(n,2) 為 O(n^2) 
        swap_generator = combinations(range(len(self.current_solution)),2)
        self.swap_list =  list(swap_generator)   
        
    def swap(self,solution,move):   
        solution[move.index1] , solution[move.index2] = solution[move.index2] ,solution[move.index1] 
        

    def tabu_rule(self,solution,move): 
        for tabu in self.tabu:  
            if tabu.index1 == move.index1 and tabu.value1 == solution[move.index1] and \
                tabu.index2 == move.index2 and tabu.value2 == solution[move.index2] : 
                return True 
        return False 

    def Iteration(self): 
        """ 若今天這一步操作會使得cost低於歷史最佳,則無論有沒有在tabu list都更新這一步
            若cost低於鄰近最佳,高於歷史最佳, 但存在於tabu list中,則不選擇這組作為下一步
        """

        best_solutionCost = np.inf 
        best_solution = None 
        best_move = None

        nonTabu_best_solutionCost = np.inf 
        nonTabu_best_solution = None 

        nonTabu_best_move = None

        for swapIndex in self.swap_list:  
            index1,index2 = swapIndex  
            move = self.move(index1,self.current_solution[index1],index2,self.current_solution[index2])
            neighborhood = self.current_solution.copy() 
            self.swap(neighborhood,move) 
            neighborhood_cost = self.cost_function(neighborhood)

            is_tabu = self.tabu_rule(neighborhood,move) 

            if neighborhood_cost < best_solutionCost: 
                best_solutionCost = neighborhood_cost 
                best_solution = neighborhood.copy()   
                best_move = move 
                
            if not is_tabu and neighborhood_cost < nonTabu_best_solutionCost : 
                nonTabu_best_solutionCost = neighborhood_cost
                nonTabu_best_solution = neighborhood.copy()  
        
        if best_solutionCost < self.best_solutionCost : 
            self.best_solutionCost = best_solutionCost 
            self.best_solution = best_solution
            self.swap(self.current_solution,best_move) 

            if best_move in self.tabu: 
                self.tabu.remove(best_move) 
            self.tabu.insert(best_move) 
        
        else: 
            self.swap(self.current_solution,nonTabu_best_move) 
            self.tabu.append(nonTabu_best_move)  
        
        if len(self.tabu) > self.tabu_size: 
            self.tabu.pop() 
        
        self.iteration_num +=1 

        