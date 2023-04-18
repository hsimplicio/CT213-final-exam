import cma
from behavior_tree_test import simulacao
from math import sin, cos, pi, exp
import random
import numpy as np


# Hyperparameters used for computing the random neighbor
delta = 2.0e-1
# Hyperparameters used for computing the temperature scheduling
temperature0 = 1.0
beta = 1.0

def random_neighbor(theta):
    """
    Returns a random neighbor of theta.
    The random neighbor is sampled around a circle of radius <delta>.
    The probability distribution of the angle is uniform(-pi, pi).

    :param theta: current point.
    :type theta: numpy.array.
    :return: random neighbor.
    :rtype: numpy.array.
    """

    random_angle = random.uniform(0,2*pi)
    neighbor = theta.copy()
    neighbor[0] = theta[0] + delta*cos(random_angle)
    neighbor[1] = theta[1] + delta*sin(random_angle)

    return neighbor

def schedule(i):
    """
    Defines the temperature schedule of the simulated annealing.

    :param i: current iteration.
    :type i: int.
    :return: current temperature.
    :rtype: float.
    """

    return  temperature0/(1+beta*(i**2))

def simulated_annealing(simulacao, random_neighbor, schedule, theta0, epsilon, max_iterations):
    """
    Executes the Simulated Annealing (SA) algorithm to minimize (optimize) a cost function.

    :param cost_function: function to be minimized.
    :type cost_function: function.
    :param random_neighbor: function which returns a random neighbor of a given point.
    :type random_neighbor: numpy.array.
    :param schedule: function which computes the temperature schedule.
    :type schedule: function.
    :param theta0: initial guess.
    :type theta0: numpy.array.
    :param epsilon: used to stop the optimization if the current cost is less than epsilon.
    :type epsilon: float.
    :param max_iterations: maximum number of iterations.
    :type max_iterations: int.
    :return theta: local minimum.
    :rtype theta: np.array.
    :return history: history of points visited by the algorithm.
    :rtype history: list of np.array.
    """

    theta = theta0
    history = [theta0]
    n = 0
    while n <= max_iterations:
      T = schedule(n)
      n += 1
      if T < 0:
        break
      neighbor = random_neighbor(theta)
      deltaE = simulacao(neighbor[0],neighbor[1],neighbor[2],neighbor[3],neighbor[4]) - simulacao(theta[0],theta[1],theta[2],theta[3],theta[4])
      if deltaE < 0:
        theta = neighbor
        history.append(neighbor)
      else:
        r = random.uniform(0,1)
        print("aqui1")
        if r >= np.exp(deltaE/T):
          print("aqui2")
          theta = neighbor
          history.append(neighbor)
    print("aqui2")
    return theta, history



def fit_simulated_annealing():
    """
    Uses Simulated Annealing (SA) to fit the ball parameters.

    :return theta: array containing the initial speed and the acceleration factor due to rolling friction.
    :rtype theta: numpy.array.
    :return history: history of points visited by the algorithm.
    :rtype history: list of numpy.array.
    """
    
    theta, history = simulated_annealing(simulacao, random_neighbor, schedule, initial_guess, 5, 300)
    return theta, history

move_foward_time = 3.0  # time moving forward before switching to the spiral behavior
move_in_spiral_time = 20.0  # time moving in spiral before switching back to moving forward
go_back_time = 0.5  # time going back after hitting a wall
spiral_factor = 0.05  # factor used to make the spiral grow while the time passes
initial_radius_spiral = 0.2  # initial spiral radius

#a = simulacao(move_foward_time, move_in_spiral_time, go_back_time, spiral_factor, initial_radius_spiral)

initial_guess = np.array([move_foward_time, move_in_spiral_time, go_back_time, spiral_factor, initial_radius_spiral])

# Solving the problem using Simulated Annealing algorithm
theta_sa, history_sa = fit_simulated_annealing()

print(theta_sa)