"""Rutines for reading QHULL generated files containing voronoi regions
and saving them as WalledTissue2d.



:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    Humboldt Univesity

:authors:
    Szymon Stoma
"""

from openalea.stse.tools.convex_hull import hulls
from openalea.stse.structures.walled_tissue import WalledTissue
from openalea.stse.structures.walled_tissue_const import WalledTissueConst
from openalea.stse.structures.algo.walled_tissue import create
from openalea.stse.structures.algo.walled_tissue_topology import find_degenerated_cells, \
    kill_degenerated_cells
from openalea.plantgl.math import Vector3
import math
from pylab import inf

def read_qhull2walled_tissue( voronoi_centers, voronoi_edges, tissue_properties=None, remove_infinite_cells=False, constraints=None ):
    """Allows to create the WalledTissue based on the information
    from two files: first one containg definitions of voronoi centers
    in the rbox format, second one containing the computed voronoi
    vertices (by qvoronoi).
    
    <Long description of the function functionality.>
    
    :parameters:
        arg1 : `T`
            <Description of `arg1` meaning>
    :rtype: `T`
    :return: <Description of ``return_object`` meaning>
    :raise Exception: <Description of situation raising `Exception`>
    """
    try:
        #file = open(voronoi_centers, 'r')
        file = voronoi_centers
        
        tag_line = file.readline()
        
        nbr_points = int(file.readline())
        
        cell2pos = {}
        for i in range(nbr_points):
            l = file.readline()
            ls = l.split()
            # formating pos
            cell2pos[ i ] = (float(ls[0]), float(ls[1]))
            

    finally:
        file.close()  
    #print cell2pos
    
    #reading centres
    try:
        #file = open(voronoi_edges, 'r')
        file = voronoi_edges
        dimension = file.readline()
        
        nbrs = file.readline()
        nbrss = nbrs.split()
        nbr_wvs = int(nbrss[0])
        nbr_cells = int(nbrss[1])
        
        wv2pos = {}
        cell2wv_list = {}
        inf_cells = []
        for i in range(nbr_wvs):
            l = file.readline()
            ls = l.split()
            # formating pos
            wv2pos[ i ] = Vector3(float(ls[0]), float(ls[1]), 0.)
        for i in range(nbr_cells):
            l = file.readline()
            l = l.split()
            l = l[1:]
            l = map(int, l)
            # removing infinite cells
            if 0 in l:
                l.remove(0)
                inf_cells.append(i)
            cell2wv_list[ i ] = l 
            

    finally:
        file.close()  
    #print cell2wv_list, wv2pos
    
    ## TISSUE CREATION
    # we define the set of settings for a tissue
    if not tissue_properties:
        tissue_properties = WalledTissueConst( name = "Tissue01" )

    # we create a tissue
    wt = WalledTissue( const = tissue_properties )    
    wt.init_tissue_property( "outside_voronoi_centers", [])
    wt.init_tissue_property( "tissue_format", "QHULL 1.0" )
    wt.init_cell_property( "was_inf", False )
    wt.init_cell_property( "voronoi_center", (0.,0.,0.) )
    create(wt, wv2pos=wv2pos, cell2wv_list=cell2wv_list)

    
    for i in inf_cells:
        wt.cell_property( i, "was_inf", True )
        if remove_infinite_cells:
            wt.remove_cell( i )

    if constraints:
        c = constraints
        wv_outside = []
        cells_outside = []
        for i in wt.wvs():
            p = wt.wv_pos( i )
            # if the point wall point is outside the border rectangle
            # defined by  constraint we mark this tissue
            if ( p[0] < c[0][0] or p[1] < c[0][1] ) or ( p[0] > c[1][0] or p[1] > c[1][1] ):
                wv_outside.append( i )
        for i in wv_outside:
            cells_outside.extend( wt.wv2cells(i) )
        # killing dupes
        cells_outside = dict(map(lambda a: (a,1), cells_outside)).keys()
        # removing outside cells
        for i in cells_outside:
            wt.remove_cell( i )
    
    kill_degenerated_cells( wt )
    return wt

