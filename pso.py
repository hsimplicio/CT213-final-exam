from behavior_tree_test import simulacao
import random
import numpy as np
from this import d
from math import inf
from utils import Params

class Particle:
    """
    Represents a particle of the Particle Swarm Optimization algorithm.
    """
    def __init__(self, lower_bound, upper_bound):
        """
        Creates a particle of the Particle Swarm Optimization algorithm.

        :param lower_bound: lower bound of the particle position.
        :type lower_bound: numpy array.
        :param upper_bound: upper bound of the particle position.
        :type upper_bound: numpy array.
        """
        
        self.x = np.random.uniform(lower_bound, upper_bound)
        delta = upper_bound - lower_bound
        self.v = np.random.uniform(-delta, delta)
        self.best_position = None
        self.J_best_position = inf


class ParticleSwarmOptimization:
    """
    Represents the Particle Swarm Optimization algorithm.
    Hyperparameters:
        inertia_weight: inertia weight.
        cognitive_parameter: cognitive parameter.
        social_parameter: social parameter.

    :param hyperparams: hyperparameters used by Particle Swarm Optimization.
    :type hyperparams: Params.
    :param lower_bound: lower bound of particle position.
    :type lower_bound: numpy array.
    :param upper_bound: upper bound of particle position.
    :type upper_bound: numpy array.
    """

    def __init__(self, hyperparams, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.count = 0

        self.num_particles = hyperparams.num_particles
        self.omega = hyperparams.inertia_weight
        self.phip = hyperparams.cognitive_parameter
        self.phig = hyperparams.social_parameter

        self.best_global = None
        self.J_best_global = inf
        self.best_iteration = None
        self.J_best_iteration = inf
        
        self.particles = []
        for i in range(0, self.num_particles):
            self.particles.append(Particle(lower_bound, upper_bound))
        self.particles = np.array(self.particles)

    def get_best_position(self):
        """
        Obtains the best position so far found by the algorithm.

        :return: the best position.
        :rtype: numpy array.
        """

        if self.J_best_iteration < self.J_best_global:
            self.J_best_global = self.J_best_iteration
            self.best_global = self.best_iteration

        return self.best_global

    def get_best_value(self):
        """
        Obtains the value of the best position so far found by the algorithm.

        :return: value of the best position.
        :rtype: float.
        """

        return self.J_best_global

    def get_position_to_evaluate(self):
        """
        Obtains a new position to evaluate.

        :return: position to evaluate.
        :rtype: numpy array.
        """
        
        return self.particles[self.count].x

    def advance_generation(self):
        """
        Advances the generation of particles. Auxiliary method to be used by notify_evaluation().
        """
        best_global = self.get_best_position()

        self.best_iteration = None
        self.J_best_iteration = inf

        for particle in self.particles:
            rp = random.uniform(0.0, 1.0)
            rg = random.uniform(0.0, 1.0)
            
            particle.v = self.omega*particle.v + self.phip*rp*(particle.best_position - particle.x) + self.phig*rg*(best_global - particle.x)
            particle.x = particle.x + particle.v

    def notify_evaluation(self, value):
        """
        Notifies the algorithm that a particle position evaluation was completed.

        :param value: quality of the particle position.
        :type value: float.
        """

        J_particle_x = value
        particle = self.particles[self.count]
                
        if J_particle_x < particle.J_best_position:
            particle.J_best_position = J_particle_x
            particle.best_position = particle.x
        if J_particle_x < self.J_best_iteration:
            self.J_best_iteration = J_particle_x
            self.best_iteration = particle.x

        if self.count < self.num_particles - 1:
            self.count += 1
        else:
            self.count = 0
            self.advance_generation()


'''
Possible initial conditions

move_foward_time = 3.0  # time moving forward before switching to the spiral behavior
move_in_spiral_time = 20.0  # time moving in spiral before switching back to moving forward
go_back_time = 0.5  # time going back after hitting a wall
spiral_factor = 0.05  # factor used to make the spiral grow while the time passes
initial_radius_spiral = 0.2  # initial spiral radius

initial_guess = np.array([move_foward_time, move_in_spiral_time, go_back_time, spiral_factor, initial_radius_spiral])
'''

# Defining hyperparameters for the algorithm
hyperparams = Params()
hyperparams.num_particles = 40
hyperparams.inertia_weight = 0.7
hyperparams.cognitive_parameter = 0.6
hyperparams.social_parameter = 0.8
# Defining the lower and upper bounds
lower_bound = np.array([0.8*3.0, 0.8*20.0, 0.8*0.5, 0.8*0.05, 0.8*0.2])
upper_bound = np.array([1.2*3.0, 1.2*20.0, 1.2*0.5, 1.2*0.05, 1.2*0.2])
pso = ParticleSwarmOptimization(hyperparams, lower_bound, upper_bound)

num_evaluations = 500
n = 0
epsilon = 75
position = pso.get_position_to_evaluate()
value = inf
while n <= num_evaluations and value > epsilon:
  n += 1
  print(n,'. ')
  position = pso.get_position_to_evaluate()
  value = simulacao(position[0], position[1], position[2], position[3], position[4])
  pso.notify_evaluation(value)

# Finally, print the best position found by the algorithm and its value
print('Best position:', pso.get_best_position())
print('Best value:', pso.get_best_value())