from Benchmark_ import Benchmarker
from itertools import permutations,count 
import matplotlib.pyplot as plt 
import time , math 
import numpy as np
class Exhaustiver: 

    def __init__(self , initial_solution ,iteration_num ,vehicle_num,early_stop ,GenerateMode=False):
        self.Optimal_cost = float("inf")
        self.Best_solution =None
        self.initial_solution = initial_solution 
        
        self.iteration_step = iteration_num if iteration_num < math.factorial(len(initial_solution)+(vehicle_num-1)) else math.factorial(len(initial_solution)+(vehicle_num-1))
        print(self.iteration_step)
        if early_stop :
            self.Early_stop = iteration_num//3
        else:
            self.Early_stop = iteration_num
        self.Cost_Array = []
        self.vehicle_num = vehicle_num
        
        
        self.GenerateMode = GenerateMode
        
        if self.vehicle_num > 1 :
            self.cost_function = Benchmarker.MultiVehicle_Cost
            self.MultiVehicle_adjust() 
            
        else : 
            print("use single vehicle")
            
            if self.GenerateMode:
                self.cost_function =lambda nodelist,vehicleNum : Benchmarker._routeCost_DataGen(nodelist, depot_start=False,cycle=True)
               
            else: 
                self.cost_function = Benchmarker._routeCost if not self.GenerateMode else Benchmarker._routeCost_DataGen

            
            
        self.init_Generator(self.initial_solution) 
    
    
    def init_Generator(self,iterable): 
        Generator = permutations(iterable) 
        self.Generator = Generator 
        
    def MultiVehicle_adjust(self): 
        step = len(self.initial_solution)//self.vehicle_num 
        for i in range(self.vehicle_num-1): 
            self.initial_solution.insert((i+1)*step,"|") 
        print(self.initial_solution)
            
    def getSolution(self): 
        sol = list(self.Generator.__next__() )
        #print(sol)
    
        return sol

    def evaluate(self,plotting=False):
        t_start = time.time()
        step_count = 0
        stop_count = 0
        rev_count = 0
        rev = False 
        try:
            for step in range(self.iteration_step):
                
                candidate = self.getSolution()
                solution = candidate.copy()
                
                if rev: 
                    l = len(candidate)//2 
                    candidate = candidate[l:]+ candidate[:l]
                    #cost,solution = Benchmarker._routeCost(candidate)
                    cost = self.cost_function(candidate,self.vehicle_num)[0]
                    
                else: 
                    #cost,solution = Benchmarker._routeCost(candidate)
                    cost = self.cost_function(candidate,self.vehicle_num)[0]
                   
                    # TODO reverse
                
                if cost < self.Optimal_cost: 
                    self.Optimal_cost = cost 
                    self.Best_solution = solution
                    stop_count = 0
                    rev_count = 0
                else:  
                    stop_count +=1 
                    rev_count +=1 
                
                self.Cost_Array.append(self.Optimal_cost) 
                
                if rev_count >= 8: 
                     rev = not rev 
                     rev_count = 0
                     #print("--------REV---------")
                if stop_count >= self.Early_stop: 
                    #print("early stop at {}".format(step))
                    break 
                step_count +=1
        except : 
            print("error")
        finally: 
            # 0921 加入cycle的動作放在encodeing labels的時候
            if self.GenerateMode : 
               self.Best_solution.append(self.Best_solution[0])
            
            #print("Best solution: {} , cost: {} " .format(self.Best_solution,self.Optimal_cost))
            #print(f"total step: {step_count}")
            CostTime = time.time() - t_start
            self.CostTime = CostTime
            #print(self.CostTime)
            if plotting:
                self.plotting()
            
            return self.Optimal_cost , self.Best_solution 


    def plotting(self): 
        #print(self.Cost_Array)
        
        # plt.subplot(1,2,1),Benchmarker.plotting(Benchmarker.SourceGraph)
        # plt.subplot(1,2,2),plt.plot(range(len(self.Cost_Array)),self.Cost_Array) 
        # plt.show()
        testing_setting = f"optimizer: Exhaustiver\n\nCost:{self.Optimal_cost}\n\niterations :{self.iteration_step}\n\nvehicle_num:{self.vehicle_num}\n\nCost time: {self.CostTime}\n\nCriterion:MinSum" 
       
        
        Benchmarker.plotting(Benchmarker.SourceGraph,solution_path=self.Best_solution,
                             optimizer="Exhaustiver",Cost_log=self.Cost_Array,testing_set=testing_setting,vehicle_num=self.vehicle_num)
        
if __name__ == "__main__": 
        
    Benchmarker.setting(setting_file_path="map/EncodeMap.json")
    Benchmarker.Source_graphLoading()


    Exahuser = Exhaustiver(initial_solution=["3","2","4","6","9","12","11","15"],iteration_num=362880,vehicle_num=1,early_stop=False,GenerateMode=True)

    #Exahuser = Exhaustiver(initial_solution=["B","J","E","H","P","M","G","O","C"],iteration_num=40000,vehicle_num=1,early_stop=False)
    #Exahuser = Exhaustiver(initial_solution=["f","G","S","m","q","s","K","T","P","A","B","D","E","a","b","c","Y","Z","x","I"],iteration_num=3000,vehicle_num=4,early_stop=False)
    #Exahuser = Exhaustiver(initial_solution=["A","1","c","b","e","2","E","C","d","4","G"],iteration_num=39916800,vehicle_num=1,early_stop=False)
    Exahuser.evaluate(plotting=True)

    #print(Exahuser.cost_function(['G', 'D', 'A', 'I', 'C', 'L']))
    # for i in range(10): 
    #    print(f"--------- iter {i} ------")
    #    Exahuser = Exhaustiver(initial_solution=list(np.random.permutation(Benchmarker.station_list)),iteration_num=36800,vehicle_num=3,early_stop=False)
    #    Exahuser.evaluate(plotting=0)