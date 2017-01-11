#!/usr/bin/python
import matplotlib.pyplot as plt
import pyfmi as fmi
import pymodelica as pym
 
# Model object
model = {'name': 'MJC', 'file': 'model.mo'}

# Path to dependencies and problem
paths = model['file']

T_final = 100

# Compile an FMU
model['FMU'] = pym.compile_fmu("MJC.Simulator", paths)

# Load the FMU
model['sim'] = fmi.load_fmu(model['FMU'])

# Simulate
model['sim_result'] = model['sim'].simulate(start_time=0., final_time=T_final)

# Plot results
fig = plt.figure(1)
fig.hold(True)

rows = 3
cols = 1

plt.subplot2grid((rows,cols), (0,0), colspan=1, rowspan=1)
plt.plot(
    model['sim_result']['mjc.x'],
    model['sim_result']['mjc.y']
)

plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.ylim([-20, 20])
plt.xlim([-20, 20])
plt.grid(True)

plt.subplot2grid((rows,cols), (1,0), colspan=1, rowspan=1)
plt.plot(
    model['sim_result']['time'],
    model['sim_result']['mjc.v']
)
plt.ylabel('v [m/s]')
plt.ylim([0, 0.4])
plt.grid(True)

plt.subplot2grid((rows,cols), (2,0), colspan=1, rowspan=1)
plt.plot(
    model['sim_result']['time'],
    model['sim_result']['mjc.omega']
)

plt.xlabel('Time [s]')
plt.ylabel('$\omega$ [rad/s]')
plt.ylim([0, 0.08])
plt.grid(True)

plt.show()