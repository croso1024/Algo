
import pygad  , json 
from Benchmark_ import Benchmarker
import networkx as nx 
import numpy as np
import time 

"""
develop log:目前在考慮要如何插入｜　可能要在每次送fitness的時候都跑一次mutil_vehicle_adjust但耗時 
另外multi_vehicle_adjust需要vehicle_num , 需要想一下在不傳入self的情況下如何使用  
或是想辦法使fitness fun可以用self
"""

class Genetic_algorithms : 
  
    def __init__(self,initial_solution,vehicle_num=1) : 
    
        self.initial_solution = initial_solution 
        if vehicle_num >1 :
            self.MultiVehicle_adjust()
            
        self.dimention = len(initial_solution) 
        self.gene_space = [i for i in range(self.dimention)]
        
        self.population_list = [] 
        self.solution_per_population = 16
        for i in range(self.solution_per_population):
            randomPermu = list(np.random.permutation(self.gene_space))
            self.population_list.append(randomPermu)
        
        
        
        
        self.num_generation = 250 
        self.num_parents_mating = 8
        
        self.num_genes = self.dimention
        self.parent_selection_type = "sss"  
        self.init_low , init_high = 1, self.dimention
        self.crossover_type = "two_points" 
        self.mutation_type ="adaptive"
        self.mutation_percent = [25,4] 
        self.keep_parents = 4
        

        
        if vehicle_num ==1:  
            self.fitness_Func = Genetic_algorithms.fitness_function
        else: 
            print("########## USE multi vehicle ###############")
            self.fitness_Func = Genetic_algorithms.fitness_function_Multi
        
        
    def createGA_instnace(self): 
        self.GA = pygad.GA(
            gene_type=int,
            num_generations=self.num_generation,
            num_parents_mating=self.num_parents_mating, 
            #fitness_func=Genetic_algorithms.fitness_function,
            #fitness_func=self.fitness_Func,
            fitness_func=self.fitness_function2(),
            sol_per_pop=self.solution_per_population, 
            initial_population=self.population_list,
            num_genes=self.num_genes,
            gene_space = self.gene_space,
            parent_selection_type=self.parent_selection_type,
            keep_parents=self.keep_parents,
            crossover_type=self.crossover_type,
            mutation_type=self.mutation_type,
            mutation_percent_genes=self.mutation_percent,
            allow_duplicate_genes=False,

        )
    @staticmethod 
    def encode(solution):   
        return [Benchmarker.encodeTalbe[node] for node in solution]
    
    
    @staticmethod
    def fitness_function(solution,solution_index): 
        
        solution = [Benchmarker.encodeTalbe[node] for node in solution]
    
        return -1 * Benchmarker._routeCost(solution)[0]
    
    def fitness_function2(self) : 
        
        def fitness_fun(solution,solution_index): 
            solution = [Benchmarker.encodeTalbe[node] for node in solution]
    
            return -1 * Benchmarker._routeCost(solution)[0]
        print(self.dimention)
        return fitness_fun
    
    @staticmethod 
    def fitness_function_Multi(solution,solution_inde): 
        solution = [Benchmarker.encodeTalbe[node] for node in solution]
        
        return -1 * Benchmarker.MultiVehicle_Cost(solution,vehicle_num=2)[0]
    
    def MultiVehicle_adjust(self,solution):  
        solution = [Benchmarker.encodeTalbe[node] for node in solution] 
        step = len(solution) // self.vehicle_num 
        for i in range(self.vehicle_num-1): 
            solution.insert((i+1)*step , "|") 
        self.initial_solution = solution
    
    
    def Optimization(self) : 
        self.createGA_instnace()   
        start = time.time()
        self.GA.run() 
        print(time.time()-start)
        solution, solution_fitness, solution_idx = self.GA.best_solution()
        print("best_solution: {solution}".format(solution =[Benchmarker.encodeTalbe[i] for i in solution]))
        print("best_solution fitness: {solution_fit}".format(solution_fit =-1*solution_fitness))
        self.GA.plot_fitness()


if __name__ =="__main__": 
    Benchmarker.setting("map/Relax_small.json")
    Benchmarker.Source_graphLoading()
    #GA =  Genetic_algorithms(initial_solution=["B","C","E","O","P","M","G","H","J","A"])
    GA = Genetic_algorithms(initial_solution=Benchmarker.station_list,vehicle_num=1)
    #encodeTable = GA.encodeTable
    #CostMap = GA.All_pair_cost
    GA.Optimization()