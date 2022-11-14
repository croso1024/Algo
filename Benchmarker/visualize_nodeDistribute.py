from squareNodeMap import node , node_coordinateFunc ,distance
import matplotlib.pyplot as plt 
import networkx as nx 

mode = "unit"
nodes_set = [node_coordinateFunc(mode) for i in range(20)] 

nodex = [n.x for n in nodes_set]
nodey = [n.y for n in nodes_set]
distance_set = []
plt.scatter(nodex,nodey , color="red")
plt.grid()
plt.show()

G = nx.Graph() 
pos_dict = {}
for i,n in enumerate(nodes_set): 
    G.add_node(str(i) , x=n.x , y=n.y)
    pos_dict[str(i)] = (n.x,n.y)
    
for i in range(20): 
    for j in range(i,20): 
        dis = distance(nodes_set[i],nodes_set[j])
        distance_set.append(dis)
        G.add_edge(str(i),str(j),weight=dis )
        
nx.draw_networkx(G , pos=pos_dict,node_size=25,node_color="red",width=0.5 , with_labels=False)
plt.ylabel("Y") , plt.xlabel("X") 
#plt.ylim(0,1),plt.xlim(0,1)
plt.grid()
plt.show()


plt.hist(distance_set,bins=50) 
plt.grid()
plt.ylabel("Number of edges"),plt.xlabel("edge weight")
plt.show()