import numpy  as np 
import json

with open("map/expo_park.json","r") as file: 
    data = json.load(file)
location = list(data["goals"].keys())
print(location)
matrix = np.random.randint(low=0,high=3,size=(2,len(location)))
adj = np.dot(matrix.transpose(),matrix)
print(matrix)
print(adj)
adj = adj.tolist()
with open("Adjency2.json","w") as file:
    data = {"station":location,"adjencyMatrix":adj}    
    file.write(json.dumps(data))