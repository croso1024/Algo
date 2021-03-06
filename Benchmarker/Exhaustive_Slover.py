from Benchmark_ import Benchmarker
from itertools import permutations,count 
import matplotlib.pyplot as plt 

class Exhaustiver: 

    def __init__(self , initial_solution ,iteration_num ,vehicle_num):
        self.Optimal_cost = float("inf")
        self.Best_solution =None
        self.initial_solution = initial_solution 
        
        self.iteration_step = iteration_num
        self.Early_stop = iteration_num//3
        
        self.Cost_Array = []
        self.vehicle_num = vehicle_num
        
        if self.vehicle_num > 1 :
            self.cost_function = Benchmarker.MultiVehicle_Cost
            self.MultiVehicle_adjust() 
            
        else : 
            print("use single vehicle")
            self.cost_function = Benchmarker._routeCost 
        
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
        print(sol)
    
        return sol

    def evaluate(self):
        step_count = 0
        stop_count = 0
        rev_count = 0
        rev = False 
        try:
            for step in range(self.iteration_step):

                candidate = self.getSolution()
                print(candidate)
                
                #cost,solution = Benchmarker._routeCost(candidate)
                cost,solution= self.cost_function(candidate,self.vehicle_num)
                
                print("ttt")
                if rev: 
                    l = len(candidate)//2 
                    candidate = candidate[l:]+ candidate[:l]
                    #cost,solution = Benchmarker._routeCost(candidate)
                    cost,solution= self.cost_function(candidate,self.vehicle_num)
                    
                else: 
                    #cost,solution = Benchmarker._routeCost(candidate)
                    cost,solution= self.cost_function(candidate,self.vehicle_num)
                    # TODO reverse
                print("abs")
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
                     print("--------REV---------")
                if stop_count >= self.Early_stop: 
                    print("early stop at {}".format(step))
                    break 
                step_count +=1
        except: 
            print("error")
        finally: 
            print("Best solution: {} , cost: {} " .format(self.Best_solution,self.Optimal_cost))
            print(f"total step: {step_count}")
            self.plotting()
            
            return self.Optimal_cost , self.Best_solution 


    def plotting(self): 
        #print(self.Cost_Array)
        
        plt.subplot(1,2,1),Benchmarker.plotting(Benchmarker.SourceGraph)
        plt.subplot(1,2,2),plt.plot(range(len(self.Cost_Array)),self.Cost_Array) 
        plt.show()

Benchmarker.setting()
Benchmarker.Source_graphLoading()

Exahuser = Exhaustiver(initial_solution=["G","D","A","I","C","L"],iteration_num=3200,vehicle_num=3)

Exahuser.evaluate()

#print(Exahuser.cost_function(['G', 'D', 'A', 'I', 'C', 'L']))
