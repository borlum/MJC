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
    'B': 1.00, # Rot. friction
    'K': 1.00, # Trans. friction
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

uncontrollableModes = ctrl.analysis.uncontrollable_modes(A,B)

sys = sp.StateSpace(A, B, C)

t = np.linspace(0, 5)
u = np.ones((2, len(t))).T
tout, y, x = sp.lsim(sys, u, t)

plt.plot(t, y)
plt.show()

if not uncontrollableModes:
    print('System is controllable.')
else: 
    print('System is uncontrollable. Uncontrollable modes are:')
    print(uncontrollableModes)

# Define our costs:
Q = np.matrix([
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0],
])

R = np.matrix([
    [1, 0],
    [0, 1]
])

# Compute the LQR controller
gain, X, closedLoopEigVals = ctrl.synthesis.controller_lqr(A,B,Q,R)

print('The computed gain is:')
print(gain)

print('The closed loop eigenvalues are:')
print(closedLoopEigVals)