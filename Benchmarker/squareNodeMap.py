import numpy as np 
import json ,math 
from numpy.random import rand as r
from numpy.random import randint as rint


class node : 
    def __init__(self,x,y): 
        self.x = x 
        self.y = y 
        print(f"node : ({x},{y})")
        
        
    def coordinate(self) -> tuple : 
        return (self.x,self.y)
        
"""
calculate the distance between two nodes , distance collector is for plot 
"""
def distance(node1,node2,distance_collector=None) -> float : 
    dis = math.sqrt(  pow((node1.x - node2.x),2) + pow((node1.y-node2.y),2) )
    if distance_collector:distance_collector.append(dis) 
    return dis 
                    
                     
    
def node_coordinateFunc(mode:str) -> node : 
    if mode == "unit": 
        return node(x=r(),y=r())
    elif mode == "big-unit": 
        return node(x=r()*10,y=r()*10)
    elif mode == "discrete" : 
        return node(x=rint(1,30),y=rint(1,30))
    elif mode == "irregular" : 
        return node(x=float(pow(rint(low=1,high=10),1+r())),y=float(pow(rint(low=1,high=10),1+r())))

def squareMap(node_num:int, output_path:str ,mode = "unit"): 
    
    station_list = [str(i) for i in range(node_num)]
    nodes = [node_coordinateFunc(mode) for i in range(node_num) ]
    
    distanceCollector = [] 

    adjency_matrix = np.zeros((node_num,node_num) , dtype=float) 
    
    for i in range(node_num): 
        for j in range(i,node_num): 
            adjency_matrix[i][j] = adjency_matrix[j][i] = distance(nodes[i],nodes[j],distance_collector=distanceCollector) 
    
    with open(output_path,"w") as file : 
        data = {
            "station":station_list, 
            "Depot" : "0" , 
            "adjencyMatrix":adjency_matrix.tolist() ,
            "node_coordinate" : [n.coordinate() for n in nodes]
        }
        file.write(json.dumps(data)) 

if __name__ == "__main__": 
    squareMap(10,"DatasetGenerate/IG_test.json")

# with open("DatasetGenerate/trainMap_square.json", "r") as file : 
#     data = json.load(file) 
#     print(data["adjencyMatrix"][7][3])