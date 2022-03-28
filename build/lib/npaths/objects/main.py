# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 21:12:51 2022

@author: 17066
"""

import numpy as np
import copy
import pandas as pd
from npaths.functions import dataframes as dfs
from npaths.functions import axial as axl
from npaths.functions import radial as rad

# Global vars
WATER = 'IF97::Water'

class MultiChannel():
    """Object that fully describes the collection of channels inside a 
    system
    
    attributes
    ----------
    multiChannel - pandas dataframe
        data frame describing properties of the system at the multiChannel 
        level
    channel - pandas dataframe
        data frame describing ... channel level
    axial - pandas dataframe
        data frame describing ... axial layer level
    rod - pandas dataframe
        data frame describing ... rod level
    radial - pandas dataframe
        data frame describing ... radial layer level
    nChannel - int
        number of channels in the system
    nAxial - int
        number of axial layers in the system
    layerIds - dict
        keys describe the layer, values are a list of corresponding Ids used 
        at that layer
    
    """
    
    def __init__(self,power,dz,hyD):
        """Initializes the MultiChannel object by filling all data specificed
        in the dictionaries
        
        parameters
        ----------
        power - 2D array
            each row represents the power along the nth channel
        dz - 1D array
            describes the width of the axial layers in the system
        hyD - 1D array
            describes the hydraulic diameter of the nth channel
        
        """
        
        nChannel = len(hyD)
        nAxial = len(dz)
        
        layerIds = {}
        layerIds['channel'] = list(range(nChannel+1))
        layerIds['axial'] = list(range(nAxial+1))
        
        # preallocate layer attributes
        # layers = ['multiChannel','channel','axial','rod','radial']
        layers = ['multiChannel','channel','axial']
        for layer in layers:
            frame = dfs.preallocateDF(layer,layerIds=layerIds)
            setattr(self,layer,frame)
        
        # specify remaining information
        for channelId in layerIds['channel']:
            # update properties in the channel
            self.update('channel',(channelId),['hyD'],hyD[channelId])
            
            for axialId in layerIds['axial']:
                # update properties in the axial layer
                out = (dz[axialId],power[channelId,axialId])
                self.update('axial',(channelId,axialId),['dz','q'],out)
    
    def _stepSolve(self,mDotFrame):
        """Fully solves the system for the specified input mass flow rates.
        A single solution step in solving the full core coolant props
        
        parameters
        ----------
        mDotDict - dictionary
            keys describe the name of a channel, values are a float describing
            the mass flow rate through the channel
        Pin - float
            inlet pressure to the multi channel system
        Tin - float
            inlet temperature to the multi channel system
        
        """
        
        layerIds = self.layerIds
        
        # solve axial bulk coolant properties
        for channelId in layerIds['channel']:
            # get the inlet conditions and flow geometry for the channel
            mDot,tIn,pIn,hyD = self.get('channel',(channelId),
                                           ['mDot','tIn','pIn','hyD'])
            
            # solve and save coolant properties in each axial layer
            for axialId in layerIds['axial']:
                # get power production and geometry at the axial layer
                q,dz = self.get('axial',(channelId,axialId),['q','dz'])
                
                # solve coolant properties for the axial layer
                out = axl.axialHelper(pIn,tIn,mDot,q,hyD,dz)
                
                # save coolant properties for the axial layer
                self.update('axial',(channelId,axialId),
                            ['pIn','p','pOut','tIn','t','tOut'],out)
                
                # update entrance conditions for the next layer
                tIn,pIn = self.get('axial',(channelId,axialId),['tOut','pOut'])
                
    def _axialSolve(self):
        """Iteratively solves coolant properties. Converges when pressure 
        drops are uniform over each channel"""
        
        layerIds = self.layerIds
        
        # divide flow equally between channels
        mDotInit = self.get('multiChannel',(),['mDot'])/self.nChannels
        
        # assign inital flow values to each channel
        for channelId in layerIds['channel']:
            self.update('channel',(channelId),['mDot'],mDotInit)
    
    def _radialSolve(self):
        """Solves rod properties using the obtained coolant properties"""
        pass
    
    def solve(self,mDot,pIn,tIn):
        """Fully solves coolant and rod properties for specified values.
        first iteratively solves coolant properties. Then uses coolant 
        properties to solve rod properties.
        
        parameters
        ----------
        mDot - float
            float describing the 
        Pin - float
            inlet pressure to the multi channel system
        Tin - float
            inlet temperature to the multi channel system
            
        """
        
        self.multiChannel['mDot'] = mDot
        self.multiChannel['pIn'] = pIn
        self.multiChannel['tIn'] = tIn
        
        # solve coolant properties at each axial layer
        self._axialSolve()
        
        # solve rod properties at each radial layer
        # self._radialSolve()
        
    def get(self,layer,index,props):
        """Returns a dataframe at a certain layer of the system
        
        Parameters
        ----------
        layer - str
            layer of the system that dataFrame should be extracted from
        index - tuple
            tuple describing the slice of the data frame to be taken
        props - list
            list of properties to slice from the data frame
        
        """
        
        return getattr(self,layer).loc[index,props]
    
    def update(self,layer,index,props,vals):
        """Updates value in a data frame
        
        Parameters
        ----------
        layer - str
            layer of the system that dataFrame should be extracted from
        index - tuple
            tuple describing the slice of the data frame to be taken
        props - list
            list of properties to slice from the data frame
        vals - tuple
            tuple of properties to be unpacked and inserted into the data frame
        
        """
        
        data = self.get(layer,index,props)
        data = vals
    
    def add(self,layer,df):
        """adds a data frame to a layer in the object
        
        Parameters
        ----------
        layer - str
            layer of the system that dataFrame should be extracted from
        df - pandas dataframe
            dataframe to be appended to the layer
            
        """
        
        # pull appropriate data frame
        data0 = getattr(self,layer)
        
        # concat data
        data1 = pd.concat([data0,df])
        
        # set value
        setattr(self,layer,data1)      