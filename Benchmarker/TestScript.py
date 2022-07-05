from Benchmark_ import Benchmarker

from TabuSearch import Tabu_Search
from Exhaustive_Slover import Exhaustiver
from Branch_Bound import BranchBound
from time import time


Map_set_small =  ["map/Relax_small.json","map/Tight_small.json","map/building_small.json" ]

Map_set_big=[ "map/Relax_big.json" , "map/Tight_big.json","map/building_big.json"]   

vehicle_set = [1,2,4]
iteration_Tabu = 30 
iteration_Exhau = 2000
#initial_solution_small = ["A","E","G","H","J","K","N","B","F","O"]
initial_solution_small = ["A","C","a","E","d","G","c","H","J","k","K","w","N","B","Y","F","O","W","t","e"]



for map in Map_set_big: 
    Benchmarker.setting(map) 
    Benchmarker.Source_graphLoading()

    for vehicle_num in vehicle_set: 
        print("vehicle ",vehicle_num)

        init_s = initial_solution_small.copy()
        Exhaus = Exhaustiver(init_s,iteration_num=iteration_Exhau,vehicle_num=vehicle_num,early_stop=False)
       
        Exhaus.evaluate(plotting=True) 
     

        init_s = initial_solution_small.copy()
        Tabu = Tabu_Search(init_s,iteration_num=iteration_Tabu,vehicle_num=vehicle_num)
        
        Tabu.Optimization(plotting=True)
        
        if vehicle_num == 0 : 
            init_s = initial_solution_small.copy()
            BB = BranchBound(init_s,vehicle_location="A")
            BB.main(plotting=True)
  
        else : 
            pass