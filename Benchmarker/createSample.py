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
    
createFromText(6,"longStation.json") 
