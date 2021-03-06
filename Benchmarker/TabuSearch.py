from itertools import combinations ,permutations

import numpy as np 
from Benchmark_ import Benchmarker
import time 
from collections import namedtuple 
import matplotlib.pyplot as plt 
class Tabu_Search: 

    #cost_function = Benchmarker._routeCost
    tabu_size = 30 
    
    move = namedtuple("move",["index1","value1","index2","value2"])

    def __init__(self,initial_solution,iteration_num,vehicle_num=1):
        
        self.best_solutionCost = np.inf 
        self.best_solution = None 
        self.tabu = []  
        
        self.current_solution = initial_solution  # --> represent the current position (solution) 
        self.iteration_num = iteration_num
        self.vehicle_num = vehicle_num
        
        self.solution_log = [] 
        if vehicle_num > 1 : 
            self.cost_function = Benchmarker.MultiVehicle_Cost 
            self.MultiVehicle_adjust() 
            
        else : 
            self.cost_function = Benchmarker._routeCost 
        
    def get_Neighborhood(self):     
        # 找到一個解的所有neighborhood作為generator
        # 這裡直接用list後相當於沒有generator的特性了, 是一次列出所有可能 C(n,2) 為 O(n^2) 
        swap_generator = combinations(range(len(self.current_solution)),2)
        self.swap_list =  list(swap_generator)   
        
    def MultiVehicle_adjust(self): 
        step = len(self.current_solution)//self.vehicle_num 
        for i in range(self.vehicle_num-1): 
            self.current_solution.insert((i+1)*step,"|") 

        
    def swap(self,solution,move):   
        solution[move.index1] , solution[move.index2] = solution[move.index2] ,solution[move.index1] 
        

    def tabu_rule(self,solution,move):  # return wheather this move obey the tabu rule  
        for tabu in self.tabu:  
            if tabu.index1 == move.index1 and tabu.value1 == solution[move.index1] and \
                tabu.index2 == move.index2 and tabu.value2 == solution[move.index2] : 
                return True 
        return False 

    def Iteration(self): 
        """ 若今天這一步操作會使得cost低於歷史最佳,則無論有沒有在tabu list都更新這一步
            若cost低於鄰近最佳,高於歷史最佳, 但存在於tabu list中,則不選擇這組作為下一步
        """
        # step1. 取得目前解的所有neighborhood 
        self.get_Neighborhood() 
        # step2. 初始化目前的這個解周圍的最佳解與非Tabu最佳解
    
        best_solutionCost = np.inf 
        best_solution = None 
        best_move = None

        nonTabu_best_solutionCost = np.inf 
        #nonTabu_best_solution = None 
        nonTabu_best_move = None

        
        for swapIndex in self.swap_list:  
        #step3. 取出一個neighborhood ,計算其cost,是否達到鄰近最佳,非禁忌鄰近最佳 （兩件事情是獨立的）
            index1,index2 = swapIndex  
            move = self.move(index1,self.current_solution[index1],index2,self.current_solution[index2])
            neighborhood = self.current_solution.copy() 
            #print(f"neighborhood before swap {neighborhood}")
            self.swap(neighborhood,move) 
            #print(f"neighborhood after swap {neighborhood}")
            #print("-----------------------------------------")
            neighborhood_cost = self.cost_function(neighborhood,self.vehicle_num)[0]

            is_tabu = self.tabu_rule(neighborhood,move) 

            if neighborhood_cost < best_solutionCost: 
                best_solutionCost = neighborhood_cost 
                best_solution = neighborhood.copy()   
                best_move = move 
                
            if not is_tabu and neighborhood_cost < nonTabu_best_solutionCost : 
                nonTabu_best_solutionCost = neighborhood_cost
                #我們真的需要的是歷史最佳解,因此只在歷史最佳有突破時保留當下的解,如果沒有突破的話單純只是前進到下個解
                #nonTabu_best_solution = neighborhood.copy()  
                nonTabu_best_move = move
        
        # step4. 此時已經取得目前解的鄰近最佳與非禁忌鄰近最佳, 檢查鄰近最佳是否優於歷史最佳, 沒有的話才用非禁忌鄰近最佳更新目前解
        if best_solutionCost < self.best_solutionCost : 
            self.best_solutionCost = best_solutionCost 
            self.best_solution = best_solution
            self.swap(self.current_solution,best_move) 

            if best_move in self.tabu: 
                self.tabu.remove(best_move) 
            self.tabu.insert(0,best_move) 
        
        else: 
            self.swap(self.current_solution,nonTabu_best_move) 
            self.tabu.append(nonTabu_best_move)  
        
        if len(self.tabu) > self.tabu_size: 
            self.tabu.pop() 
        self.solution_log.append(self.best_solutionCost)
        self.iteration_num +=1 

    def Optimization(self): 
        for iteration  in range(self.iteration_num):
            self.Iteration()
        
        print(f"best solution: {self.best_solution}")
        print(f"best solution cost: {self.best_solutionCost}")
        plt.plot(range(len(self.solution_log)) , self.solution_log)
        plt.show()
if __name__ =="__main__": 
    Benchmarker.setting() 
    Benchmarker.Source_graphLoading() 
    Tabu = Tabu_Search(initial_solution=["B","A","E","G","D","K","I","H","C","L","M","O","Q","R"],iteration_num=10,vehicle_num=4)
    #Tabu = Tabu_Search(initial_solution=["G","D","A","I","C","L"],iteration_num=20)
    Tabu.Optimization()