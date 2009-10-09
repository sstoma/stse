#!/usr/bin/env python
"""Defines configuration for quad2 tissue.

<Long description of the module functionality.>

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
__contact__="<Your contact>"
__license__="Cecill-C"
__date__="Tue Jun 16 12:44:32 CEST 2009"
__version__="0.1"
__docformat__= "restructuredtext en"

import math
import os

# making sure that the configuration is new
import openalea.stse.io.walled_tissue.dat_config
m = reload( openalea.stse.io.walled_tissue.dat_config )
locals().update(m.__dict__)


format_version = 1.0
# scale use to convert the units 
scale_factor = 0.1
# rotate the points around 0,0 and z-axis
rotation = math.pi/2.
# translate the points to make 0,0 geometric center
translation = True
#cells to remove
remove_cell_list = []
# path to data
stse_path = os.getenv("STSE_DIR")
file_folder = stse_path+"/data/09-06-10-marianne-quad1"
# .dat file name
dat_file = "quad1.dat"
#  .link file name
link_file = "quad1.link"
# link description in properties
link = "PIN"
#tissue description
description="Tissue of quadriple mutant AUX/LAX 01"

CZ=[39,1012,1043,1038,858,845,844,801,802,864,857]
P0=[946,948,949,954]
P1=[986,1034,926,1031]

cell_regions = {"CZ": 0, "P0": 0, "P1": 0 }
cell_iz =  { "CZ_IZ":0,"P0_IZ": 0, "P1_IZ": 0}
regions2cells = {"CZ": CZ, "P0": P0, "P1": P1}

# properties to set with tissue
from openalea.stse.structures.walled_tissue_const import WalledTissueConst
const=WalledTissueConst()
const.cell_properties = {}
const.cell_properties.update( cell_regions )
const.cell_properties.update( cell_iz )
const.tissue_properties ={}
const.cell_edge_properties={}
const.wv_properties={}
const.wv_edge_properties={}

#for each property the properties dictionary will be searched. if no value is
#found, the properties will be set as default if the dictionary contains a key
#with property name it can contain a dictionary inside with
#{id: modifiedProperty}
cell_properties = {}
cell_edge_properties={}
wv_properties={}
wv_edge_properties={}

def set_zones( wt, **keys ):
    """sets zones for meristem after tissue initalization
    
    :parameters:
        wt : `WalledTissue`
            Tissue on which zones will be set.
    """
    for i in regions2cells:
        for j in regions2cells[ i ]:
            wt.cell_property(j, i, 1 )

# sets in
def set_influence_zones( wt, **keys):
    def f( wt, directed_cell_edge ):
        return wt.directed_cell_edge_property( directed_cell_edge, "PIN")
    
    from openalea.stse.structures.algo.walled_tissue_influence_zones import set_property_on_tissue_component
    for i in regions2cells:
        #print zones[ i ]
        for j in regions2cells[ i ]:
            set_property_on_tissue_component( wt=wt,
                                 cell= j,
                                 f_component=f,
                                 tol=0.1,
                                 property=i+"_IZ",
                                 property_value=1.,
                                 with_neighbors=False,
                                 fill_gaps=False,
                                 additional_vertices=[])

post_procedures = [set_zones, set_influence_zones]