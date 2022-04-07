# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 18:18:15 2022

@author: 17066
"""

PROPS = {"multiChannel":["mDot",
                         "pIn","p","pOut","tIn","t","tOut"],
         
         "channel":["hyD","flA","mDot",
                    "pIn","p","pOut","tIn","t","tOut",
                    "dPtot","dPaccl","dPgrav","dPfric",
                    "fuA"],
         
         "axial":["q","dz",
                  "pIn","p","pOut","tIn","t","tOut",
                  "grA",
                  "dPtot","dPaccl","dPgrav","dPfric","dPform",
                  "cp","rho","mu","vel","G"],
         
         "radial":["rIn","rOut","comp","tIn","t","tOut","k"]
         }

INDEXES = {"multiChannel":[],
           "channel":["channel"],
           "axial":["channel","axial"],
           "radial":["channel","axial","radial"]
           }

import pandas as pd
import copy

def preallocateDF(layer,layerIds):
    """Returns an empty, preallocated data frame for a certain layer
    
    parameters
    ----------
    layer - str
        layer that the data frame is to be generated for
    layerIds - dict
        key is the layer, value is a list of Ids within the layer
    
    """
    
    df = pd.DataFrame()
    
    for ndx0,subLayer in enumerate(INDEXES[layer]):
        if ndx0 == 0:
            # first layer must be established in order to assign values
            df[subLayer] = layerIds[subLayer]
        else:
            # remaining layers are appended
            tmpDf = copy.deepcopy(df)
            Ids = layerIds[subLayer]
            for ndx1,Id in enumerate(Ids):
                tmpDf[subLayer] = Id
                if ndx1 == 0:
                    out = copy.deepcopy(tmpDf)
                else:
                    out = pd.concat([out,tmpDf])
            df = out
    
    # extract properties
    props = PROPS
    
    # assign all nonindexes a value of 0
    for ndx,prop in enumerate(props[layer]):
        df[prop] = 0
        if layer == 'multiChannel' and ndx == 0:
            # initialize row for the multiChannel dataFrame
            df.loc[0] = [0]
    
    # convert and return as a multiindex dataframe
    if layer == 'multiChannel':
        return df
    else:
        return df.set_index(INDEXES[layer]).sort_index()