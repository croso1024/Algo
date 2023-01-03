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
    
    #vehicle_set = ["ANEV01","ANEV02","ANEV03","ANEV04"]
    #vehicle_pos = {"ANEV01":"1F_start","ANEV02":"1F_start","ANEV03":"1F_start","ANEV04":"B"}
    #vehicle_pos = {"ANEV01":"A","ANEV02":"A","ANEV03":"A","ANEV04":"A"}
    vehicle_set = []
    vehicle_pos = {}
    def __init__(self): 
        super().__init__(self) 
    @classmethod 
    def setting(cls,setting_file_path=None): 
        cls.source_path =setting_file_path
        cls.Total_vehicleNum =1
      
        #cls.source_path = setting_file_path

    @classmethod  
    def Source_graphLoading(cls): 
        #sourceGraph = Benchmarker() 
        sourceGraph = cls() 
        print(cls.source_path)
        with open(cls.source_path,"r") as file:
            graph = json.load(file)
            cls.Depot = graph["Depot"]
            cls.station_list = graph["station"]
            cls.dimention = len(cls.station_list)
            cls.adjencyMatrix = graph["adjencyMatrix"]
            assert cls.dimention == len(cls.adjencyMatrix[0]) , "Adjency matrix error"
            for i in range(cls.Total_vehicleNum): 
                car = "AMR0"+str(i+1) 
                cls.vehicle_set.append(car)
                cls.vehicle_pos.update({car:cls.Depot})
            # 0904 set for GA
            cls.encodeTalbe = {i:node for i,node in enumerate(cls.station_list)}    
                
            
        # loading nodes from sourcefile  
        for node in cls.station_list: 
            sourceGraph.add_node(node) 
        # loading self-loop edge , weight = 0 
        # for node in cls.station_list: 
        #     sourceGraph.add_edge(node,node,weight=0)
        
        # loading edges for every
        for i, node in enumerate(cls.station_list): 
            for j in range(i+1,cls.dimention): 
                cost = cls.adjencyMatrix[i][j]
                if cost: 
                    sourceGraph.add_edge(node,cls.station_list[j],weight=cost)
        
        
        
        cls.SourceGraph = sourceGraph 
        cls.All_pair_cost = dict(nx.all_pairs_dijkstra_path_length(cls.SourceGraph))
        cls.All_pair_path = dict(nx.all_pairs_dijkstra_path(cls.SourceGraph))
        #print("Source graph Loading complete")
        #print(cls.All_pair_cost)
        #print("all pair path ")
        #print(cls.All_pair_path)
    #excepted request is list including dispatch msg {"account":,location.. ,"uuid"}
    #nodes --> pure "location" , anything attribute likes uuid will be append on request 
    @classmethod 
    def _routeCost(cls,nodes: list,vehicle_num=1): 
       
        total_cost = 0  
        #nodes = cls.Solution_parser(vehicle_num=1,nodes=nodes)[0]
        # 如果vehicle_num >1 在parser時就insert過了
        if vehicle_num ==1:
            nodes.insert(0,cls.vehicle_pos[cls.vehicle_set[0]])
        
        for step in range( len(nodes)-1 ): 
            curNode = nodes[step]
            nextNode = nodes[step+1]
     
            #print(cls.All_pair_cost[curNode][nextNode])
            total_cost += cls.All_pair_cost[curNode][nextNode]  
        
        
        #print("The solution total cost is {}".format(total_cost))
        #print("Solution:{}".format(nodes))
        return total_cost,nodes


    ######################################
    # 0917 , simplify datagenerate , cost compute by origin graph !!! 
    @classmethod
    def _routeCost_DataGen(cls,nodes:list , vehicle_num=1,depot_start=False , cycle=True) : 
        
        
        total_cost = 0 
        if vehicle_num ==1 and depot_start:
            nodes.insert(0,cls.vehicle_pos[cls.vehicle_set[0]])
        for step in range( len(nodes) - 1): 
            curNode = str(nodes[step])
            nextNode = str(nodes[step+1])
            
            #for non Encode map 
            total_cost += cls.All_pair_cost[curNode][nextNode]
            
            # for Encode map 
            #total_cost += cls.SourceGraph[curNode][nextNode]["weight"]
       
        if cycle : 
            total_cost += cls.All_pair_cost[nodes[-1]][nodes[0]]
        
        # print(total_cost,nodes)
        
        return total_cost,nodes
    
    ####################################
    @classmethod
    def Solution_parser(cls,vehicle_num,nodes,backToHome=False) : 
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
                cost_set[n], ret  = cls._routeCost(nth_solution,vehicle_num)
            else : 
                cost_set[n] = 0  
        #print(cost_set)
        #criterion 1 . min Sum , minimize the total cost for every vehicle  
        Cost = sum(cost_set) 
        #criterion 2 , min Max , minimize the most cost vehicle in set     
        #Cost = max(cost_set)
        return Cost , solution_set#nodes
        
        
    
    
    
    @staticmethod
    def plotting(graph,solution_path =None,optimizer:str=None, title:str=None,Cost_log=None,testing_set=None,vehicle_num=1,map_name=None):
        pos_mode = nx.kamada_kawai_layout(graph)
        cost_label = nx.get_edge_attributes(graph,"weight")
        
        if optimizer and solution_path and Cost_log :  
            fig = plt.figure(figsize = (14,4), dpi = 100 )
            # ---------------origin graph
            
            plt.subplot(1,4,1),plt.title("Map")
            nx.draw_networkx(graph,pos =pos_mode ,node_size=50,with_labels=True,font_size=5)
            nx.draw_networkx_edge_labels(graph,pos=pos_mode,edge_labels=cost_label,font_color="red",font_size=6)
            plt.subplot(1,4,2),plt.title("solution path")
            # --------------- copy a graph to plot solution
            solution_graph = graph.copy()
            nx.draw_networkx(solution_graph,pos =pos_mode ,node_size=50,with_labels=True,font_size=5)
            nx.draw_networkx_edge_labels(solution_graph,pos=pos_mode,edge_labels=cost_label,font_color="red",font_size=6)
            color_plate = ["red","green","yellow","purple","lime","pink","gold","darkorange","violet"]
       
            node_list_by_vehicle = [list() for i in range(vehicle_num)]
            
            vehicle = 0  
            for i, node in enumerate(solution_path): 
                if not node == "|": 
                    node_list_by_vehicle[vehicle].append(node) 
                else : 
                    vehicle += 1             
                    
            for i,node_list in enumerate(node_list_by_vehicle):  # -- > expected completely parser ["a","b","c"]
                if not node_list:
                    continue
                
                # 0920 : comment this line for dataGenerate , plot tour without start point (depot)
                #node_list.insert(0,Benchmarker.vehicle_pos[Benchmarker.vehicle_set[i]])
                
                edge_list = [] 
                for j in range(len(node_list)-1):
                    edge_list.append(tuple( [node_list[j],node_list[j+1]]) )
                nx.draw_networkx_nodes(solution_graph, pos= pos_mode , nodelist=node_list,node_size=70,node_color=color_plate[i])
                nx.draw_networkx_edges(solution_graph,pos = pos_mode,width=2,edge_color=color_plate[i] , 
                                    edgelist=edge_list)
                
                
            
            
            plt.subplot(1,4,4) , plt.title(f"optimization by {optimizer}")
            plt.plot(range(len(Cost_log)),Cost_log) , plt.ylabel("Cost")  , plt.xlabel("iteration Num")
            text_ax = plt.subplot(1,4,3) 
            plt.text(0,0.2,testing_set,transform=text_ax.transAxes)
            plt.axis("off")
            fig.tight_layout()
        
        else: 
           
            plt.title("Loading map")
            nx.draw_networkx(graph,pos =pos_mode ,node_size=50,with_labels=True,font_size=15)
            nx.draw_networkx_edge_labels(graph,pos=pos_mode,edge_labels=cost_label,font_color="red",font_size=16)
           
        plt.show()

    @classmethod 
    def inference(cls,map_set,vehicle_set,Algorithm_set): 
        pass

if __name__ == "__main__":
    print("dodo")
    Benchmarker.setting("map/YaTai3_adjency.json")
    Benchmarker.Source_graphLoading()
    Benchmarker.plotting(Benchmarker.SourceGraph)
