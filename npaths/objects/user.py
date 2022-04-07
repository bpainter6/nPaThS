# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 01:36:49 2022

@author: 17066
"""

import numpy as np
from math import pi
class Rod():

    def __init__(self,Id,channelIds,comp,rOut,nLayer):
        """Allows user to quickly define data about a rod in the system
        
        Parameters
        ----------
        Id - str
            name of the rod
        channelIds - list of int
            channels where the rod is located
        fuA - list of float
            total cross sectional area of the fuel elements in each channel
        comp - list of str
            material composition of the ith radial layer in the rod
        
        """
        
        # rFuel def
        self.rFuel = rOut[-1]
        
        # specify ids
        self.radialIds = list(range(np.sum(np.array(nLayer))))
        self.channelIds = channelIds 
        self.Id = Id
        
        comps = []
        for ndx,n in enumerate(nLayer):
            comps += n*[comp[ndx]]
        
        self.comp = np.array(comps)
        
        # specify radii
        rOut.append(0)
        rOuts = np.array([])
        for ndx,n in enumerate(rOut[:-1]):
            rOutsN = np.linspace(rOut[ndx],rOut[ndx+1],nLayer[ndx]+1)[:-1]
            rOuts = np.append(rOuts,[rOutsN])
        
        self.rOut = rOuts
        self.rIn  = np.append(rOuts[1:],0)