import pygad
from behavior_tree_test import simulacao
import numpy as np
from constants import *

def fitness_func(solution, solution_idx):
    output = simulacao(solution[0],solution[1],solution[2],solution[3],solution[4])
    fitness = 1.0 / np.abs(output)
    return fitness

fitness_function = fitness_func

num_generations = 50
num_parents_mating = 4

sol_per_pop = 8
num_genes = 5 #numero de solucoes

init_range_low = -2
init_range_high = 5

parent_selection_type = "sss"
keep_parents = 1

crossover_type = "single_point"

mutation_type = "random"
mutation_percent_genes = 10


ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_function,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       init_range_low=init_range_low,
                       init_range_high=init_range_high,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes,
                       gene_space=[[MOVE_FORWARD_TIME_ORIGINAL*0.8,MOVE_FORWARD_TIME_ORIGINAL*1.2],[MOVE_IN_SPIRAL_TIME_ORIGINAL*0.8,MOVE_IN_SPIRAL_TIME_ORIGINAL*1.2],[GO_BACK_TIME_ORIGINAL*0.8,GO_BACK_TIME_ORIGINAL*1.2],[SPIRAL_FACTOR_ORIGINAL*0.8,SPIRAL_FACTOR_ORIGINAL*1.2],[INITIAL_RADIUS_SPIRAL_ORIGINAL*0.8,INITIAL_RADIUS_SPIRAL_ORIGINAL*1.2]])

ga_instance.run()


solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))

#prediction = np.sum(np.array(function_inputs)*solution)
#print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))

