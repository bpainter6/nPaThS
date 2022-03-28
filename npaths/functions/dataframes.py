# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 18:18:15 2022

@author: 17066
"""

PROPS = {"multiChannel":["presIn","pres","presOut","tempIn","temp","tempOut",
                         "mDot"],
         "channel":["hyD","presIn","pres","presOut","tempIn","temp","tempOut","mDot",
                    "dPtot","dPaccl","dPgrav","dPfric","dPtotal"],
         "axial":["q","dz","presIn","pres","presOut","tempIn","temp","tempOut","mDot",
                  "dPtot","dPaccl","dPgrav","dPfric","dPtotal","dz"],
         "rod":[],
         "radial":["cond","tempIn","temp","tempOut","rIn","rOut","dr"]
         }

INDEXES = {"multiChannel":[],
           "channel":["channel"],
           "axial":["channel","axial"],
           "rod":["channel","axial","rod"],
           "radial":["channel","axial","rod","radial"]
           }

import pandas as pd
import copy

def preallocateDF(layer,layerIds,props=None,):
    """Returns an empty, preallocated data frame for a certain layer
    
    parameters
    ----------
    layer - str
        layer that the data frame is to be generated for
    layerIds - dict
        key is the layer, value is a list of Ids within the layer
    
    """
    
    df = pd.DataFrame()
    
    for ndx0,(layer,Ids) in enumerate(layerIds.items()):
        if ndx0 == 0:
            # first layer must be established in order to assign values
            df[layer] = Ids
        else:
            # remaining layers are appended
            tmpDf = copy.deepcopy(df)
            for ndx1,Id in enumerate(Ids):
                tmpDf[layer] = Id
                if ndx1 == 0:
                    out = copy.deepcopy(tmpDf)
                else:
                    out = pd.concat([out,tmpDf])
            df = out
    
    # use default PROPS if not specified
    if isinstance(props,type(None)):
        props = PROPS
    
    # assign all nonindexes a value of 0
    for prop in props[layer]:
        df[prop] = 0
    
    # convert and return as a multiindex dataframe
    return df.set_index(INDEXES[layer]).sort_index()