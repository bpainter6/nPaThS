# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 02:04:30 2022

@author: 17066
"""

import npaths
import numpy as np
import pickle
from math import pi

with open('power.pkl', 'rb') as f:
    power = pickle.load(f)

# calc hydraulic diameter
Dfuel  = 0.950/100
Dguide = 1.224/100
pitch  = 1.26/100
nf     = 264
ng     = 25
Pfuel  = pi*Dfuel 
Pguide = pi*Dguide
Afuel  = pitch**2 - pi/4*(Dfuel**2) 
Aguide = pitch**2 - pi/4*(Dguide**2)
Af     = nf*Afuel + ng*Aguide
Pw     = nf*Pfuel + ng*Pguide
hyD    = 4*Af/Pw

# initialize inputs
hyD = np.array(31*[hyD])
Af  = np.array(31*[Af])
dz = np.array(3*[21]+12*[20]+3*[21])/100

core = npaths.MultiChannel(power,dz,hyD,Af)

# solve with sepcific inputs
mDot = 2325
pIn  = 15.6e+06
tIn  = 289.1+273.15
core.solve(mDot,pIn,tIn)