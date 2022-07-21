from Benchmark_ import Benchmarker 
import numpy as np 
import time ,json 
import heapq as heap


class Node: 
    # location of root is the current location of vehicle 
    def __init__(self,parent=None,search_set=None,location=None): 
        self.nodebound = np.inf 
        self.parent = parent
        self.search_set = search_set
        self.location = location
        
    def bulid_solution(self): 
        solution = [self.location] 
        #cost = self.parent.nodebound 
        cost = self.nodebound
        probe = self.parent
        
        while probe :  
            solution.append(probe.location)
            probe = probe.parent 
        solution.reverse() 
        return solution ,cost 
    
    def evaluate(self): 
        self.nodebound = self.parent.nodebound + Benchmarker.All_pair_cost[self.parent.location][self.location]
    def __eq__(self,other):
        return (self.nodebound == other.nodebound) 
    def __gt__(self,other): 
        return (self.nodebound > other.nodebound) 
    def __lt__(self,other):
        return (self.nodebound < other.nodebound) 
    

    
class BranchBound: 
    
    def __init__(self,initial_solution,vehicle_location): 
        print(initial_solution)
        self.search_set = []  # --> use as minheap for node bound
        
        self.optimal_solution = initial_solution # use initial or None as optimal for start

        #self.optimal_solution_cost = 90

        ##### follow 2 line must enable simutanious , _routeCost may modify the initial solution
        self.optimal_solution_cost = Benchmarker._routeCost(initial_solution,vehicle_num=1)[0]
        initial_solution.pop(0)# fix the effect of call _routeCost ( add a station of vehicle pos )
        
        self.current_node = Node(search_set=initial_solution,location=vehicle_location)
        #print("--------",self.current_node.search_set)
        self.current_node.nodebound = 0 # root cost(bound) = 0  

        self.find_solution_num = 0
        
        self.solution_log = []
    def search_set_NotEmpty(self): 
        return  bool(self.search_set)
    
    def search(self) : 
        # findout all branch that node can search , and evaluate them , 
        #print(f"current node search_set = {self.current_node.search_set}")
        for i,location in enumerate(self.current_node.search_set)  :
            #print(f"current node search_set = {self.current_node.search_set},location:{location}")
            sub_solution =  self.current_node.search_set.copy()
            sub_solution.pop(i)
            node = Node(parent=self.current_node,search_set=sub_solution,location=location) # pass the residue subprobelm_set to next level node 

            
            # 如果search space還有東西, 則代表此節點還可以繼續擴展而還沒有辦法形成解, 計算此節點的界,若大於目前的下界,就不加入接下來的搜索heap
            if sub_solution : # if still have something wait to be search 
                
                node.evaluate()  #--> calculate this node lowwer bound 
                #node.nodebound = node.parent.nodebound +  Benchmarker.All_pair_cost[node.parent.location][node.location]
                if node.nodebound < self.optimal_solution_cost: 
                    #print(f"add new node:{node.search_set},node_bound:{node.nodebound} ") 
                    
                    heap.heappush(self.search_set,(node.nodebound,node)) 
                else :
                    #print("----cut------")
                    pass
            # 當搜索空間被清空,代表這個節點已經可以形成解了, 用回溯parent的地點的方式形成解
            else : # we can figure out a solution 
                node.evaluate()
                solution,cost = node.bulid_solution()
                # update bound , solution 
                #print(f"get a solution:{solution}")

                #0715 , if use in realAMR , we dont't need the current position add into task
                solution.pop(0) 
                
                if cost < self.optimal_solution_cost : 
                    self.optimal_solution_cost  = cost 
                    self.optimal_solution = solution 
                else : 
                    pass 
                self.find_solution_num += 1
                self.solution_log.append(self.optimal_solution_cost)
            
    def move(self): 
        next_node = heap.heappop(self.search_set)[1]
        #print(f"get next node {next_node}")
        self.current_node = next_node 
        self.search()
        
    def main(self,plotting=False): 
        heap.heappush(self.search_set,(self.current_node.nodebound,self.current_node))
        root = heap.heappop(self.search_set)[1]
        self.current_node = root 

        t_start = time.time()
        self.search()
        while self.search_set_NotEmpty() : 
            #print(self.search_set)
            self.move()
        CostTime = time.time()-t_start
        print(f"Total find solution : {self.find_solution_num}")
        print(f"Optimal solution: {self.optimal_solution}")
        print(f"Optimal solution cost:{self.optimal_solution_cost}")
        if plotting: 
            test_setting = f"optimizer: Branch&Bound\n\nCost:{self.optimal_solution_cost}\n\nget solution num:{self.find_solution_num}\n\nCost time: {CostTime}\n\nCriterion:MinSum" 
            Benchmarker.plotting(Benchmarker.SourceGraph,self.optimal_solution,"Branch&Bound",Cost_log=self.solution_log,testing_set=test_setting)
        
if __name__ == "__main__": 
    Benchmarker.setting(setting_file_path="map/building_small.json")
    Benchmarker.Source_graphLoading() 
    bb = BranchBound(initial_solution=["B","J","E","H","P","M","G","O","C"],vehicle_location="A") 
    #bb = BranchBound(initial_solution=["A","1","c","b","e","2","E","C","d","4","G"],vehicle_location="A") 
    #bb = BranchBound(initial_solution=["1F_stage","1F_gate_2","1F_HenGi","1F_table","1F_forest","1F_willy_destroy"],vehicle_location="1F_start")
    bb.main(plotting=True)