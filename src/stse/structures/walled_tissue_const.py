#!/usr/bin/env python

"""Most general const class required for WalledTissue initialization.

It defines default properties of different compartment composites.

:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    INRIA

"""

# Module documentation variables:
__authors__="""Szymon Stoma    
"""
__contact__=""
__license__="Cecill-C"
__date__="03/2009"
__version__="0.1"
__docformat__= "restructuredtext en"
__revision__="$Id$"

class WalledTissueConst:
    """Used to store tissue properties.
    """
    def __init__( self,
                 name="Tissue",
                 cell_properties={},
                 tissue_properties={},
                 cell_edge_properties={},
                 wv_properties={},
                 wv_edge_properties={}
                 ):
        self.name = str( name )
        self.cell_properties = cell_properties
        self.tissue_properties = tissue_properties
        self.cell_edge_properties = cell_edge_properties
        self.wv_properties = wv_properties
        self.wv_edge_properties = wv_edge_properties