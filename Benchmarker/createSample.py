import numpy  as np 
import json



def createFromJSON(input_path,out_path):  
    #with open("map/expo_park.json","r") as file: 
    with open(input_path,"r") as file : 
        data = json.load(file)
    location = list(data["goals"].keys())
    print(location)
    matrix = np.random.randint(low=0,high=3,size=(2,len(location)))
    adj = np.dot(matrix.transpose(),matrix)
    print(matrix)
    print(adj)
    adj = adj.tolist()
    with open(out_path,"w") as file:
        data = {"station":location,"adjencyMatrix":adj}    
        file.write(json.dumps(data))
        
def createFromText(size: int , out_path): 
    dot  = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    location ,length= dot[:size] , len(dot[:size])
    print(location)
    matrix = np.random.randint(low=0,high = 10 , size= (3,length))
    adj = np.dot(matrix.transpose(),matrix)
    adj = adj.tolist() 
    with open(out_path,"w") as file:
        data = {"station":location , "adjencyMatrix":adj}
        file.write(json.dumps(data))
    
def create_Map_shape1(size: int or list,out_path,dot_list,peace=1): #--> create map like SSB

    if size == int:  
        size =[size] 
        assert peace ==1 , "slice error"    
    else: 
        assert peace == len(size) , "slice error"

    adj_list = [list() for i in range(peace)]
    location =""
    for i,dot in enumerate(dot_list): 
        
        location += dot[:size[i]]
        length =  len(dot[:size[i]])
        print(location,length)
        matrix = np.random.randint(low =1 ,high = 3,size = (3,length))
        adj = np.dot(matrix.transpose(),matrix)
        print(adj.shape)
        adj_list[i] = adj 
    
    adjmatrix = np.zeros( (sum(size),sum(size)) , dtype =int)
    slice_start = 0
    for i,adj in enumerate(adj_list):  
        adjmatrix[slice_start:slice_start+adj.shape[0] , slice_start:slice_start+adj.shape[0]] = adj
        slice_start += adj.shape[0]
    print(adjmatrix)
    adjmatrix = adjmatrix.tolist() 
   
    with open(out_path,"w") as file:
        data = {"station":location , "adjencyMatrix":adjmatrix}
        file.write(json.dumps(data))


#createFromText(6,"longStation.json") 


dot1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
dot2 = "abcdefghijklmnopqrstuvwxyz"
dot3 = "0123456789"
dot = [dot1,dot2,dot3]

create_Map_shape1([20,20,10],out_path="building_big.json",dot_list = dot,peace=3)