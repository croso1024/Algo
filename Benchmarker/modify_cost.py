import json
import numpy as np 
path = "map/YaTai3_adjency.json"

with open (path,"r") as f : 
    print(f)
    file = json.load(f)
    goal_list =  { v:i  for i,v in enumerate(file["station"]) } 
    size = len(file["station"])
    matrix = np.asarray(file["adjencyMatrix"])
    #goal_list = file["station"]
    print(matrix)
print(goal_list)


#matrix = np.zeros((size,size),dtype=int) 

while 1: 
    source = int(input("source  : ") ) 
    target = int(input("target  : "))
    cost  = int(input("cost : "))
    if cost == 999: 
        break 
    matrix[source][target] = cost 
    matrix[target][source] = cost 
    print(matrix)
    print(goal_list)
with open("map/YaTai_xxx.json","w+") as file: 
    matrix = matrix.tolist()
    json.dump(matrix,file)
print("done")