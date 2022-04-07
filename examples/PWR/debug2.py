# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 02:10:43 2022

@author: 17066
"""

import npaths
import pickle

# flow data
with open('core.pkl', 'rb') as f:
    core = pickle.load(f)

fuD = 0.819/100     # fuel pellet diameter
clD = 0.950/100     # clad diameter and fule rod outer diameter

# create define fuel rod geometry and locarions with the rod object
fuelRod = npaths.Rod("fuel",list(range(31)),['Zircaloy','UO2'],[clD,fuD],[3,3])

# solve fuelTemps
core.solveTemps(fuelRod)