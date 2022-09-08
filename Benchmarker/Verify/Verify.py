import sys

Path = "/home/croso1024/python_code/Algorithms/Benchmarker"
if not Path in sys.path : sys.path.append(Path)

from TSPGA import Genetic_Algorithms
from Benchmark_ import Benchmarker 
from TabuSearch import Tabu_Search
import numpy as np 
import time 
import matplotlib.pyplot as plt 


Map_set_small =  ["../map/Relax_small.json","../map/Tight_small.json","../map/building_small.json" ]

Map_set_big=[ "../map/Relax_big.json" , "../map/Tight_big.json","../map/building_big.json"] 

# for map in Map_set_small :
Benchmarker.setting("map/Relax_big.json") 
Benchmarker.Source_graphLoading()

#     initial_solution = list(np.random.permutation(Benchmarker.station_list))
    
#     temp = initial_solution.copy() 
    
#     for vehicle_num in range(1,4): 
        
#         print(f"vehicle num: {vehicle_num}")
GA_log = []
GA_time = [] 
TS_log = []
TS_time = []

Verify_times = 15

for i in range(Verify_times): 
    print(f"Tabu--------iter {i}-----")
    Tabu = Tabu_Search(initial_solution=list(np.random.permutation(Benchmarker.station_list)),iteration_num=60,vehicle_num=4)
    Tabu.Optimization(plotting=0)
    TS_log.append(Tabu.best_solutionCost)
    TS_time.append(Tabu.CostTime) 
    

# for i in range(Verify_times): 
#     print(f"Tabu--------iter {i}-----")
#     Tabu = Tabu_Search(initial_solution=list(np.random.permutation(Benchmarker.station_list)),iteration_num=100,vehicle_num=4)
#     Tabu.Optimization(plotting=0)
#     GA_log.append(Tabu.best_solutionCost)
#     GA_time.append(Tabu.CostTime) 
    


for i in range(Verify_times): 
    print(f"GA--------iter {i}-----")
    GA = Genetic_Algorithms.Create_GA_Instance(  initial_solution=list(np.random.permutation(Benchmarker.station_list)), vehicle_num=4)
    GA.Optimization(plotting=0)
    GA_log.append(GA.solution_fitness)
    GA_time.append(GA.CostTime) 
    
    

########## Plot ##############

fig , axis1 = plt.subplots() 
plt.title("Cost&Time -- 50 instance Relax big ")  
plt.xlabel("Sample") 
axis2 = axis1.twinx()
    
    
axis1.set_ylabel("Route Cost" ) 
axis2.set_ylabel("Cost time")
axis2.set_ylim(0,1)

TSCost = axis1.plot(range(len(TS_log)),TS_log,label="TS Cost" , color="blue",marker="o") 
GACost = axis1.plot(range(len(GA_log)),GA_log ,label="GA Cost", color="orange",marker="^") 
#legendAxis1 = axis1.legend([TSCost,GACost],["TS Cost" , "GA Cost"],loc="upper left")


TSTime = axis2.plot(range(len(TS_time)),TS_time,label="TS Time", color="Navy",linestyle="dashed")
GATime = axis2.plot(range(len(GA_time)),GA_time ,label="GA Time" ,color="red" , linestyle="dashed")
#legendAxis2 = axis2.legend([TSTime,GATime],["TS Time","GA Time"] , loc="lower right")

lines = TSCost + GACost +TSTime + GATime 
labels = [l.get_label() for l in lines]  
plt.legend(lines,labels,loc=0) 
plt.show()
