#!/usr/bin/env python
"""This module specifies helpers for reading .dat and .link files.

<Long description of the module functionality.>

:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    HU

"""
# Module documentation variables:
__authors__="""Szymon Stoma
"""
__license__="Cecill-C"
__date__="Mon Jun 15 15:47:22 CEST 2009"
__version__="0.1"
__docformat__= "restructuredtext en"


format_version = 1.0
# scale use to convert the units 
scale_factor = 1.
# rotate the points around 0,0 and z-axis
rotation = 0.
# translate the points to make 0,0 geometric center
translation = False
#cells to remove
remove_cell_list = []
# path to data
file_folder = ""
# .dat file name
dat_file = ".dat"
#  .link file name
link_file = ".link"
# link description in properties
link = "PIN"
#tissue description
description=""

# properties to set with tissue
from openalea.stse.structures.walled_tissue_const import WalledTissueConst
const = WalledTissueConst()
const.cell_properties ={}
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

# procedures run after tissue initialization, may do various editing stuff
post_procedures = []
