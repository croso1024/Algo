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
    
    def __init__(self): 
        super().__init__(self) 
    @classmethod 
    def setting(cls,setting_file_path=None): 
        #cls.source_path = "Adjency.json"
        cls.source_path = "map/longStation.json"
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
        print(cls.All_pair_cost)
    
    #excepted request is list including dispatch msg {"account":,location.. ,"uuid"}
    #nodes --> pure "location" , anything attribute likes uuid will be append on request 
    @classmethod 
    def _routeCost(cls,nodes: list): 
        total_cost = 0  
        for step in range( len(nodes)-1 ): 
            curNode = nodes[step]
            nextNode = nodes[step+1]
            total_cost += cls.All_pair_cost[curNode][nextNode]  
        #print("The solution total cost is {}".format(total_cost))
        #print("Solution:{}".format(nodes))
        return total_cost,nodes

    @staticmethod
    def plotting(graph):
        pos_mode = nx.kamada_kawai_layout(graph)
        cost_label = nx.get_edge_attributes(graph,"weight")
        nx.draw_networkx(graph,pos =pos_mode ,node_size=50,with_labels=True,font_size=5)
        nx.draw_networkx_edge_labels(graph,pos=pos_mode,edge_labels=cost_label,font_color="red",font_size=3)

        

if __name__ == "__main__": 
    Benchmarker.setting()
    Benchmarker.Source_graphLoading()
    Benchmarker.plotting(Benchmarker.SourceGraph)
