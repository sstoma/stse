__doc__ = """This is the file demonstrating how to inspect STSE WalledTissue2D structure which can be used for further processing.
"""

# working with svn version:
stse_svn_revision = 54

from openalea.stse.gui.compartment_viewer import start_gui
from openalea.stse.structures.algo.walled_tissue import avg_cell_property
from openalea.stse.structures.algo.walled_tissue import calculate_cell_surface,\
    calculate_wall_length, cell_edge2wv_edge, cell_centers, cell_center

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
    a1.load_image( data_dir+"/"+expression_data_files[ 0 ]+'0'+".png" )
    a2.load( data_dir+"/"+expression_data_files[ 0 ]+"-auto" )
    
    # proxy
    mesh = window._voronoi_wt
    
    # getting average expression in different compartment types
    print "# Example 1 (expression signal in different compartments):"
    for i in expression_channels2cell_types.keys():
        print '  Average expression in', cell_type2biological_name[ expression_channels2cell_types[ i ] ], avg_cell_property(wt=mesh, property="custom_cell_property1", property_filter="cell_type", property_filter_value=expression_channels2cell_types[ i ], consider_surface=False)
    
    # calculating the ratio between nucleus/cytoplsm expression
    print '  Ratio: expression in nucleus/cytoplasm', avg_cell_property(wt=mesh, property="custom_cell_property1", property_filter="cell_type", property_filter_value="C", consider_surface=False) /  avg_cell_property(wt=mesh, property="custom_cell_property1", property_filter="cell_type", property_filter_value="B", consider_surface=False)
    
    # making a profile plot    
    x = []
    y = []
    for i in mesh.cells():
        if mesh.cell_property(i, "cell_type") == "B":
            x.append(cell_center(mesh,i)[0])
            y.append(mesh.cell_property(i, "custom_cell_property1"))
    scatter(x,y,c='r',hold=True)
    x2 = []
    y2= []
    z2 = []
    for i in mesh.cells():
        if mesh.cell_property(i, "cell_type") == "C":
            x2.append(cell_center(mesh,i)[0])
            y2.append(mesh.cell_property(i, "custom_cell_property1"))
            z2.append(cell_center(mesh,i)[1])
            
    scatter(x2,y2,c='b',hold=True)
    legend( ('Expression in cyt.', 'Expression in nuc.') )
    show()
    figure()
    scatter(x2,z2,hold=False)
    show()
    print "# Profile through a cell.. DONE"
    
    print "# Example 2 (geometrical properties of the mesh - in pixels):"
    
    # example cell surface
    print "  Example cell surface:", calculate_cell_surface(mesh, mesh.cells()[0] )
    
    #getting ratio between cytoplasm surface and nucleus surface
    cs = 0.
    ns = 0.   
    for i in mesh.cells():
        if mesh.cell_property(i, "cell_type") == "B":
            cs += calculate_cell_surface(mesh, i)
        elif mesh.cell_property(i, "cell_type") == "C":
            ns += calculate_cell_surface(mesh, i)
    print "  Ratio between cell/nucleus surface: ", cs/ns
    
    # calculaing the nucleus membrane length in 2D projection  
    ml = 0.
    for i in mesh.cells():
        if mesh.cell_property(i, "cell_type") == "C":
            for j in  mesh.cell_neighbors( i ):
                if mesh.cell_property(j, "cell_type") == "E":
                    ml += calculate_wall_length( mesh, (i, j))
    print "  Nucleus membrane length in 2D projection:", ml

    # calculaing the celll membrane length in 2D projection  
    cml = 0.
    for i in mesh.cells():
        if mesh.cell_property(i, "cell_type") == "B":
            for j in  mesh.cell_neighbors( i ):
                if mesh.cell_property(j, "cell_type") == "D":
                    cml += calculate_wall_length( mesh, (i, j))
    print "  Cell membrane length in 2D projection:", cml

    print "# Example 3 (topological properties of the mesh):"
    #getting ratio between cytoplasm surface and nucleus surface
    nc = 0
    nbr_nei = 0   
    for i in mesh.cells():
        if mesh.cell_property(i, "cell_type") == "C":
            nbr_nei += len( mesh.cell_neighbors( i ) )
            nc += 1
    print "  Average number of each compartment neighbours in the nucleus:", nbr_nei / float(nc)
    
    print "# Example 4 (manipulating tissue):"
    # changing cell_types
    for i in mesh.cells():
        if mesh.cell_property(i, "cell_type") == "C":
            mesh.cell_property(i, "cell_type", "E")
    print "  Changing all nucleus compartments to nucleus membrane compartments.. DONE"
    
    # Removing cells
    br = len(mesh.cells())
    for i in mesh.cells():
        if mesh.cell_property(i, "cell_type") == "E":
            mesh.remove_cell(i)
    print "  Removing nucleus and (old) nucleus membrane compartment.. DONE"
    ar = len(mesh.cells())
    print "  Removed ", br-ar, "compartments. Current number of compartiments: ", ar 
    window.update_vtk_from_voronoi()
    window._cell_scalars_active = True
    #window.update_colormap( render_scene = True, voronoi_changed=True)
