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
file_folder = "/Users/stymek/src/stse/trunk/data/09-05-26-marianne-quad2"
# .dat file name
dat_file = "quad2.dat"
#  .link file name
link_file = "quad2.link"
# link description in properties
link = "PIN"
#tissue description
description="Tissue of quadriple mutant AUX/LAX 02"

CZ = [215,222,82,198,213,309,94,99,189,192,94]
P0 = [446,466]
P1 = [714,597,601,618,715,718]
P2 = [790,792,809,800,808,795,807,277,270,272,282] # marianne says it is eventually
P3 = [1124,1122,1189,1128,983,1055,1073,1078,1136,1096,1092,1094,1086,1089,1083,1116,1113,1110,1054,1063,1121,1111,1079,1115]
P3_removed = [1032, 1020]

cell_regions = {"CZ": 0, "P0": 0, "P1": 0,"P2": 0,"P3": 0 }
cell_iz =  { "CZ_IZ":0,"P0_IZ": 0, "P1_IZ": 0, "P2_IZ": 0, "P3_IZ": 0}
regions2cells = {"CZ": CZ, "P0": P0, "P1": P1, "P2": P2, "P3": P3}

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
