#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyfmi as fmi
import pymodelica as pym
 
# Model object
model = {'name': 'MJC', 'file': 'model.mo'}

# Path to dependencies and problem
paths = model['file']

# Get state names and their values at given index
def get_x(fmu, results, index):
    # Identify states as variables with a _start_ value
    identifier = "_start_"
    keys = fmu.get_model_variables(filter=identifier + "*").keys()
    # Now, loop through all states, get their value and put it in x
    x = {}
    for name in keys:
         x[name] = results[name[len(identifier):]][index]
    # Return state
    return x

# Compile an FMU
model['FMU'] = pym.compile_fmu(
    "MJC.Simulator", paths,
    compiler_options = {"state_initial_equations": True}
)

# Load the FMU
model['sim'] = fmi.load_fmu(model['FMU'])

Ts = 10;
T_final = 100;
number_samp_tot = int(T_final/Ts)

def control(k):
    # Create input object
    t = np.linspace(k*Ts, (k + 1)*Ts)
    u = np.ones(len(t))*12
    u = np.transpose(np.vstack((t, u, u)))
    return (['v_in_left', 'v_in_right'], u)

# Initialize
fig = plt.figure(1)
fig.hold(True)

x_k = get_x(model['sim'], model['sim'].simulate(), -1)
for k in range(number_samp_tot):
    # Reset the model and set the new initial states 
    model['sim'].reset()
    model['sim'].set(x_k.keys(), x_k.values())
    
    # simulate the next sample period with the input u_k
    sim_res = model['sim'].simulate(
        start_time=k*Ts, 
        final_time=(k+1)*Ts, 
        input=control(k)
    )

    # Get new state
    x_k = get_x(model['sim'], sim_res, -1)

    # Plot results
    plt.plot(
        sim_res['mjc.x'],
        sim_res['mjc.y']
    )

plt.show()