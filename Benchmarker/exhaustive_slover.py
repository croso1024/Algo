
def SolutionPool(nodelist):
    def exhaustive(nodelist,tail=""): 
        if len(nodelist) == 0: 
            #print(list(tail) )
            pool.append(list(tail)) 
        else: 
            for i in range(len(nodelist)): 
                exhaustive(nodelist[:i]+nodelist[i+1:],tail+nodelist[i])
    pool = []
    exhaustive(nodelist)
    
    return pool

print(SolutionPool(["A","B","D","C"]))
