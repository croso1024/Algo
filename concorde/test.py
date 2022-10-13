from concorde.tsp import TSPSolver 
from concorde.tests.data_utils import get_dataset_path 
from itertools import permutations 
# frame = get_dataset_path("berlin52")  
# solver = TSPSolver.from_tspfile(frame)


def cal(seq,adjM,cycle=True): 
    
    total_cost = 0 
    
    for step in range(len(seq)-1 ) : 
        total_cost += adjM[seq[step]][seq[step+1]]
       # print(total_cost)
    if cycle : 
        total_cost+= adjM[seq[-1]][seq[0]]
     
    #print(total_cost)        
    return total_cost






import numpy as np 
#dist_matrix = np.array([[0, 1, 2, 3,2], [1, 0, 3, 4,5], [2, 3, 0, 1,5], [3, 4, 1, 0,2] , [1,4,3,2,0]] ,dtype=np.int32)
dimension = 20
a = np.random.randint(low=1,high=5 , size=(1,dimension) , dtype= np.int32) 
#a = np.ones((1,dimension) ,dtype=np.int32)
dist_matrix = a.transpose().dot(a) 
for i in range(dimension) : 
    dist_matrix[i][i] = 0 
print(dist_matrix) 


# solver only supports integral edge weights, so here float will be rounded to two
# decimals, multiplied by 100 and converted to integer
solver = TSPSolver.from_data(dist_matrix=dist_matrix)

solution = solver.solve() 
print('--------------------')
print(solution.tour , type(solution.tour))
print('--------------------')
print(solution.optimal_value)

# best = float("inf")  
# for sol in permutations(list(range(dimension)) , dimension): 
    
#     cost = cal(list(sol),dist_matrix,cycle=True) 
    
#     if cost < best : 
#         best = cost    
#     else: pass 

# print(best) 
print(solution.optimal_value)
    

