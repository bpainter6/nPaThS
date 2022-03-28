# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 22:32:12 2022

@author: 17066
"""

from mutts.objects import dataframes as dfs

def powerFrame(nChannels,nLayers):
    """returns a dataframe that the user can use to specify axial layer power 
    production"""
    
    layerIds = {}
    layerIds['channel'] = list(range(nChannels+1))
    layerIds['axial'] = list(range(nLayers+1))
    
    return dfs.preallocateDF('axial', layerIds, props='q')