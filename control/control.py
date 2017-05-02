import numpy as np
import scipy.signal as sp
import matplotlib.pyplot as plt
import controlpy as ctrl

# MODEL
p = {
    'k': 1/50, # Torque <-> rot. velo motor
    'R': 0.07, # Wheel radius
    'L': 0.20, # Dist. between wheels
    'b': 0.10, # Dist. from center
    'M': 1.10, # Mass
    'B': 0.1, # Rot. friction
    'K': 0.1, # Trans. friction
}

# Calculate inertia (box)
p['J'] = (p['M'] * p['b']**2) / 4

# State-space system
A = np.matrix([
    [-p['B']/p['J'], 0, 0], 
    [1, 0, 0], 
    [0, 0, -p['K']/p['M']]
])

B = np.matrix([
    [(p['k']*p['L']) / (p['J']*p['R']), -(p['k']*p['L']) / (p['J']*p['R'])], 
    [0, 0], 
    [p['k']/(p['M']*p['R']), p['k']/(p['M']*p['R'])]
])

C = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

sys = sp.StateSpace(A, B, C)

# Check if system is controllable (cross fingers!)
uncontrollableModes = ctrl.analysis.uncontrollable_modes(A,B)

if not uncontrollableModes:
    print('System is controllable.')
else: 
    print('System is uncontrollable. Uncontrollable modes are:')
    print(uncontrollableModes)


# Discretize:
dt = 0.01
(A, B, C, D, dt) = sp.cont2discrete((sys.A, sys.B, sys.C, sys.D), dt)

# Synthesize LQR
Q = np.matrix([
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0],
])

R = np.matrix([
    [1, 0],
    [0, 1]
])

# Compute gain
K, X, closedLoopEigVals = ctrl.synthesis.controller_lqr_discrete_time(
    A, B, Q, R
)

# Adding a reference by feed-forward (dv/dt = 0) NOT WORKING...:
N = np.matrix([
    [2 * p['R']],
    [2 * p['R']]
])

print(N)

x0 = np.matrix([0, 0.5, 0.2]).T
x_ref = np.matrix([0, 0, 0.2]).T
x = x0
x_res = x0
for k in range(1000):
    u = -K * x + 0.2 * N
    print(u)
    x = A * x + B * u
    print(x)