import pygad
import json
from Benchmark_ import Benchmarker
import networkx as nx
import numpy as np
import time


class Genetic_Algorithms:
    # pass the TSP instance , create chromosome according the problem dimension , then construct GA instance
    def __init__(self, initial_solution, vehicle_num=1):

        self.initial_solution = initial_solution
        self.vehicle_num = vehicle_num

        self.dimension = len(self.initial_solution)
        self.num_gene = len(self.initial_solution)
        self.gene_space = [i for i in range(self.dimension)]

        self.encodeTable = {i: node for i,
                            node in enumerate(self.initial_solution)}

        if self.vehicle_num > 1:
            # --> modify self.initial_solution / self.dimension / self.gene_space
            self.MultiVehicle_adjust()

        #self.population_size = 16
        self.initial_population = [list(np.random.permutation(
            self.gene_space)) for i in range(self.population_size)]
        self.encode = lambda solution:  [self.encodeTable[i] for i in solution]

        self.GA = pygad.GA(
            gene_type=int,
            num_generations=self.num_generation,
            num_parents_mating=self.num_paraents_mating,
            fitness_func=self.Fitness_fun(),
            sol_per_pop=self.population_size,
            num_genes=self.num_gene,
            gene_space=self.gene_space,

            K_tournament= 8,
            parent_selection_type=self.parent_selection_type,
            crossover_type=self.crossover_type,
            mutation_type=self.mutation_type,
            mutation_percent_genes=self.mutation_percent,
            allow_duplicate_genes=False,
            keep_parents=self.keep_parents_afterIteration,
            
            ###### plotting ######
            #save_best_solutions=True ,
            ###### life cycle ######
            on_fitness=self.log_fitness()
        )

    @classmethod
    def Parameter(cls):

        cls.num_generation = 650
        cls.num_paraents_mating = 8
        cls.parent_selection_type = "rank"
        
        cls.crossover_type = "two_points"
        cls.mutation_type = "random"
        cls.population_size = 16
        if cls.mutation_type == "adaptive":
            cls.mutation_percent = [25, 10]
        else:
            cls.mutation_percent = 5

        cls.keep_parents_afterIteration = -1

    @classmethod
    def Create_GA_Instance(cls, initial_solution, vehicle_num, plotting=False):
        cls.Parameter()
        return cls(initial_solution, vehicle_num)

    def MultiVehicle_adjust(self):
        base = 1000
        for i in range(1, self.vehicle_num):
            self.gene_space.append(base+i)
            self.encodeTable.update({base+i: "|"})
            
        self.dimension = len(self.gene_space)
        self.num_gene = len(self.gene_space)
        print(self.gene_space)
    def Fitness_fun(self):
        encode = self.encode
        
        def fitness(solution, solution_index):

            return -1*Benchmarker._routeCost(encode(solution))[0]

        def fitness_multi(solution, solution_index):
            
            return -1*Benchmarker.MultiVehicle_Cost(encode(solution),vehicle_num=self.vehicle_num)[0]

        return fitness if self.vehicle_num == 1 else fitness_multi

    def log_fitness(self):
        self.avg_log= [] 
        self.best_log = []
        
        def log(ga_instance,pop_fit): 
            self.best_log.append(-1*pop_fit.max())
            self.avg_log.append(-1*pop_fit.mean())
        return log
    
    def Optimization(self , plotting=False):
        start = time.time()
        self.GA.run()
        end = time.time()
        self.solution, self.solution_fitness, solution_idx = self.GA.best_solution()
        self.solution = self.encode(self.solution) 
        self.solution_fitness = -self.solution_fitness
        print("best_solution: {solution}".format(
            solution=self.solution ) )
        print("best_solution fitness: {solution_fit}".format(
            solution_fit=-self.solution_fitness))
        #self.GA.plot_fitness()
        self.CostTime = end-start
        
        print(self.CostTime)
        if plotting: 
            test_setting = f"optimizer: Genetic\n\nCost:{self.solution_fitness}\n\nIteration+num:{self.num_generation}\n\nCost time:{self.CostTime}\n\nCriterion:MinSum"
            Benchmarker.plotting(Benchmarker.SourceGraph,self.encode(self.solution),"GeneticAlgorithms",Cost_log=self.best_log,testing_set=test_setting,vehicle_num=self.vehicle_num)
   
        


if __name__ == "__main__":
    Benchmarker.setting("map/building_big.json")
    Benchmarker.Source_graphLoading()

    #GA = Genetic_Algorithms.Create_GA_Instance(initial_solution=["B","C","E","O","P","M","G","H","J","A"],vehicle_num=3)
    GA = Genetic_Algorithms.Create_GA_Instance(    initial_solution=Benchmarker.station_list, vehicle_num=3)
   

    GA.Optimization(plotting=0)
   
    for i in range(10): 
       print(f"--------- iter {i} ------")
       GA = Genetic_Algorithms.Create_GA_Instance(    initial_solution=Benchmarker.station_list, vehicle_num=3)
       GA.Optimization(plotting=0)