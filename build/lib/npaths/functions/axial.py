# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 21:14:23 2022

@author: 17066
"""

from CoolProp.CoolProp import PropsSI
import numpy as np
import copy

# Global vars
WATER = 'IF97::Water'

###############################################################################
### MAIN ######################################################################
###############################################################################

def axialHelper(pIn,tIn,mDot,q,hyD,Af,dz):
    """Solves bulk and exit coolant properties within an axial layer"""
    
    # entrance flow rate conditions
    inFlow = Flow()
    inFlow.solve(mDot,Af,"P",pIn,"T",tIn,WATER)
    
    # inital guess for bulk and outlet coolant props
    avFlow  = copy.deepcopy(inFlow)
    outFlow = copy.deepcopy(inFlow)
    
    # initial guess of outlet temperature and pressure
    tOut = copy.deepcopy(tIn)
    pOut = copy.deepcopy(pIn) 
    
    # loop until outlet pressure converges
    pOuts = np.array([pOut])
    while True:
        
        # loop until outlet temperature converges
        tOuts = np.array([tOut])
        while True:
            
            # calc outlet conditions
            outFlow.solve(mDot,Af,"P",pOut,"T",tOut,WATER)
            
            # calc bulk coolant flow
            avFlow = averageFlow(outFlow,inFlow)
            cp   = avFlow['cp']
            
            # solve for Tout
            tOut = q/(mDot*cp)+tIn
            tOuts = np.append(tOuts,tOut)
            
            # check outlet temperature convergence
            if convTest(tOuts):
                break
        
        # calculate pressure drop
        dP = PressDrop(inFlow,outFlow,avFlow,mDot,hyD,Af,dz)
        
        # solve Pout
        pOut = pIn - dP['dPtotal']
        pOuts = np.append(pOuts,pOut)
        
        # check outlet pressure convergence
        if convTest(pOuts):
            break
    
    # average pressure, temperature
    p = (pIn+pOut)/2
    t = (tIn+tOut)/2
    
    # extract pressure drop data
    dPtot,dPaccl,dPgrav,dPfric = \
        dP['dPtotal'],dP['dPaccl'],dP['dPgrav'],dP['dPfric']
    
    # extract bulk coolant props
    rho,mu,vel = \
        avFlow['rho'],avFlow['mu'],avFlow['vel']
    
    # output results
    return pIn,p,pOut,tIn,t,tOut,dPtot,dPaccl,dPgrav,dPfric,cp,rho,mu,vel

###############################################################################
### HELPER FUNCTIONS ##########################################################
###############################################################################

def averageFlow(*flows):
    """Takes in multiple flow objects, averages their properties, and 
    outputs a new Flow object with these average properties"""
    
    outFlow = Flow()
    
    # append data from all flows into the output flow
    for flow in flows:
        for key,val in flow.items():
            try:
                np.append(outFlow[key],val)
            except:
                outFlow[key] = np.array([val])
    
    # average all data contained in outFlow
    for key,val in outFlow.items():
        outFlow[key] = np.mean(val)
    
    return outFlow    

def frictionFactor(Re):
    """Returns the friction factor based on the Re of a flow"""
    
    if Re<2200:
        # Laminar
        f = 64/Re
    elif Re<30000:
        # Blasius
        f = 0.316*Re**(-0.25)
    else:
        # McAdams
        f = 0.184*Re**(-0.20)
    return f

def convTest(vec):
    """returns whether a vector of values has converged on a steady value"""
    
    # return result based on difference in last two values
    return abs(vec[-1]-vec[-2])/vec[-1] < 0.001

###############################################################################
### HELPER OBJECTS ############################################################
###############################################################################

class Flow(dict):
    """Object that stores data related to the flow at a certain point in a 
    system"""
    
    def __init__(self):
        """initialize the flow object"""
    
    def solve(self,mDot,Af,*args):
        """solve the flow properties based on flow conditions"""
        
        # cp J/kgK
        self['cp']  = PropsSI("C",*args)
        
        # viscosity Pa-sec
        self['mu']  = PropsSI("V",*args) 
        
        # density kg/m**3
        self['rho'] = PropsSI("D",*args)
        
        # fluid velocity
        self['vel'] = mDot/self['rho']/Af

class PressDrop(dict):
    """Object that calculates and stores the partial pressure drops and total 
    pressure drop in a system"""
    
    def __init__(self,inFlow,outFlow,avFlow,mDot,hyD,Af,dz):
        """Calculates partial pressure drops and stores them in the object"""
        
        # coolant boundary properties
        velOut = outFlow['vel']
        velIn  = inFlow['vel']
        
        # bulk coolant properties
        rho  = avFlow['rho']
        mu   = avFlow['mu']
        vel  = avFlow['vel']
        
        # Re number and friction factor
        Re = hyD*mDot/(mu*Af)
        f =  frictionFactor(Re)
        
        # acceleration pressure drop
        dPaccl = rho*(velOut**2-velIn**2)/2
        self['dPaccl'] = dPaccl
        
        # gravity pressure drop
        dPgrav = rho*9.81*dz
        self['dPgrav'] = dPgrav
        
        # friction pressure drop
        dPfric = f*dz/hyD*rho*(vel**2)/2
        self['dPfric'] = dPfric
        
        # total dP
        self['dPtotal'] = dPaccl + dPgrav + dPfric