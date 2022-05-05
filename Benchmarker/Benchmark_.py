#　benchmark platform for MVRP-PD 
# Multi Vehicle Route Problem - Pick & Delivery   

# initial condition : available robot / source graph  / edge cost / request 
# 平台本身hold著一個source graph的資料,只有點名稱以及點與點的連接關係和cost
# instance則是不同情況下的 sub-graph, 支援add / delete 功能
import matplotlib.pyplot as plt 
import networkx as nx 
from networkx.algorithms import approximation as algo
import json 
from exhaustive_slover import SolutionPool
class Benchmarker(nx.Graph): 
    
    def __init__(self): 
        super().__init__(self) 
    @classmethod 
    def setting(cls,setting_file_path=None): 
        cls.source_path = "Adjency.json"
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
    
    #excepted request is list including dispatch msg {"account":,location.. ,"uuid"}
    #nodes --> pure "location" , anything attribute likes uuid will be append on request 
    @classmethod
    def _subGraph(cls,nodes):  #--> 暫時棄用, 直接採用All pair dijkstra一同保存在class中 ,更有彈性去應對動態節點變化
        subGraph = cls()
        All_pair_distance = dict(nx.all_pairs_dijkstra_path_length(cls.SourceGraph))
        for node in nodes: 
            subGraph.add_node(node)
        for i,node in enumerate(nodes): 
            for j in range(i+1,len(nodes)) : 
            #index = cls.station_list.index(node) 
                print(j)
                cost  = All_pair_distance[node][nodes[j]]  
                subGraph.add_edge(node,nodes[j],weight=cost)  
        return subGraph 
    
    @classmethod 
    def _routeCost(cls,nodes: list): 
        total_cost = 0  
        for step in range( len(nodes)-1 ): 
            curNode = nodes[step]
            nextNode = nodes[step+1]
            total_cost += cls.All_pair_cost[curNode][nextNode]  
        print("The solution total cost is {}".format(total_cost))
        print("Solution:{}".format(nodes))
        return total_cost
    # @classmethod
    # def _Dispatcher(cls,request): 
    #     solution_list = SolutionPool(request) 
    #     optimal_cost = float("inf")
    #     for route in solution_list: 
    #         cost = cls._routeCost(route) 
    #         if cost < optimal_cost: 
    #             optimal_cost = cost 
    #         else: 
    #             pass 
    #         print("current optimal".format(optimal_cost))
    #     print("optimal cost : {}".format(optimal_cost))
    @classmethod 
    def exhaustive(cls,nodelist,sol=""): 
        if len(nodelist) == 0: 
            cost = cls._routeCost(sol)
            if cost < optimal_cost: 
                optimal_cost = cost 
            else: 
                pass 
        else: 
            for i in range(len(nodelist)): 
                cls.exhaustive(nodelist[:i]+nodelist[i+1:],sol+nodelist[i])
   

    

    @staticmethod
    def plotting(graph):
        pos_mode = nx.kamada_kawai_layout(graph)
        cost_label = nx.get_edge_attributes(graph,"weight")
        nx.draw_networkx(graph,pos =pos_mode ,node_size=100,with_labels=True,font_size=15)
        nx.draw_networkx_edge_labels(graph,pos=pos_mode,edge_labels=cost_label,font_color="red",font_size=15)

Benchmarker.setting()
Benchmarker.Source_graphLoading()
Benchmarker.plotting(Benchmarker.SourceGraph)
#g = Benchmarker._subGraph(["A","B","C"])
Benchmarker._Dispatcher(["A","B","C","D","E"])
#Benchmarker.plotting(g)
plt.show()
