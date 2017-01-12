#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pyfmi as fmi
import pyfmi_help as fmi_ex

# Load the FMU
FMU = fmi.load_fmu('../model/MJC_Simulator.fmu')

Ts = 10
T_final = 30
number_samp_tot = int(T_final/Ts)

def control(k, v_left, v_right):
    # Create input object
    t = np.linspace(k*Ts, (k + 1)*Ts)
    u1 = np.ones(len(t))*v_left
    u2 = np.ones(len(t))*v_right
    u = np.transpose(np.vstack((t, u1, u2)))
    return (['v_in_left', 'v_in_right'], u)

res = fmi_ex.create_result_obj(FMU)

x_k = fmi_ex.get_state(FMU, FMU.simulate(), -1)
for k in range(number_samp_tot):
    # Reset the model and set the new initial states 
    FMU.reset()
    FMU.set(x_k.keys(), x_k.values())
    
    # simulate the next sample period with the input u_k
    sim_res = FMU.simulate(
        start_time=k*Ts,
        final_time=(k+1)*Ts, 
        input=control(k, 1, 1)
    )

    # Get new state
    x_k = fmi_ex.get_state(FMU, sim_res, -1)

    # Save data
    res = fmi_ex.append_to_result_obj(FMU, res, sim_res)

# Plot results
fig = plt.figure(1)
fig.hold(True)
plt.plot(
    res['mjc.x'],
    res['mjc.y']
)
plt.ylim([-6, 6])
plt.xlim([-2, 15])
plt.ylabel('y [m]')
plt.xlabel('x [m]')
plt.grid()
plt.show()