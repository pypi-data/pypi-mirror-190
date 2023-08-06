'''import numpy as np
from scipy.signal import StateSpace, lsim
import matplotlib.pyplot as plt

class StateSpaceSimulation:
    def __init__(self, A, B, C, D):
        self.sys = StateSpace(A, B, C, D)

    def simulate_response(self, t, input_type, input_vals=None):
        t, y, x = lsim(self.sys, input_vals, t)
        return t, y
        
    def plot_response(self, t, y, input_type):
        plt.plot(t, y)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude (m)')
        plt.title('Response of Pendulum to {} Input'.format(input_type))
        plt.show()

# Define the parameters of the pendulum
m = 0.2  # mass of the pendulum
l = 1.0  # length of the pendulum
g = 9.81  # acceleration due to gravity
k = 0.01  # damping coefficient

# Define the state space equation of the pendulum
A = np.array([[-k/m, -g/l], [l, 0]])
B = np.array([[0.1], [0]])
C = np.array([[1, 0], [0, 0]])
D = np.array([0])

# Create a system object from the state space equation
sys = StateSpaceSimulation(A, B, C, D)

# Define the time interval for simulation
t = np.arange(0, 30, 0.01)

# Simulate the response of the pendulum to a step input
t, y = sys.simulate_response(t, 'step', np.ones_like(t))
sys.plot_response(t, y, 'Step')

# Simulate the response of the pendulum to an impulse input
t, y = sys.simulate_response(t, 'impulse', np.array([1 if i == 0 else 0 for i in t]))
sys.plot_response(t, y, 'Impulse')
'''