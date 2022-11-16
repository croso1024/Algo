from multiprocessing import Process 
import time 
from random import randint as r 

def sleeppp(number,n):  
    print(f"process {number} start sleep")
    time.sleep(n) 
    
    print(f"process {number} wake up ")

    
p_set = list()
for i in range(5): 

    p = Process(target=sleeppp , args=(i,r(3,5)) )
    p_set.append(p)
p_set.append(Process(target=sleeppp , args=(11,10) ))

for i,p in enumerate(p_set): 
    print(i,"start")
    p.start() 

print("i am main")
for i,p in enumerate(p_set): 
    print(i,"join")
    p.join()
    
print("continue")