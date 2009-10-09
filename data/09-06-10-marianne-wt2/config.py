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
file_folder = stse_path+"/data/09-06-10-marianne-wt2"
# .dat file name
dat_file = "wt2.dat"
#  .link file name
link_file = "wt2.link"
# link description in properties
link = "PIN"
#tissue description
description="Tissue of wildtype 01"

# cell regions
CZ=[54,42,43,89,90,82,44,45,143,253,76,187]
P0=[545,546,566]
P1=[430,428,166,444,688] #455,
P2=[553,476,429,486,734,742,621,575,623,604]
P3=[819,824,836,851,842,830,818,848,993,1043,1044]
P4=[408,413,743,407,427,418,473,485,618,488,474,475,750,759,761,763,515,489,514,527,516,774,777,787] #766,
P5=[1182,1179,1185,1163,1128,1130,1183,1153,1131,1162,1108,1109,1195,1114,1123,1115,1073,1074,1110,1120,1116,1121,1122,1088,1089,1136,1150,1164,1146,1142,1176,1161]
P6=[958,840,953,976,977,949,961,901,935,1000,899,875,871,886,887,925,924,932,804,762,776,773,736,817,984,775,964,933,926,923,936,832,946,922,943,967,979,815,816]

cell_regions = {"CZ": 0, "P0": 0, "P1": 0,"P2": 0,"P3": 0,"P4": 0,"P5": 0,"P6": 0 }
cell_iz =  { "CZ_IZ":0,"P0_IZ": 0, "P1_IZ": 0, "P2_IZ": 0, "P3_IZ": 0, "P4_IZ": 0, "P5_IZ": 0, "P6_IZ": 0}
regions2cells = {"CZ": CZ, "P0": P0, "P1": P1, "P2": P2, "P3": P3, "P4": P4, "P5": P5, "P6": P6}


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
