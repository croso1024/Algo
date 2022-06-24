#　benchmark platform for MVRP-PD 
# Multi Vehicle Route Problem - Pick & Delivery   

# initial condition : available robot / source graph  / edge cost / request 
# 平台本身hold著一個source graph的資料,只有點名稱以及點與點的連接關係和cost
# instance則是不同情況下的 sub-graph, 支援add / delete 功能
from matplotlib import animation
import matplotlib.pyplot as plt 

import networkx as nx 
from networkx.algorithms import approximation as algo
import json 


class Benchmarker(nx.Graph): 
    
    vehicle_set = ["ANEV01","ANEV02","ANEV03","ANEV04"]
    vehicle_pos = {"ANEV01":"A","ANEV02":"A","ANEV03":"A","ANEV04":"A"}
    
    def __init__(self): 
        super().__init__(self) 
    @classmethod 
    def setting(cls,setting_file_path=None): 
        #cls.source_path = "map/Adjency.json"
        cls.source_path = "map/longStation2.json"
    @classmethod  
    def Source_graphLoading(cls): 
        #sourceGraph = Benchmarker() 
        sourceGraph = cls() 
        with open(cls.source_path,"r") as file:
            graph = json.load(file)
            cls.station_list = graph["station"]
            cls.dimention = len(cls.station_list)
            cls.adjencyMatrix = graph["adjencyMatrix"]
            assert cls.dimention == len(cls.adjencyMatrix[0]) , "Adjency matrix error"
        # loading nodes from sourcefile  
        for node in cls.station_list: 
            sourceGraph.add_node(node) 
        # loading edges for every
        for i, node in enumerate(cls.station_list): 
            for j in range(i+1,cls.dimention): 
                cost = cls.adjencyMatrix[i][j]
                if cost: 
                    sourceGraph.add_edge(node,cls.station_list[j],weight=cost)
        cls.SourceGraph = sourceGraph 
        cls.All_pair_cost = dict(nx.all_pairs_dijkstra_path_length(cls.SourceGraph))
        print("Source graph Loading complete")
        #print(cls.All_pair_cost)
    
    #excepted request is list including dispatch msg {"account":,location.. ,"uuid"}
    #nodes --> pure "location" , anything attribute likes uuid will be append on request 
    @classmethod 
    def _routeCost(cls,nodes: list,vehicle_num=1): 
        total_cost = 0  
        for step in range( len(nodes)-1 ): 
            curNode = nodes[step]
            nextNode = nodes[step+1]
            total_cost += cls.All_pair_cost[curNode][nextNode]  
        #print("The solution total cost is {}".format(total_cost))
        #print("Solution:{}".format(nodes))
        return total_cost,nodes


                
    @classmethod
    def Solution_parser(cls,vehicle_num,nodes) : 
        sub_set = [list() for i in range(vehicle_num)]
        # for first vehicle 
        n_path = 0 
        sub_set[n_path].insert(0,cls.vehicle_pos[cls.vehicle_set[n_path]])  
        
        for station in nodes: 

            if not station == "|":  #沒有遇到symbol的時候就單純加入list
                sub_set[n_path].append(station) 
    
            else : 
                # 遇到symbol, 將下一台車的位置加入,開始整理下一台車負責的解集合
                n_path +=1 
        
                sub_set[n_path].insert(0,cls.vehicle_pos[cls.vehicle_set[n_path]])   
                
        for n, nth_sub_set in enumerate(sub_set) : 
            if len(nth_sub_set) == 1:  # mean in this solution the n-th vehicle dosen't have any mission
                sub_set[n] = []
            
        return sub_set 

    @classmethod 
    def MultiVehicle_Cost(cls,nodes:list,vehicle_num): 
        solution_set  = cls.Solution_parser(vehicle_num , nodes)
        cost_set = [0 for i in range(vehicle_num)]
    
        for n, nth_solution in enumerate(solution_set) : 
            if nth_solution : # this solution have waypoint ( len(solution) > 0 )
                cost_set[n], ret  = cls._routeCost(nth_solution)
            else : 
                cost_set[n] = 0  
        
        #criterion 1 . min Sum , minimize the total cost for every vehicle  
        Cost = sum(cost_set) 
        #criterion 2 , min Max , minimize the most cost vehicle in set     
        #Cost = max(cost_set)
        return Cost , nodes
        
        
    @staticmethod
    def plotting(graph):
        pos_mode = nx.kamada_kawai_layout(graph)
        cost_label = nx.get_edge_attributes(graph,"weight")
        nx.draw_networkx(graph,pos =pos_mode ,node_size=50,with_labels=True,font_size=5)
        nx.draw_networkx_edge_labels(graph,pos=pos_mode,edge_labels=cost_label,font_color="red",font_size=3)


    @classmethod 
    def inference(cls,map_set,vehicle_set,Algorithm_set): 
        pass

if __name__ == "__main__": 
    Benchmarker.setting()
    Benchmarker.Source_graphLoading()
    Benchmarker.plotting(Benchmarker.SourceGraph)
