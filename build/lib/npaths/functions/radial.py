# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 00:08:59 2022

@author: 17066
"""

from math import exp,log
import numpy as np

def radialHelper(Q,rIn,rOut,rF,comp,tOut):
    """returns the radial temperature distribution through an annular element
    
    Parameters
    ----------
    Q - float
        volumetric heat generation in the axial layer
    rOut - float
        outer radius of the element
    rIn - float
        inner radius of the element
    rF - float
        outer radius of the fuel element
    comp - str
        comp name in the element
    tOut - int
        temperature at the outer radius of the segment
    
    """
    
    # Initial Tout guess
    tIn = tOut
    tIns = np.array([tIn])
    
    while True:
        t   = (tOut + tIn)/2
        k   = getConductivity(comp, t)
        
        if comp == 'UO2':
            tIn = Q/4/k*(rOut**2-rIn**2)+tOut
        else:
            tIn = Q/2/k*(rF**2)*log(rOut/rIn)+tOut
        
        tIns = np.append(tIns,tIn)
        
        if convTest(tIns):
            break
    
    return tIn,t,tOut,k

def getConductivity(material, tempK):
    """returns the conductivity of a material at temperature (in K)"""
    
    if (material == 'UO2'):
        tempC = tempK - 273.15
        k = 1/(0.1148+2.475E-4*tempC)+0.0132*exp(0.00188*tempC)
    
    elif (material == 'Zircaloy'):
        k = 12.767 - 5.4348E-4*tempK+8.9818E-6*tempK**2
    
    elif (material == 'Helium'):
        k = 15.80E-4*(tempK**(0.79))
    
    else:
        print('This material does not exist')
        return -1
    
    return k

def convTest(vec):
    """returns whether a vector of values has converged on a steady value"""
    
    # return result based on difference in last two values
    return abs(vec[-1]-vec[-2])/vec[-1] < 0.001