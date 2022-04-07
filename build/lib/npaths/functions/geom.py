# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 22:32:12 2022

@author: 17066

set of functions that allow user to easily define advanced geometries within 
the core

"""

from math import pi

def channel(shape,pit,grT,rdD,rdN):
    """calculates advanced geometry parameters for the system based in user 
    input
    
    Parameters
    ----------
    shape - str
        defines the shape of the channel (triangle or square)
    pit - float
        defines the pitch of each element in the channel
    grT - float
        spacer grid thickness
    rdD - list of float
        defines the outer diameter of the ith rod in the channel
    rdN - list of float
        defines the number of occurences of the ith rod in the channel
    
    """
    
    flA = 0 # flow area
    wP  = 0 # wetted perimeter
    grA = 0 # gird frontal area
    
    for ndx,d in enumerate(rdD):
        n = rdN[ndx]
        
        wP  += n*pi*d
        flA += n*(pit**2 - pi*(d/2)**2)
        grA += n*(pit**2 - (pit-grT)**2)
    
    hyD = 4*flA/wP
    
    return hyD,flA,grA

def fuel(fuD,fuN):
    """calculates the total cross sectional area of the fuel in a channel
    
    Parameter
    ---------
    fuD - list of float
        diameter of the ith fuel element in the channel
    fuN - list of float
        number of occurences of the ith fuel element in the channel
        
    """
    
    fuA = 0
    
    for ndx,d in enumerate(fuD):
        n = fuN[ndx]
        fuA += n*pi*(d/2)**2
    
    return fuA