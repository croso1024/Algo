
# from Benchmark_ import Benchmarker 

# a = ["A","B","F","|","E","|","C","G"]

# print(Benchmarker.MultiVehicle_Cost(3,a) )

# a= ["A","D","G","F","C","E","R","W","T","U"]

# def adj(l,num) : 
#     s = len(l)//num  
    
#     for i in range(num-1): 
        
#         l.insert((i+1)*s,"|")
#     return l    
    
# print(adj(a,3) )

import heapq as h 
class node: 
    def __init__(self,value,info):
        self.value = value
        self.info = info

heap = []
a = node(2,"hi i am 2")
b = node(5,"i am 54")
c = node(9,"memme 9")
d = node(1,"wew 1 ")

for i in [a,b,c,d]:
    h.heappush(heap ,(i.value,i))

for i in range(4): 
    print(h.heappop(heap))