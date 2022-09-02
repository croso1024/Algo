import pygad  , json 
from Benchmark_ import Benchmarker
import networkx as nx 
import numpy as np


# def fitness_function(solution,solution_index): 
#     global encodeTable , CostMap   
#     #print(f"solution before parse {solution}")
#     solution = [encodeTable[i] for i in solution]
#     #print(f"solution after parse {solution}")
#     total_cost = 0
#     for step in range(len(solution)  -1 ): 
#         curNode = solution[step]
#         nextNode = solution[step+1]
#         total_cost += CostMap[curNode][nextNode]

#     return -1*total_cost 



class Genetic_algorithms : 
    
    def __init__(self,setting_file_path=None) : 
        self.SourceGraph = nx.Graph() 
        self.map_file = setting_file_path 
        self.graphLoading()
        
    def graphLoading(self):  
        
        with open(self.map_file , "r") as file : 
            graph = json.load(file) 
            self.station_list = graph["station"] 
            self.dimention = len(self.station_list)
            self.adjencyMatrix  = graph["adjencyMatrix"] 
            self.encodeTable = {i+1:node for i,node in  enumerate(self.station_list)}
            
            
            for node in self.station_list: 
                self.SourceGraph.add_node(node) 
            for i , node in enumerate(self.station_list): 
                for j in range(i+1 , self.dimention) : 
                    cost = self.adjencyMatrix[i][j] 
                    if cost :  self.SourceGraph.add_edge(node,self.station_list[j],weight=cost) 
        self.All_pair_cost = dict(nx.all_pairs_dijkstra_path_length(self.SourceGraph)) 
        self.All_pair_path = dict(nx.all_pairs_dijkstra_path(self.SourceGraph)) 
        print(self.SourceGraph.nodes())
        print(self.SourceGraph.edges())
    

        
    @staticmethod
    def fitness_function(solution,solution_index): 
        global encodeTable , CostMap   
        #print(f"solution before parse {solution}")
        solution = [encodeTable[i] for i in solution]
        #print(f"solution after parse {solution}")
        total_cost = 0
        for step in range(len(solution)  -1 ): 
            curNode = solution[step]
            nextNode = solution[step+1]
            total_cost += CostMap[curNode][nextNode]

        return -1*total_cost 

    
    def Parameter(self): 
        
        num_generation = 250 
        num_parents_mating = 8
        solution_per_population = 16
        num_genes = self.dimention
        
        parent_selection_type = "sss"  
        init_low , init_high = 1, self.dimention
        crossover_type = "two_points" 
        mutation_type ="adaptive"
        mutation_percent = [10,20] 
        keep_parents = 8
        
        gene_space = [i for i in range(1,self.dimention+1)]
        
        population_list = [] 
        
        for i in range(solution_per_population):
            randomPermu = list(np.random.permutation(gene_space))
            population_list.append(randomPermu)
        
        self.GA_instance = pygad.GA(
            num_generations=num_generation,
            num_parents_mating=num_parents_mating, 
            fitness_func=Genetic_algorithms.fitness_function,
            sol_per_pop=solution_per_population, 
            initial_population=population_list,
            num_genes=num_genes,
            gene_space = gene_space,
            parent_selection_type=parent_selection_type,
            keep_parents=keep_parents,
            crossover_type=crossover_type,
            mutation_type=mutation_type,
            mutation_percent_genes=mutation_percent,
            allow_duplicate_genes=False,
        ) 
        print("done")
    def Optimization(self) : 
        self.Parameter()   
        self.GA_instance.run() 
        solution, solution_fitness, solution_idx = self.GA_instance.best_solution()
        print("best_solution: {solution}".format(solution =[encodeTable[i] for i in solution]))
        print("best_solution fitness: {solution_fit}".format(solution_fit =-1*solution_fitness))
        
        
GA =  Genetic_algorithms(setting_file_path="map/Relax_small.json")
encodeTable = GA.encodeTable
CostMap = GA.All_pair_cost
GA.Optimization()