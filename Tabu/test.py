

with open("city.txt","r") as f : 
    for line in f.readlines(): 
        print(line.splitlines())
    
    