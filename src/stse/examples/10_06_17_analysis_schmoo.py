__doc__ = """This is the file demonstrating how to inspect STSE WalledTissue2D structure which can be used for further processing.
"""

# working with svn version:
stse_svn_revision = 54

from openalea.stse.gui.compartment_editor import start_gui
from openalea.stse.structures.algo.walled_tissue import avg_cell_property
from openalea.stse.structures.algo.walled_tissue import calculate_cell_surface,\
    calculate_wall_length, cell_edge2wv_edge, cell_centers

import sys
import copy
import time
import os.path

if __name__ == '__main__':

    
    window = start_gui()
    #exchange it with your data pointing to schmoo example
    data_dir ="/home/sstoma/src/stse/data/10-04-27-schmoo"
    expression_data_files = [
        "schmoo-0",
    ]
    expression_channels2cell_types  = {
        '0': 'B',
        '1': 'C',
        '2': 'D',
        '3': 'E',
        '4': 'F',       
    }
    # proxy to actions
    a1 = window.actions['file_load_background_image']
    a2 = window.actions['file_load_walled_tissue']
    a3 = window.actions[ "actions_define_cell_types" ]
    a4 = window.actions[ "actions_calculate_average_expression" ]
    a5 = window.actions[ 'file_save_walled_tissue' ]
    
    # loading geometry
    a1.load_image( data_dir+"/"+expression_data_files[ 0 ]+'0'+".png" )
    a2.load( data_dir+"/"+expression_data_files[ 0 ]+"-auto" )
    
    # proxy
    mesh = window._voronoi_wt
    
    # getting average expression in different compartment types
    for i in expression_channels2cell_types.keys():
        print expression_channels2cell_types[ i ], avg_cell_property(wt=mesh, property="custom_cell_property1", property_filter="cell_type", property_filter_value=expression_channels2cell_types[ i ], consider_surface=False)
    
    #getting ratio between cytoplasm surface and nucleus surface
    cs = 0.
    ns = 0.
    
    for i in mesh.cells():
        if mesh.cell_property(i, "cell_type") == "C":
            cs += calculate_cell_surface(mesh, i)
        elif mesh.cell_property(i, "cell_type") == "D":
            ns += calculate_cell_surface(mesh, i)
    print "Ratio between cell/nucleus surface: ", cs/ns
    
    