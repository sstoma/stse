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
import openalea.plantgl.all as pgl
import openalea.plantgl.ext.all as pd
import math

## we define the set of settings for a tissue
#wtc = WalledTissueConst( name = "Tissue01")
## we declare the set of properties for every cell edge
## it corresponds to the protein PIN level
#wtc.cell_edge_properties = { "PIN" : 0. }
##wtc.wvs_edges_properties = { "PIN": 0. }
#
## we create an empty tissue
#wt = WalledTissue( const = wtc )
#
## we initialize the tissue using the data read from
## .dat file Specification can be found in the stsf
## documentation
##wt = read_dat2walled_tissue( filename = "/Users/stymek/src/stse/trunk/data/09-05-26-marianne-quad2/quad2.dat", tissue_properties = wtc, screen_coordinates = True)
##wt = read_dat2walled_tissue( filename = "/Users/stymek/src/stse/trunk/data/09-06-10-marianne-quad1/quad1.dat", tissue_properties = wtc, screen_coordinates = True)
#wt = read_dat2walled_tissue( filename = "/Users/stymek/src/stse/trunk/data/09-06-10-marianne-wt2/wt2.dat", tissue_properties = wtc, screen_coordinates = True)
#
## setting physiological information
#
## read links from .link file
## .link file Specification can be found in the stsf
## documentation
##links = read_link_file( link_fn = "/Users/stymek/src/stse/trunk/data/09-05-26-marianne-quad2/quad2.link")
##links = read_link_file( link_fn = "/Users/stymek/src/stse/trunk/data/09-06-10-marianne-quad1/quad1.link")
#links = read_link_file( link_fn = "/Users/stymek/src/stse/trunk/data/09-06-10-marianne-wt2/wt2.link")
#
#
#for (i,j) in links:
#    try:
#        wt.directed_cell_edge_property((int(i), int(j)), "PIN", 1. )
#    except Exception:
#        print " ! link not added:", i,j
#
### sample visualization using pylab
#from openalea.stse.visu.walled_tissue_pylab import show_cells
#show_cells(wt, True)
#
### adjusting visulalization
## adjusting geometry to display
#for i in wt.wvs():
#    wt.wv_pos( i, wt.wv_pos( i )/ 10. )
#s = pgl.Vector3()
#for i in wt.wvs():
#    s += wt.wv_pos( i )
#s = s/len( wt.wvs() )
#for i in wt.wvs():
#    wt.wv_pos( i, wt.wv_pos( i ) - s )
#r = pgl.Matrix3().axisRotation((0,0,1),math.pi/2.)
#for i in wt.wvs():
#    wt.wv_pos( i, r*wt.wv_pos( i ))

from openalea.stse.io.walled_tissue.dat_config_processing import read_dat_tissue_directory
wt = read_dat_tissue_directory( "" )

# sample visualization using plantGL
from openalea.stse.visu.walled_tissue_pgl import visualisation_pgl_2D_varried_membrane_thickness, f_property2scalar
visualisation_pgl_2D_varried_membrane_thickness( wt,
                                                abs_intercellular_space=0.05,
                                                abs_membrane_space=0.25,
                                                stride=20,
                                                f_membrane_thickness=f_property2scalar(
                                                    wt_property_method=wt.directed_cell_edge_property,
                                                    property = "PIN",
                                                    default_value = 0.,
                                                    segment = (0, 1),
                                                    factor = 1.
                                                    )
                                                )
# viewer configuration
pgl.Viewer.camera.setOrthographic()
pgl.Viewer.display( pd.SCENES[ pd.CURRENT_SCENE ] )
pgl.Viewer.camera.position = pgl.Vector3(0,0,38.)
pgl.Viewer.light.enabled=False

