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
__svn_revision__= "13"


import openalea.plantgl.all as pgl
import openalea.plantgl.ext.all as pd
from openalea.stse.structures.algo.walled_tissue import wv_edge2cell_edge
from openalea.stse.visu.walled_tissue_pgl import visualisation_pgl_2D_varried_membrane_thickness, f_property2scalar, f_cell_marking, f_properties2material


def f_pin( wt ):
    """Function returning function which returns the membrane thickness according
    to PIN cell_edge property.
    
    <Long description of the function functionality.>
    
    :parameters:
        wt : `WalledTissue`
            Tissue containing cell data
    :rtype: function
    :return: Function which returns the membrane thickness according
    to PIN cell_edge property.
    """
    f1 = f_property2scalar(  wt_property_method=wt.directed_cell_edge_property,
                        property = "PIN",
                        default_value = 0.,
                        segment = (0, 1),
                        factor = 1.)
    def f( cell, edge ):
        try:
            ce = wv_edge2cell_edge( wt, edge )
            if ce[ 1 ] == cell: ce=(ce[1],ce[0])
            v = f1( ce )
        except TypeError:
            v = f1( None )
        return v
    return f

# sample visualization using plantGL
def vis( wt, config, props=[], clear=False, save=False ):
    """Displaying of IZ and saving the results.
    """
    for prop in props:
        if clear: pd.SCENES[ pd.CURRENT_SCENE ].clear()
        pd.instant_update_viewer()
        visualisation_pgl_2D_varried_membrane_thickness( wt,
                                            abs_intercellular_space=0.05,
                                            abs_membrane_space=0.25,
                                            stride=20,
                                            f_membrane_thickness = f_pin( wt ),
                                            f_cell_marking = [f_cell_marking( properties=config.cell_regions.keys(), property_true_radius=0.2)], 
                                            f_material = f_properties2material( [prop] ),
                                            reverse = True
                                            )        
        pd.instant_update_viewer()
        if save: pgl.Viewer.frameGL.saveImage( config.file_folder+"/"+"iz"+prop+".png" )
        
    
# viewer config    
def display_config():    
    """Viewer configuration for tissue display.
    """
    # viewer configuration
    pgl.Viewer.camera.setOrthographic()
    pgl.Viewer.display( pd.SCENES[ pd.CURRENT_SCENE ] )
    pgl.Viewer.frameGL.setSize(1024,1024)
    pgl.Viewer.camera.position = pgl.Vector3(0,0,30.)
    pgl.Viewer.light.enabled=False
    pd.instant_update_viewer()



