#!/usr/bin/python
import pymodelica as pym

# Paths: both to Modelica-file and perhaps 3rd party libs
paths = 'model.mo'

# Compile an FMU
pym.compile_fmu(
    "MJC.Simulator", paths,
    compiler_options = {"state_initial_equations": True}
)