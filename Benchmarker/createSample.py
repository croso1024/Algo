import numpy  as np 
import json


############# create a map from map , format by willy 
def createFromJSON(input_path,out_path):  
    #with open("map/expo_park.json","r") as file: 
    with open(input_path,"r") as file : 
        data = json.load(file)
    location = list(data["goals"].keys())
    print(location)
    #matrix = np.random.randint(low=0,high=1,size=(2,len(location)))
    # 0812 
    matrix = np.zeros((2,len(location)), dtype=int)
    adj = np.dot(matrix.transpose(),matrix)
    print(matrix)
    print(adj)
    adj = adj.tolist()
    with open(out_path,"w") as file:
        data = {"station":location,"adjencyMatrix":adj}    
        file.write(json.dumps(data))


def hollowMap(adj_matrix,probability) ->list : 
    for i in range(len(adj_matrix))  :    # 0-> size 
        for j in range(len(adj_matrix)) :    # 0 -> size 
            radint = np.random.uniform() 
            if radint < probability : 
                adj_matrix[i][j] = 0  
                adj_matrix[j][i] = 0   
            else : 
                pass 
    return adj_matrix

####### create a random generate map from only text 
def createFromText(size: int , out_path , probability=None): 
    dot  = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    location ,length= dot[:size] , len(dot[:size])
    print(location)
    matrix = np.random.randint(low=0,high = 10 , size= (3,length))
    adj = np.dot(matrix.transpose(),matrix)
    if probability : 
        adj = hollowMap(adj,probability=probability)
    
    adj = adj.tolist() 
    with open(out_path,"w") as file:
        data = {"station":location , "adjencyMatrix":adj}
        file.write(json.dumps(data))







####### create a ssb-like map from text only 

def create_Map_shape1(size: int or list,out_path,peace=1): #--> create map like SSB
    dot1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    dot2 = "abcdefghijklmnopqrstuvwxyz"
    dot3 = "0123456789"
    dot_list = [dot1,dot2,dot3]
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
        matrix = np.random.randint(low =0 ,high = 0,size = (3,length))
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


def createEncodeMap(size: int , out_path , probability=None): 
    
    dot = [ str(i) for i in range(50)]
    
    
    #dot  = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    location ,length= dot[:size] , len(dot[:size])
    print(location)
    #matrix = np.random.randint(low=0,high = 1 , size= (3,length))
    matrix = np.random.rand(3,length)
    matrix.astype(dtype=np.float16)
    adj = np.dot(matrix.transpose(),matrix)
    if probability : 
        adj = hollowMap(adj,probability=probability)
    
    # diagonal zero ! 
    for i in range(size): 
        adj[i][i] = 0 
    
    
    adj = adj.tolist() 
    with open(out_path,"w") as file:
        data = {"station":location , "adjencyMatrix":adj}
        file.write(json.dumps(data))


#createFromText(50,"Relax_big.json",probability=0.6) 
#createFromJSON("YaTai3.json","map/YaTai3_adjency.json")

createEncodeMap(20,"EncodeMap.json")  

# dot1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# dot2 = "abcdefghijklmnopqrstuvwxyz"
# dot3 = "0123456789"
# dot = [dot1,dot2,dot3]

# create_Map_shape1([20,20,10],out_path="building_big.json",peace=3)