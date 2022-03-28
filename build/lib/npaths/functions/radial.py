# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 00:08:59 2022

@author: 17066
"""


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

def getRadTemp(Tout,Rout,Rin,mat,qDens,nSeg=False):
    """returns the radial temperature distribution through an annular element
    
    Parameters
    ----------
    Tout - float
        temperature at the outer boundary
    Rout - float
        outer radius of the element
    Rin - floar
        inner radius of the element
    mat - str
        material name in the element
    qDens - float
        volumetric heat generation in the element
    nSeg - int
        number of segments in the element used to calculate distribution. If
        left unspecified, nSeg will be calculated automatically
    
    """
    
    volI = (pi*Rf**2)/nSeg  # volume of each ring
    Rout, Tout = Rf, Tf     # Temperature at the surface (at Rf)
    Ti, Ri = [Tf], [Rf]     # lists to store temperature for each node
    idx = 1
    while (idx < segN + 1):
        kf = getConductivity('UO2', Tout)       # W/mK
        if idx == segN:                         # prevent negative value caused by roundoff errors
            Rin = 0.0
        else:
            Rin = (Rout**2-volI/pi)**0.5                          # calculate the next distance from center
        Ri.append(Rin)                              # store the radius in the list
        Tin = -densQ/4/kf*(Rin**2-Rout**2)+Tout                             # calculate the temperature at Rin
        Ti.append(Tin)                              # append to a list
        Rout, Tout = Rin, Tin                       # update the BCs for the next ring
        idx += 1                                    # continue to the next ring
    print('Tm={:2.1f} kelvin at r={:2.6f}'.format(Tout,Rin))