# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 01:30:33 2022

@author: 17066
"""

import numpy as np
import pandas as pd
import pickle

nChannel = 31
nAxial = 18

data = np.zeros([nChannel,nAxial])
out = pd.read_excel('dataTH.xlsx')
for it,ndx in enumerate(out):
    if it in [0,1,20,21]:
        continue
    else:
        data[:,it-2] = np.array(out[ndx][2:-5])

data[0,:]  = data[0,:]*8
data[1,:]  = data[1,:]*2
data[2,:]  = data[2,:]*2
data[3,:]  = data[3,:]*2
data[5,:]  = data[5,:]*2
data[6,:]  = data[6,:]*2
data[9,:]  = data[9,:]*2
data[10,:] = data[10,:]*2
data[14,:] = data[14,:]*2
data[15,:] = data[15,:]*2
data[20,:] = data[20,:]*2
data[21,:] = data[21,:]*2
data[27,:] = data[27,:]*2

with open('power.pkl', 'wb') as f:
    pickle.dump(data, f)