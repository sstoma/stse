#!/usr/bin/env python
"""<Short description of the module functionality.>

<Long description of the module functionality.>

:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    Humboldt University

"""
# Module documentation variables:
__authors__="""Szymon Stoma    
"""
__contact__="<Your contact>"
__license__="Cecill-C"
__date__="<Timestamp>"
__version__="0.1"
__docformat__= "restructuredtext en"
__svn_revision__= "15"

from openalea.stse.structures.walled_tissue import WalledTissue
from openalea.stse.structures.walled_tissue_const import WalledTissueConst
from openalea.stse.structures.algo.walled_tissue import create
from openalea.stse.io.walled_tissue.dat_representation import read_dat2walled_tissue, read_link_file
from openalea.plantgl.math import Vector3

# we define the set of settings for a tissue
wtc = WalledTissueConst( name = "Tissue01")
# we declare the set of properties for every cell edge
# it corresponds to the protein PIN level
wtc.cell_edges_properties = { "PIN" : 0. }

# we create an empty tissue
wt = WalledTissue( const = wtc )

# please adjust the path to access the files from data directory of stsf
# project
stse_path = "/Users/stymek/src/stse/trunk/data"

# we initialize the tissue using the data read from
# .dat file Specification can be found in the stsf
# documentation
wt = read_dat2walled_tissue( filename = stse_path+"/2cellTest/2cellTest.dat", tissue_properties = wtc)

# setting physiological information

# read links from .link file
# .link file Specification can be found in the stse
# documentation
links = read_link_file( link_fn = stse_path+"/2cellTest/2cellTest.link")

for (i,j) in links:
    try:
        wt.directed_cell_edge_property((int(i), int(j)), "PIN", 1. )
    except Exception:
        print " ! link not added:", i,j

## adjusting visulalization
# adjusting the cell geometry to the display
avg=Vector3()
for i in wt.wvs():
    wt.wv_pos(i, wt.wv_pos(i)*0.1)
    avg+=wt.wv_pos(i)
avg = avg/float(len(wt.wvs()))
for i in wt.wvs():
    wt.wv_pos(i, wt.wv_pos(i)-avg)
        
## sample visualization using plantGL
from openalea.stse.visu.walled_tissue_pgl import visualisation_pgl_2D_varried_membrane_thickness
visualisation_pgl_2D_varried_membrane_thickness( wt,
                                            abs_intercellular_space=0.05,
                                            abs_membrane_space=0.25
                                            )  


import openalea.plantgl.all as pgl
import openalea.plantgl.ext.all as pd

# viewer configuration
pgl.Viewer.camera.setOrthographic()
pgl.Viewer.display( pd.SCENES[ pd.CURRENT_SCENE ] )
pgl.Viewer.frameGL.setSize(1024,1024)
pgl.Viewer.camera.position = pgl.Vector3(0,0,30.)
pgl.Viewer.light.enabled=False
pd.instant_update_viewer()
