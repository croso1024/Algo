# from Benchmark_ import Benchmarker 

# a = ["A","B","F","|","E","|","C","G"]

# print(Benchmarker.MultiVehicle_Cost(3,a) )

a= ["A","D","G","F","C","E","R","W","T","U"]

def adj(l,num) : 
    s = len(l)//num  
    
    for i in range(num-1): 
        
        l.insert((i+1)*s,"|")
    return l    
    
print(adj(a,3) )

    