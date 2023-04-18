# Metaheuristics for parameter optimization of a Roomba robot

**Authors:** Antônio Espínola Navarro Neto; Henrique Silva Simplicio.

Simulation code of Roomba written by Prof Dr Marcos R. O. A. Maximo.

## Abstract
The present work is based on the use of metaheuristic-based algorithms to optimize the parameters of a Roomba robot. Such a robot can perform a series of movements based on a behavior tree, including walking forward, spiraling, walking backward, and rotating. The time it takes for each action is of great importance for the total time it takes for the Roomba to traverse all or most of the area in which it operates. Therefore, 4 metaheuristic algorithms are used to optimize these parameters and find an optimal solution.

## Instructions to execute the code

Each algorithm was implemented in its respective file: `genetic_algorithm.py`, for *Genetic Algorithm*; `simulated_annealing.py`, for *Simulated Annealing*; `pso.py`, for *Particle Swarm Optimization*; and `cmaes.py`, for *CMA-ES*. To run an algorithm, simply execute the corresponding file.

To change the number of simulations used to calculate the average time for a given set of parameters, simply change the value of the variable `n`, in line 21 of the file `behavior_tree_test.py`.

## References

  • D. E. Goldberg, "Genetic algorithms in search, optimization, and machine learning", EUA: Addison-Wesley, 1989.

  •  M. Pincus, "A Monte-Carlo method for the approximate solution of certain types of constrained optimization problems", Journal of the Operations Research Society of America, Nov–Dec 1970. https://doi.org/10.1287/opre.18.6.1225

  • N. Hansen, "The CMA evolution strategy", Dec. 2016. Accessed: July 17, 2022. [Online]. Available: https://cma-es.github.io/

  • J. Kennedy and R. Eberhart, "Particle swarm optimization", Proceedings of ICNN'95 - International Conference on Neural Networks, 1995, pp. 1942-1948 vol.4, https://doi.org/10.1109/ICNN.1995.488968.

  • M. R. Bonyadi and Z. Michalewicz, "Particle Swarm Optimization for Single Objective Continuous Space Problems: A Review", Evol Comput, 2017, pp. 1–54 vol. 25 (1). https://doi.org/10.1162/EVCO_r_00180
