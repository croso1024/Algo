
from math import perm
from re import I


def permu(listnode,tail=""): 

    if len(listnode) == 0: 
        
        yield tail
    else: 
        for i in range(len(listnode)):
            yield from permu(listnode[:i]+listnode[i+1:],tail+listnode[i])
    

demo = ["A","B","C"]


a = permu(demo)
print(next(a))
result = list() 
try: 
    while 1:
        value = a.__next__()
        result.append(value)
        print(value)
except: 
    pass 
print(result)