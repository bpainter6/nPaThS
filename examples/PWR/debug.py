# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 02:04:30 2022

@author: 17066
"""

import npaths
import numpy as np
import pickle

# import 2D power array
with open('power.pkl', 'rb') as f:
    power = pickle.load(f)

fuD = 0.819/100     # fuel pellet diameter
clD = 0.950/100     # clad diameter and fule rod outer diameter
guD = 1.224/100     # guide tube outer diameter
fuN = 264           # number of fuel rods
guN = 25            # number of guide tubes
grT = 0.45/1000    # spacer grid thickness
pit = 1.26/100      # pitch of elements in the channel

# calculate advanced geometery
hyD,flA,grA = npaths.geom.channel('square',pit,grT,[clD,guD],[fuN,guN])
fuA = npaths.geom.fuel([fuD],[fuN])

# space grid locations
grA = [0]+[grA]+[0]+[grA]+[0]+[grA]+[0]+[grA]+2*[0]+[grA]+[0]+[grA]\
               +[0]+[grA]+[0]+[grA]+[0]

# define adavanced geometry for each channel with the array
hyD = np.array(31*[hyD])
flA = np.array(31*[flA])
grA = np.array(31*(grA))
fuA = np.array(31*[fuA])

# define axial layer thickness
dz  = np.array(3*[21]+12*[20]+3*[21])/100

# initialize multichannel object
core = npaths.MultiChannel(fuA,dz)

# update multiChannel advanced geometry values
core.update("channel",(slice(None)),['hyD','flA'],(hyD,flA))
core.update("axial",(slice(None)),['q','grA'],(power,grA))

# solve flow properties with specific inlet conditions
mDot = 2325
pIn  = 15.6e+06
tIn  = 289.1+273.15
core.solveFlow(mDot,pIn,tIn)

# save flow data to pickle file
# with open('core.pkl', 'wb') as f:
    # power = pickle.dump(core, f)