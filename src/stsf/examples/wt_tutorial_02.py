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
stsf_path = "/Users/stymek/src/stse/trunk/data"

# we initialize the tissue using the data read from
# .dat file Specification can be found in the stsf
# documentation
wt = read_dat2walled_tissue( filename = stsf_path+"/2cellTest/2cellTest.dat", tissue_properties = wtc)

# setting physiological information

# read links from .link file
# .link file Specification can be found in the stsf
# documentation
links = read_link_file( link_fn = stsf_path+"/2cellTest/2cellTest.link")

for (i,j) in links:
    try:
        wt.cell_edge_property((int(i), int(j)), "PIN", (i,j) )
    except Exception:
        print " ! link not added:", i,j

#for i in wt.wvs():
#    wt.wv_pos( i, wt.wv_pos( i )/ 100. )

### sample visualization using pylab
#from openalea.stse.visu.walled_tissue_pylab import show_cells_with_wvs
#show_cells_with_wvs(wt, True)

## sample visualization using plantGL
from openalea.stse.visu.walled_tissue_pgl import visualisation_pgl_2D_plain
visualisation_pgl_2D_plain( wt )

## adjusting visulalization
import openalea.plantgl.all as pgl
import openalea.plantgl.ext.all as pd

pgl.Viewer.camera.setOrthographic()
pgl.Viewer.display( pd.SCENES[ pd.CURRENT_SCENE ] )
pgl.Viewer.camera.lookAt( (0., 0., 5.) )
