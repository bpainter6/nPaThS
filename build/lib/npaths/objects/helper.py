# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 21:13:24 2022

@author: 17066
"""

from npaths.functions import helper as fhp
import numpy as np

def Rod(dict):
    """Object describing the geometry and composition of a fuel rod within an
    axial layer"""
    def __init__(self,comp=None,nLayer=None,rOut=None):
        """Initialize rod with user specified data"""
        
        nInput = len(comp)
        
        # initialize mats list, rads array
        mats = []
        rads = np.array([])
        
        for ndx,mat in enumerate(mats):
            
            mats += comp[ndx]*nLayer[ndx]
            
            if ndx == 0:
                tmpRads = np.linspace(rOut[ndx],rOut[ndx+1],nLayer[ndx]+1)
            elif ndx == nInput-1:
                # final specified material should go to r = 0
                tmpRads = np.linspace(rOut[ndx],0          ,nLayer[ndx]+1)[1:]
            else:
                # exclude first value to avoid repition in rads
                tmpRads = np.linspace(rOut[ndx],rOut[ndx+1],nLayer[ndx]+1)[1:]
               
            rads = np.concatenate((rads,tmpRads))
        
        self.mats = mats
        self.rads = rads

def Geom(dict):
    """Object describing the geometry of a an axial layer within a 
    singleChannel """
    
    def __init__(self):
        """initialize the Geom object"""

def RadCond(dict):
    """dictionary describing the radial temperature distribution within an axial
    layer"""
    
    def __init__(Tc,geom):
        """Solve the radial temperature distribution then store it in the
        Temps object"""
        
        # Inner clading temperature
        Tg = fhp.getRadTemp(Tc,'Zircaloy',1)
        kc = fhp.getConductivity('Zircaloy', Tc)
        Tg = log(Rc/Rg)/kc*(Rf**2)*densQ/2+Tc
        
        # Outer fuel temperature
        kg = fhp.getConductivity('Helium', Tg)
        Tf = log(Rg/Rf)/kg*(Rf**2)*densQ/2 + Tg
        Tfg = (Tf+Tg)/2
        kg = fhp.getConductivity('Helium', Tfg)  # update the conductivity
        Tf = log(Rg/Rf)/kg*(Rf**2)*densQ/2 + Tg