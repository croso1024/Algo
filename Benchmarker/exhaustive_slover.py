import Benchmark_

def _exhaustive_slover(nodelist):
        optimal_cost = float("inf")
        best_sol = None
        stoping_count = 0
        cost_array = []
        def exhaustive(nodelist,sol=""): 
            nonlocal optimal_cost,best_sol,cost_array,stoping_count
            if stoping_count >=20: 
                
                return 
            else:
                if len(nodelist) == 0: 
                    print("---------------------")
                    print("optimal cost now {}".format(optimal_cost))
                    cost,solution = Benchmark_.Benchmarker._routeCost(sol)
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
