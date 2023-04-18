import cma
from behavior_tree_test import simulacao
import numpy as np
from math import inf


'''
Possible initial conditions

move_foward_time = 3.0  # time moving forward before switching to the spiral behavior
move_in_spiral_time = 20.0  # time moving in spiral before switching back to moving forward
go_back_time = 0.5  # time going back after hitting a wall
spiral_factor = 0.05  # factor used to make the spiral grow while the time passes
initial_radius_spiral = 0.2  # initial spiral radius

initial_guess = np.array([move_foward_time, move_in_spiral_time, go_back_time, spiral_factor, initial_radius_spiral])
'''

# CMA-ES parameters
lower_bound = np.array([0.8*3.0, 0.8*20.0, 0.8*0.5, 0.8*0.05, 0.8*0.2])
upper_bound = np.array([1.2*3.0, 1.2*20.0, 1.2*0.5, 1.2*0.05, 1.2*0.2])
m0 = np.random.uniform(lower_bound, upper_bound)  # initial guess used in the optimization algorithm
sigma0 = 1.0  # initial step size (CMA-ES)

es = cma.CMAEvolutionStrategy(m0, sigma0,{'popsize':5})

num_iterations = 50
n = 0
epsilon = 75
value = inf
while n < num_iterations and value > epsilon:
    n += 1
    print(n,'. ')
    samples = es.ask()
    fitnesses = [simulacao(sample[0],sample[1],sample[2],sample[3],sample[4]) for sample in samples]
    value = np.min(fitnesses)
    es.tell(samples, fitnesses)

es.result_pretty()  # where the result can be found