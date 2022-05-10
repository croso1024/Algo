# New route optimization sys  
# launch at 2022/03/24 



import matplotlib.pyplot as plt 
import networkx as nx
from networkx.algorithms import approximation as algo
import json 

"""
2022/03/24:
分成 base graph, 以及request graph(fully con)
"""
"""
2022/03/13 要把送達目標點這件事情的cost也考慮進去
而不是傳統意義上的通過就好 
"""
class NetGraph(nx.Graph):

#graph_name= "HB"
#node_doc = "expo_park.json"
    def __init__(self,name):
        super().__init__(self)
        self.path = name
        self.filed = name[:-5]
        self.graphLoading()
        

    def graphLoading(self):     
        # Setting up the node name&position , including the path and weight
        # added to the graph instance 
        with open(self.path,"r") as element:
            rawData = json.load(element)
            print("Raw data loading complete")
        destination_list = list(rawData["goals"].keys())
        for goal in destination_list:
            position =(rawData["goals"][goal]["pos"]["x"],rawData["goals"][goal]["pos"]["y"])
            self.add_node(goal,pos=position)
        #-------------------for gurobi version----------------------s
        self.GurobiEdge = rawData["edges"]  
        self.GurobiWeight = rawData["weights"]
        #-----------------------------------------------------------
        edge_list = rawData["edges"]    
        weight_list = rawData["weights"]
        for i in range(len(edge_list)):
            edge_start = eval(edge_list[i])[0]
            edge_end = eval(edge_list[i])[1]
            self.add_edge(destination_list[edge_start],destination_list[edge_end],weight=weight_list[i])
        self.pos = nx.get_node_attributes(self,"pos")
        self.weight = nx.get_edge_attributes(self,"weight")
        print("graph generation complete")
    
    # draw the figure ,work either non-fully connective or fully connective
    @staticmethod
    def drawing(graph,Pos_mode=None,Weight_mode=None):   #--> draw the figure
        if Pos_mode==None:
            #Pos_mode = nx.get_node_attributes(self,"pos")
            Pos_mode = nx.kamada_kawai_layout(graph)
        if Weight_mode ==None:
            Weight_mode =nx.get_edge_attributes(graph,"weight")
        #print(type(weight_info))
        
        nx.draw_networkx(graph,pos=Pos_mode,node_size=100,with_labels=True,font_size=5)
        nx.draw_networkx_edge_labels(graph,pos=Pos_mode,edge_labels=Weight_mode,font_color="red",font_size=10)
        #plt.show()

    @staticmethod # --> TSP transformer 
    def comGraph_Transform(graph,source,targetList,weight="weight") -> nx.Graph():
        if type(targetList) != type([]): 
            targetList = list(targetList)

        comGraph = nx.Graph()
        targetList.insert(0,source)
        assert targetList != None , "targetList is None" 
        Path_dict = dict(nx.all_pairs_bellman_ford_path_length(graph,weight))

        print("Node will build the comGraph: {}".format(targetList))
        comGraph.add_nodes_from(targetList,Source=False) 
        comGraph._node[source]["Source"]=True
        
        temp = targetList.copy()
        for start in targetList:
            temp.remove(start)
            for end in temp:
                print("add edge from {} to {}, weight = {}".format(start,end,Path_dict[start][end]))
                comGraph.add_edge(start,end,weight=Path_dict[start][end])
        comGraph.weight = nx.get_edge_attributes(comGraph,"weight")      
        return comGraph
    @staticmethod
    def TSP_solve(graph,source=None,targetList=None):
        print("Visit node: {}".format(targetList))
        
        path = algo.traveling_salesman_problem(graph,cycle=False)
        #path2 = algo.greedy_tsp(graph,weight="weight")
        print(f"the path be planning : {path}")
        #print(type(path))
        
        return path
    # --> targetlist  讀取quene class 
    # def TSP_solve(self,source=None,targetList=None):
    #     print("Visit node: {}".format(targetList))
        
    #     print(dict(nx.all_pairs_dijkstra(self,weight="weight")))
    #     print("ending")
    #     print(dict(nx.all_pairs_dijkstra_path_length(self,weight="weight")))
    #     #return path

if __name__ =="__main__":

    graph = NetGraph("/home/croso1024/python_code/Networkx_/expo_park.json")

    source = "1F_start"
    #TargetList =["1F_gate_1","1F_HenGi","1F_willy_destroy"]
    TargetList = ["1F_start","1F_HenGi","1F_forest","1F_stage","1F_gate_1","1F_willy_destroy"]
    comG = NetGraph.comGraph_Transform(graph,source="1F_forest",targetList=TargetList)
    NetGraph.TSP_solve(comG)
    plt.figure()
    plt.subplot(1,2,1)
    NetGraph.drawing(graph) 
    plt.subplot(1,2,2)
    NetGraph.drawing(comG)  
    plt.show()
    #print(nx.get_edge_attributes(graph,"weight"))
   



