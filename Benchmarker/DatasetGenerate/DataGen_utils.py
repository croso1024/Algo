from datetime import datetime 
import networkx as nx 
import numpy as np 
from concorde.tsp import TSPSolver 

import argparse  ,torch , time 
from tqdm import tqdm 
import os ,shutil,json

"""
    2022 - 11 - 13 ---------------------------------------------------------------------
    A standard TSP instance generator utilize function package  ,    
    
    ##### 1. multi-process 

        Use the multi-process create the sub-task directory , combined at every process done   

    ##### 2. COO-format edge labels enable ! 

        use the labels_CE & subGraph( return from GraphFeature ) to produce the COO-format edge connectively labels 
    
    2022 - 11 - 26 ---------------------------------------------------------------------
    
    Add a flag to decide wheather the self-loop is enable , 
    and add edgeIndex as the argument in COO format transform 
    cause we want to use 2 x edge_num ( use edge_index ) to generate the labels_COO 
    
    2023 - 01 - 04 --------------------------------------
    
    1.Remove the graph loading from Benchmarker, replace by the graphLoading
    2.Add node coordinate extract in graph feature , to fixed the node-feature representation to learning 
"""


def GraphLoading(m_path):  
    sourceGraph = nx.Graph() 
    with open(m_path ,'r') as file : 
        graph = json.load(file) 
        nodes = graph['station']
        dimension = len(nodes)
        adjencyMatrix = graph['adjencyMatrix']
        node_coordinate = graph['node_coordinate']
        assert dimension == len(adjencyMatrix[0])  
         
    for i,node in enumerate(nodes): 
        sourceGraph.add_node(node , node_coordinate = node_coordinate[i])
    for i , node  in enumerate(nodes): 
        for j in range(i+1 , dimension): 
            cost = adjencyMatrix[i][j] 
            if cost : 
                sourceGraph.add_edge(nodes[i],nodes[j] , weight=cost)
    all_pair_cost = dict(nx.all_pairs_dijkstra_path_length(sourceGraph))  
    all_pair_path = dict(nx.all_pairs_dijkstra_path(sourceGraph))
    Stations = list(sourceGraph.nodes())
    return sourceGraph ,Stations, all_pair_cost , all_pair_path 

def Sampler(Stations , size=5) : # --> generate the random list  ! just for single vehicle 
    out =  list(np.random.choice(Stations , size , replace=False) )
    #print(f"Debug Sampler:{out}")
    
    return out


def GraphFeature(seq,SourceGraph) : # --> output the node-feature matrix ( dijkstra )
    
    subGraph = nx.subgraph(SourceGraph,seq) 
    sub_dijkstra = dict(nx.all_pairs_dijkstra_path_length(subGraph)) 
    ###### Node Feature extract ###############################################
    
    seq_sort = sorted(seq , key = lambda x : int(x)) 
    #print(f"Debug : seq-sort : {seq_sort}")

    # reindex : a reference look-table 
    reindex = {seq[i] : seq_sort.index(seq[i]) for i in range(len(seq))}  
    
    node_coordinates = np.zeros( (len(seq),2) , dtype=np.float32 ) 
    
    for node in subGraph.nodes() : 
        node_coordinates[ reindex[node] ] = subGraph.nodes[node]['node_coordinate']
        
    # print(f"Debug : subGraph.nodes() {subGraph.nodes()}")
    # print(f"Debug : node-coordinate : {node_coordinates}")
    # print(f"Debug : re-index:{reindex}")
    # print(f"Debug : sub dijkstra :{sub_dijkstra}")

    Dijkstra_nodeFeature = np.zeros( (len(seq),len(seq) ) , dtype = np.float32)
    # --> src & dst node is "str" node and not yet normalized 
    # --> need use reindex 
    for src_node in sub_dijkstra :
        
        for dst_node in sub_dijkstra[src_node]: 

            Dijkstra_nodeFeature[ reindex[src_node] ][  reindex[dst_node] ]  = sub_dijkstra[src_node][dst_node] 
    
    #print(f"Debug : Dijkstra node feature : \n {Dijkstra_nodeFeature}")


    ############ Edge Featrue extract ###########
    edgeIndex = list() 
    edgeWeight = list() 
    
    for u,v in subGraph.edges: 
        edgeWeight.append(sub_dijkstra[u][v])
        edgeWeight.append(sub_dijkstra[v][u])
        edgeIndex.append([reindex[u] , reindex[v]])
        edgeIndex.append([reindex[v] , reindex[u]])
        
    return Dijkstra_nodeFeature , edgeIndex , edgeWeight , subGraph , reindex , node_coordinates


def concorde_Solver(dist_matrix , vehicle_num=1) -> list:     #--> output opt , y_CE

    Solver = TSPSolver.from_data(dist_matrix=dist_matrix.copy())
    
    output = Solver.solve() 
    
    #print(f"Debug output-tour : {output.tour}")

    #print(f"Debug output cost : {output.optimal_value}")
    return output.tour , float(output.optimal_value/100)


# check this edge is in labels_CE , note the tmp is a duplicate of labels_CE
def CCO_have_edge(tmp , u,v) -> bool : 
    # tmp = label_CE[:]
    # tmp.append(tmp[0])
    
    for idx in range(len(tmp)-1): 
        y = tmp[idx:idx+2] 
        if  y == [u,v] or y ==[v,u] : 
            return True 
        else : pass 
        
    return False      
""" 
    2022-11-26 modift , info see above 
    
def COO_transform(label_CE , subGraph,indexTable): 
    tmp = label_CE[:].tolist()
                      
    tmp.append(tmp[0])
                      
    COO_edge_labels = [] 
    print(len(subGraph.edges))
    
    for u,v in subGraph.edges: 
        if CCO_have_edge(tmp,indexTable[u],indexTable[v] ) : 
            COO_edge_labels.append(1)  
        else:                          
            COO_edge_labels.append(0)  
    # print(COO_edge_labels)           
                                       
    return COO_edge_labels             
"""                                    

def COO_transform(label_CE , subGraph,indexTable , edgeIndex): 
    tmp = label_CE[:].tolist()
                      
    tmp.append(tmp[0])
                      
    COO_edge_labels = [] 

    for u , v in edgeIndex : 
        if CCO_have_edge(tmp , u ,v ): 
            COO_edge_labels.append(1) 
        else : 
            COO_edge_labels.append(0) 
     
    return COO_edge_labels       
                                       
def debug_logger(log_path , info) :    
    t = datetime.now().isoformat()     
    with open(log_path ,"a") as file : 
                                       
        file.write(str(datetime.now()))
        file.write(json.dumps(info))
        file.write("\n")
        
                                       
def Generator(                         
                    SourceGraph,       
                    Stations ,         
                    All_pair_cost ,    
                    sampleSize = 20 ,  
                    dataSize=100 ,     
                    save=True ,        
                    number=1,          
                    savePath=None, 
                                  
              ):                  
    assert savePath and SourceGraph , "map error"
                                  
    Stations_length = len(Stations) - 1
    inputNodefeature = []  # --> Dijksta matrix  
    inputEdgeindex = []           
    inputEdgeweight = []       
    inputCoordinate = []   
    y_CCO = []                    
    y_CE = []                     
    opt = []                      
                                  
    Debug_logger = []             
    Debug_logger_path = savePath

    start = time.time()
    
    for i in tqdm(range(dataSize)):
        try : 
            problem_instance = Sampler(Stations , sampleSize)
            
            node_feature , edge_index , edge_weight , subGraph, reindex,node_coor = GraphFeature(problem_instance,SourceGraph=SourceGraph)
            
            y_ce , optCost = concorde_Solver(node_feature)
            # 12-04 find a buuger that sometime (3%) the slover cannot find solution , when use the multi-proces
            if optCost >1000 : continue  
            
            COO_edge_labels = COO_transform(y_ce,subGraph,reindex , edgeIndex=edge_index)
            

            inputNodefeature.append(node_feature)
            inputEdgeindex.append(edge_index) 
            inputEdgeweight.append(edge_weight)
            inputCoordinate.append(node_coor)
            y_CCO.append(COO_edge_labels)
            y_CE.append(y_ce) 
            opt.append(optCost)
     
        
        except  Exception as e  :
            print(e) 
            debug_logger(Debug_logger_path+"log.txt" , f"thread {i} raise a error when generate ")
            continue
    # covert to tensor 
    tensor_Node_feature = torch.tensor(np.array(inputNodefeature) , dtype=torch.float)
    tensor_Edge_index = torch.tensor(np.array(inputEdgeindex) ,dtype=torch.long)
    tensor_Edge_weight = torch.tensor(np.array(inputEdgeweight) , dtype=torch.float)
    tensor_Node_coordinate = torch.tensor(np.array(inputCoordinate), dtype= torch.float)
    tensor_y_COO = torch.tensor(np.array(y_CCO), dtype=torch.long)
    tensor_y_CE = torch.tensor(np.array(y_CE) , dtype=torch.long)  
    tensor_opt = torch.tensor(np.array(opt).astype(np.float32),dtype=torch.float32)
    
    del inputEdgeindex,inputEdgeweight,inputNodefeature , inputCoordinate ,y_CE , opt 
    
    if save: 
        if os.path.isdir(savePath) : pass 
        else : os.mkdir(savePath) 
        
        savePath =  savePath + str(number) 

        print(savePath , '---------------------------------')
        try: 
            os.mkdir(savePath) 
        except: 
            debug_logger(Debug_logger_path+"log.txt" , f"thread {i} raise a error when SAVE ")
            raise BaseException("This directory is exist !!! ERROR")

        print(f"save path : {savePath}")
        torch.save(tensor_Node_feature,  savePath+"/node_feature.pt")
        torch.save(tensor_Edge_index,    savePath+"/edge_index.pt")
        torch.save(tensor_Edge_weight,   savePath+"/edge_weight.pt"  ) 
        torch.save(tensor_Node_coordinate , savePath + "/node_coordinate.pt") 
        torch.save(tensor_y_COO,         savePath+"/labels_COO.pt")
        torch.save(tensor_y_CE,          savePath+"/labels_CE.pt")
        torch.save(tensor_opt,           savePath+"/opt.pt")
    
    print(f"The process {number} is done  {time.time() - start }!")
    return 
        
# in every process /home/python_code/GNN/Dataset/ date + number / node_feature...
def Assembly(store_path,*target): 
    print("start assemble the dataset")
    
    """
    2022-11-16  use the os.listdir to grab all directory in the path  
    tmp_dirs = [store_path+str(i) for i in range(num_workers)]
    
    #check those folder is exist 
    tmp_dirs = list(filter(lambda path:os.path.isdir(path) , tmp_dirs) )
    """
    print(store_path)
    tmp_dirs= list(filter( lambda x : os.path.isdir(store_path+x) , list(os.listdir(store_path))) )
    print(tmp_dirs)
    tmp_dirs = [store_path+i for i in tmp_dirs[:]]
    print(tmp_dirs)
    for t in target: 

        t+= ".pt"
        tensorData = list()
        for Dir in tmp_dirs : 
            try: 
                tensorData.append(torch.load(Dir+"/"+t))
            except: print("Dir ",Dir)

     
        file = torch.concat(tuple(tensorData),dim=0)
        torch.save(file , store_path+t)
        print(f"concat the {t} {file.shape} has done ")

    
    #[shutil.rmtree(dirs) for dirs in tmp_dirs ]  



# use only for test 
if __name__ == "__main__": 
    
    # Path = "/home/croso1024/python_code/Algorithms/Benchmarker"
    # import sys 
    # if not Path in sys.path : sys.path.append(Path)
    # from Benchmark_ import Benchmarker 
    
    # Benchmarker.setting("./DatasetGenerate/trainMap.json")
    # Benchmarker.Source_graphLoading() 
    # SourceGraph = Benchmarker.SourceGraph
    # Stations = Benchmarker.station_list  
    # All_pair_cost = Benchmarker.All_pair_cost 
    SourceGraph ,Stations , All_pair_cost , ret = GraphLoading("./DatasetGenerate/trainMap_square_GCN.json")
    
    Generator(
                    SourceGraph=SourceGraph,
                    Stations=Stations , 
                    All_pair_cost=All_pair_cost ,
                    sampleSize = 20 ,
                    dataSize=10 ,
                    save=False , 
                    number=1, 
                    savePath="./",
                    
              )