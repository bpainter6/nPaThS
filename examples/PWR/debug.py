# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 02:04:30 2022

@author: 17066
"""

import npaths
import numpy as np
import pickle
import tests as tst

a = 2
b = 3

out = tst.testDebug(a,b)

with open('power.pkl', 'rb') as f:
    power = pickle.load(f)
    
hyD = np.array(31*[5])
dz = np.array(3*[21]+12*[20]+3*[21])/100

core = npaths.MultiChannel(power,dz,hyD)