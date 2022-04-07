# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 17:29:52 2022

@author: 17066
"""

import matplotlib.pyplot as plt
import numpy as np

def channelPlot(data,channelMap,label=None,vmin=None,vmax=None,save=None):
    """Allows user to plot channel data by providing a channel map
    
    parameters
    ----------
    data - 1D array
        an array of data describing a property at each channel
    channelMap - 2D array
        a map describing the geometrical position of a channel based on its
        channel index
    label - str
        label of the property being plotted. (shown adjacent to colorbar)
    vmin/vmax - float
        min/max values that the colorbar can represent
    
    """
    
    # convert to 2D array
    dataMap = mapData(data,channelMap)
    
    plt.matshow(dataMap,cmap=plt.get_cmap('plasma'),vmin=vmin,vmax=vmax)
    cbar = plt.colorbar()
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel(label, rotation=270)
    plt.axis('off')
    
    # save figure
    if not isinstance(save,type(None)):
        plt.savefig(save)

def mapData(data,channelMap):
    shape = np.shape(channelMap)
    out = np.zeros(shape)
    for row in range(shape[0]):
        for col in range(shape[1]):
            ndx = channelMap[row][col]
            if ndx == -1:
                out[row][col] = np.nan
            else:
                out[row][col] = data[ndx]
    return out