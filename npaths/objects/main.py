# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 21:12:51 2022

@author: 17066
"""

import pandas as pd
import numpy as np
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
    
    def __init__(self,fuA,dz):
        """Initializes the MultiChannel object by filling all data specificed
        in the dictionaries
        
        parameters
        ----------
        fuA - 1D array of float
            fuel cross sectional area in each channel
        dz - 1D array of float
            axial layer thickness at each layer
        
        """
        
        nChannel = len(fuA)
        nAxial   = len(dz)
        
        layerIds = {}
        layerIds['channel'] = list(range(nChannel))
        layerIds['axial']   = list(range(nAxial))
        
        # preallocate layer attributes
        layers = ['multiChannel','channel','axial']
        for layer in layers:
            frame = dfs.preallocateDF(layer,layerIds)
            setattr(self,layer,frame)
        
        # set fuA values
        self.update('channel',(slice(None)),["fuA"],(fuA))
        
        # set dz values
        for channelId in layerIds['channel']:
            self.update('axial',(channelId,slice(None)),["dz"],(dz))
        
        self.layerIds = layerIds 
        self.nChannel = nChannel
        self.nAxial   = nAxial
    
    def solveFlow(self,mDot,pIn,tIn):
        """Fully solves flow data. Using specified parameters
        
        parameters
        ----------
        mDot - float
            float describing the 
        Pin - float
            inlet pressure to the multi channel system
        Tin - float
            inlet temperature to the multi channel system
            
        """
        
        layerIds = self.layerIds
        
        self.multiChannel['mDot'] = mDot
        self.multiChannel['pIn'] = pIn
        self.multiChannel['tIn'] = tIn
        
        # assign boundary conditions to each channel
        for channelId in layerIds['channel']:
            self.update('channel',(channelId),['pIn','tIn'],(pIn,tIn))
        
        # solve coolant properties at each axial layer
        self._axialSolve(mDot,pIn)
        
        # solve rod properties at each radial layer
        # self._radialSolve()
    
    def _axialSolve(self,mDotCore,pIn):
        """Iteratively solves coolant properties. Converges when pressure 
        drops are uniform over each channel
        
        parameters
        ----------
        mDotCore - float
            core mass flow rate
        pIn - float
            core inlet pressure
        
        """
        
        nChannel = self.nChannel
        
        # Initialize mDot and pOut histories with boundary condition
        mDots = np.array([0]*nChannel)
        pOuts = np.array([pIn]*nChannel)
        
        # initial guess - divide core flow equally between channels
        mDot = np.array([mDotCore/nChannel]*nChannel)
        
        while True:
            # calculate outlet pressures from intial guess
            pOut = self._stepSolve(mDot)
            
            # check break condition
            if converged(pOut-pIn):
                break
            
            # append mDot and pOut to histories
            pOuts = np.vstack([pOuts,pOut])
            mDots = np.vstack([mDots,mDot])
            
            # Calculate next mDot guess
            pOut0 = pOuts[-2,:]
            pOut1 = pOuts[-1,:]
            mDot0 = mDots[-2,:]
            mDot1 = mDots[-1,:]
            R     = (mDot1-mDot0)/(pOut1-pOut0)
            
            pOutg = np.sum(pOut1*R)/np.sum(R)
            mDot = mDot1 + (pOutg-pOut1)*R
    
    def _stepSolve(self,mDots):
        """Fully solves the system for the specified input mass flow rates.
        A single solution step in solving the full core coolant props
        
        parameters
        ----------
        mDots - array
            array of mass flow rates describing the flow rates in each channel
        
        """
        
        layerIds = self.layerIds
        
        # populate mass flow rates for each channel
        for channelId in layerIds['channel']:
            self.update('channel',(channelId),['mDot'],mDots[channelId])
        
        # solve axial bulk coolant properties
        for channelId in layerIds['channel']:
            # get the inlet conditions and flow geometry for the channel
            mDot,tIn,pIn,hyD,flA = self.get('channel',(channelId),
                                           ['mDot','tIn','pIn','hyD','flA'])
            
            # solve and save coolant properties in each axial layer
            for axialId in layerIds['axial']:
                # get axial variant data
                q,dz,grA = self.get('axial',(channelId,axialId),
                                    ['q','dz','grA'])
                
                # calculate form loss coefficient
                if axialId == 0:
                    # entrance losses
                    form = 1
                elif axialId == self.nAxial-1:
                    # exit losses
                    form = 0.5
                else:
                    form = 0
                
                # calculate flow conditions at the layer
                out = axl.axialHelper(pIn,tIn,mDot,q,hyD,flA,dz,grA,form)
                
                # save coolant properties for the axial layer
                self.update('axial',(channelId,axialId),
                            ["pIn","p","pOut","tIn","t","tOut",
                            "dPtot","dPaccl","dPgrav","dPfric","dPform",
                            "cp","rho","mu","vel"],
                            out)
                
                # update entrance conditions for the next layer
                tIn,pIn = self.get('axial',(channelId,axialId),['tOut','pOut'])
            
            # set the channel outlet pressure
            self.update('channel',(channelId),['pOut'],(pIn))
        
        return self.get('channel',(slice(None)),['pOut'],mode='array')
    
    def solveTemps(self,rod):
        """Solves rod properties using the obtained coolant properties"""
        
        layerIds = self.layerIds
        layerIds['radial'] = rod.radialIds
        layerIds['channel'] = rod.channelIds
        
        # preallocate layer attributes
        frame = dfs.preallocateDF('radial',layerIds)
        setattr(self,rod.Id,frame)
        
        # fuel radius
        rF = rod.rFuel
        
        # update rod data adn solve
        for channelId in layerIds['channel']:
            # channel properties
            fuA = self.get('channel',(channelId),['fuA'],mode='float')
            
            for axialId in layerIds['axial']:
                # boundary conditions
                q,tOut = self.get('axial',(channelId,axialId),['q','t'],
                                    mode='float')
                
                # get cross sectional heat generation
                Q = q/fuA
                
                # define radial data
                props = ['rIn','rOut','comp']
                vals = rod.rIn,rod.rOut,rod.comp
                self.update(rod.Id,(channelId,axialId,slice(None)),props,vals)
                
                # calc radial conditions in each radial layer
                for radialId in layerIds['radial']:
                    # radial conditions
                    rIn,rOut = self.get(rod.Id,(channelId,axialId,radialId),
                                           ['rIn','rOut'],mode='float')
                    comp = self.get(rod.Id,(channelId,axialId,radialId),
                                           ['comp'],mode='str')
                    
                    out = rad.radialHelper(Q,rIn,rOut,rF,comp,tOut)
                    
                    # save radial properties for the radial layer
                    self.update(rod.Id,(channelId,axialId,radialId),
                                ["tIn","t","tOut","k"],out)
                    
                    # update entrance conditions for the next layer
                    tOut = self.get(rod.Id,(channelId,axialId,radialId),
                                    ['tIn'],mode='float')
                    
    def get(self,layer,index,props,mode='df'):
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
        
        data = getattr(self,layer).loc[index,props]
        
        if mode == 'df':
            return data
        
        if mode == 'float':
            # 1 prop, 1 index only
            outs = []
            for prop in props:
                outs.append(float(data[prop]))
        
        if mode == 'array':
            # 1 prop only
            outs = []
            for prop in props:
                outs.append(np.array(data[prop]))
        
        if mode == 'str':
            # 1 prop 1 index only
            outs = []
            for prop in props:
                outs.append(str(data[prop]))
        
        if len(props) == 1:
            return outs[0]
        else:
            return tuple(outs)
    
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
        
        data = getattr(self,layer)
        
        # allow array inputs
        if isinstance(vals,tuple) and isinstance(vals[0],type(np.array([]))):
            for ndx,prop in enumerate(props):
                val = vals[ndx]
                
                # flatten 2D input
                if val.ndim > 1:
                    val = val.flatten()
                
                data.loc[index,prop] = val
        
        else:
            data.loc[index,props] = vals
        
        setattr(self,layer,data)

def converged(vec):
    """check whether a vector of values has converged ot an average. Return true
    if the maximum error is less than 1%
    """
    
    mu      = np.mean(vec)
    err     = abs(abs(mu-vec)/mu)
    testErr = np.max(err)
    return testErr < 0.001