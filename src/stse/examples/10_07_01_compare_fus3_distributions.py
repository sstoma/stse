__doc__ = """This is the file compares the distribution of .
"""

# working with svn version:
__svn_revision__= "211"
__run_command__ = "ipython -wthread (when shell starts use 'run file_name')"

from openalea.stse.gui.compartment_viewer import start_gui
from openalea.stse.structures.algo.walled_tissue import avg_cell_property
from openalea.stse.structures.algo.walled_tissue import calculate_cell_surface,\
    calculate_wall_length, cell_edge2wv_edge, cell_centers, cell_center
from openalea.stse.io.walled_tissue.vtk_representation import  \
    copy_cell_properties_from_wt_to_voronoi
from openalea.stse.io.walled_tissue.native_representation import \
    write_walled_tissue, read_walled_tissue

import sys
import copy
import time
import os.path
import os
from matplotlib.pyplot import scatter, legend, show, figure


if __name__ == '__main__':

    
    window = start_gui()
    #exchange it with your data pointing to schmoo example
    # please adjust the path to access the files from data directory of stsf
    # project
    stse_path = os.getenv("STSE_DIR")
    data_dir =stse_path+"/data/10-04-27-schmoo"
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
    cell_type2biological_name ={
        'A': 'outside',
        'B': 'cytoplasm',
        'C': 'nucleus',
        'D': 'cell_membrane',
        'E': 'nuceus_membrane',
        'F': 'schmoo_tip',
    }
    
    # proxy to actions
    a1 = window.actions['file_load_background_image']
    a2 = window.actions['file_load_walled_tissue']
    #a3 = window.actions[ "actions_define_cell_types" ]
    #a4 = window.actions[ "actions_calculate_average_expression" ]
    a5 = window.actions[ 'file_save_walled_tissue' ]
    
    # loading geometry
    a1._load_image( data_dir+"/"+expression_data_files[ 0 ]+'0'+".png" )
    a2._load( data_dir+"/"+expression_data_files[ 0 ]+"-auto" )
    
    simulated_wt = read_walled_tissue( file_name= data_dir+"/"+expression_data_files[ 0 ]+"-diffusion,gamma50"  )
    
    # proxy
    mesh = window._voronoi_wt
    
    # normalizing the image data/simulated data
    for tissue in [mesh, simulated_wt]:
        max = 0.
        for i in tissue.cells():
            if max < tissue.cell_property(i, "custom_cell_property1"):
                max = tissue.cell_property(i, "custom_cell_property1")
        print " Max expression: ", max
        for i in tissue.cells():
            tissue.cell_property(i, "custom_cell_property1", tissue.cell_property(i, "custom_cell_property1") / max)
        
    # calculating the difference
    for i in mesh.cells():
        d = mesh.cell_property(i, "custom_cell_property1") - simulated_wt.cell_property(i, "custom_cell_property1")
        mesh.cell_property(i, "custom_cell_property1", abs(d))
    
    #the difference is only important in simulated areas
    for i in mesh.cells():
        if mesh.cell_property(i, "cell_type") == "D":
            mesh.cell_property(i, "custom_cell_property1", 0.)
     
    # visualizing the difference    
    copy_cell_properties_from_wt_to_voronoi( mesh, window._voronoi_center_list, ["custom_cell_property1"] )
    window._cell_scalars_active_name = "custom_cell_property1"
    window._cell_scalars_dynamic=False
    window._cell_scalars_active = True    
    window._cell_scalars_range[1]=1.
    window.update_colormap()