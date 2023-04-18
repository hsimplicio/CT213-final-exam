# Metaheuristics for parameter optimization of a Roomba robot

## Abstract
The present work is based on the use of metaheuristic-based algorithms to optimize the parameters of a Roomba robot. Such a robot can perform a series of movements based on a behavior tree, including walking forward, spiraling, walking backward, and rotating. The time it takes for each action is of great importance for the total time it takes for the Roomba to traverse all or most of the area in which it operates. Therefore, 4 metaheuristic algorithms are used to optimize these parameters and find an optimal solution.

## Instructions to execute the code

Each algorithm was implemented in its respective file: `genetic_algorithm.py`, for *Genetic Algorithm*; `simulated_annealing.py`, for *Simulated Annealing*; `pso.py`, for *Particle Swarm Optimization*; and `cmaes.py`, for *CMA-ES*. To run an algorithm, simply execute the corresponding file.

To change the number of simulations used to calculate the average time for a given set of parameters, simply change the value of the variable `n`, in line 21 of the file `behavior_tree_test.py`.
