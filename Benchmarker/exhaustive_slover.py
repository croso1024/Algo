
from Benchmark_ import Benchmarker 
import matplotlib.pyplot as plt
def _slover(nodelist):
    optimal_cost = float("inf")
    best_sol = None
    stoping_count = 0
    cost_array = []
    def exhaustive(nodelist,sol=""): 
        nonlocal optimal_cost,best_sol,cost_array,stoping_count
        if stoping_count >=50: 
        
            return 
        else:
            if len(nodelist) == 0: 
                print("---------------------")
                print("optimal cost now {}".format(optimal_cost))
                cost,solution = Benchmarker._routeCost(sol)
                if cost >= optimal_cost: 
                    stoping_count+=1 
                
                if cost < optimal_cost : 
                    optimal_cost = cost 
                    best_sol = solution
                    stoping_count=0
                else: 
                    pass 
                
                cost_array.append(optimal_cost)
            else: 
                for i in range(len(nodelist)): 
                    exhaustive(nodelist[:i]+nodelist[i+1:],sol+nodelist[i])
    exhaustive(nodelist)
    return optimal_cost,best_sol,cost_array

Benchmarker.setting()
Benchmarker.Source_graphLoading()
bestCost,bestSol,cost_array = _slover(["A","C","D","E","G","F"])
print("best cost: {} , best solution :{} ".format(bestCost,bestSol))
f1 =  plt.subplot(1,2,1) ,Benchmarker.plotting(Benchmarker.SourceGraph)
f2 =  plt.subplot(1,2,2) ,plt.plot(range(len(cost_array)),cost_array)
plt.show()