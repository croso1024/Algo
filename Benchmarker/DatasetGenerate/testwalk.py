import os 

dirs = list(filter( lambda x : os.path.isdir(x) , list(os.listdir("/home/croso1024/python_code/GNN/Dataset/Square_test"))) )
print(dirs)