from Benchmark_ import Benchmarker
from itertools import permutations,count 
import matplotlib.pyplot as plt 

class Exhaustiver: 

    def __init__(self):
        self.Optimal_cost = float("inf")
        self.Best_solution =None
        self.iteration_step = 1000
        self.Early_stop = 200
        self.Cost_Array = []

    def init_Generator(self,iterable): 
        Generator = permutations(iterable) 
        self.Generator = Generator 
    
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
                cost,solution = Benchmarker._routeCost(candidate)
                if rev: 
                    l = len(candidate)//2 
                    candidate = candidate[l:]+ candidate[:l]
                    cost,solution = Benchmarker._routeCost(candidate)
                    
                else: 
                    cost,solution = Benchmarker._routeCost(candidate)
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
            return self.Optimal_cost , self.Best_solution 


    def plotting(self): 
        #print(self.Cost_Array)
        plt.subplot(1,2,1),Benchmarker.plotting(Benchmarker.SourceGraph)
        plt.subplot(1,2,2),plt.plot(range(len(self.Cost_Array)),self.Cost_Array) 
        plt.show()

Benchmarker.setting()
Benchmarker.Source_graphLoading()
Exhauser = Exhaustiver() 
Exhauser.init_Generator(["B","C","D","E","G","A"]) 
#Exhauser.init_Generator(["1F_start","1F_HenGi","1F_forest","1F_stage","1F_gate_1","1F_willy_destroy","1F_table"]) 
opt_cost,opt_route = Exhauser.evaluate() 
Exhauser.plotting()
