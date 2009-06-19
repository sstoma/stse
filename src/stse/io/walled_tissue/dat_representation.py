"""Rutines for reading .DAT files and saving them as WalledTissue2d.



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
from openalea.plantgl.math import Vector3
import math
from pylab import inf
from re import compile

def build_cell_neigbourhood( cell2points, point2cells ):
    """Builds neighbourhood graph based on cell to point mapping. Two cells are
    neighbours if they share more than 1 vertex.
        
    :param cell2points: cell to point mapping
    :type filename: dict of cell_id to wall_vertex_id
    :return: dict of cell to cell neighbours
    """
    # create empty neighborhood
    n = {}
    neigh = {}
    for i in cell2points:
        for j in cell2points:
            n[ (i,j) ] = 0
        neigh[ i ] = []
        
    for i in cell2points:
        for j in cell2points[ i ]:
            for k in point2cells[ j ]: 
                if not k == i:
                    if i < k: n[ (i, k) ] += 1
                    else: n[ (k, i) ] += 1
    
    for (i,j) in n:
        if n[ (i,j) ] > 2:
            neigh[ i ].append(j)
            neigh[ j ].append(i)
    
    for i in neigh:
        list_without_dups = dict(map(lambda a: (a,1), neigh[ i ])).keys()
        #list_without_dups.remove( i )
        neigh[ i ] =list_without_dups
        
    return neigh
            
def read_dat2walled_tissue(filename, tissue_properties=None, screen_coordinates=False):
    """Reads .dat file and creates walled_tissue datastructure based on this
    file.
        
    :param filename: name of the file to read
    :param tissue_properties: tissue properties object use to initialize tissue.
    :param screen_coordinates: True if Y coord should be read with - sign.
    Usefull when using merrydig software. By default False.
    :type filename: string
    :return: tissue
    """
    try:
        file = open(filename, 'r')
        
        image_file = file.readline()
        format = file.readline()
        if format.find("DAT1.0") == -1:
            raise IOError("File format not supported. Check for compatibility.")
        
        nbr_points = int(file.readline())
        
        point2position = {}
        position2point = {}
        point2cells = {}
        cell2points = {}
        for i in range(nbr_points):
            l = file.readline()
            ls = l.split()
            point_id = int( ls[0] )
            # formating pos
            pos = ls[1]
            pos = pos[1:-1]
            pos = pos.split(',')
            if screen_coordinates:
                point2position[ point_id ] = ( float( pos[0] ), -float( pos[1] ) )
            else:
                point2position[ point_id ] = ( float( pos[0] ), float( pos[1] ) )
            position2point[ point2position[ point_id ] ] = point_id
            
            cells = []
            for j in range( int ( ls[ 2 ] ) ):
                cells.append( int( ls[ 3+j] ) )
            point2cells[ point_id ] = list( cells )
            
            for k in cells:
                if cell2points.has_key( k ):
                    t = cell2points[ k ]
                    t.append( point_id )
                    cell2points[ k ] = t
                else:
                    cell2points[ k ] = [ point_id ]
    finally:
        file.close()            
    
    # cleaning degenerated cells
    _cells_to_remove = {}
    for i in cell2points:
        if len( cell2points[ i ] ) < 3:
            _cells_to_remove[ i ] = cell2points[ i ]
    for i in _cells_to_remove:
        print " ! removing <3 point cell: ", i
        del cell2points[ i ]
    for i in _cells_to_remove:
        for j in _cells_to_remove[ i ]:
            l = point2cells[ j ]
            l.remove( i )
            point2cells[ j ] = l
    
    ## TISSUE CREATION
    # we define the set of settings for a tissue
    if not tissue_properties:
        tissue_properties = WalledTissueConst( name = "Tissue01" )
    tissue_properties.tissue_properties[ "tissue_image_file" ] = image_file
    tissue_properties.tissue_properties[ "tissue_file" ] = filename
    tissue_properties.tissue_properties[ "tissue_format" ] = format
    # we create a tissue
    wt = WalledTissue( const = tissue_properties )
    
    # the problem is that not all cells are convex, therefore hulls will drop
    # some vertices from cells. To correct this error we must repair the cells
    # for which the number of vertices returned by hulls is smaller than the
    # input number.
    # if a vertex was removed from the cell wall it means that it can be still
    # found in the wall of this cell neighbour since it was convex there
    
    # create cell neigh
    cell_neighbourhood = build_cell_neigbourhood( cell2points, point2cells )
    #print cell_neighbourhood
    
    cell2wv_list = {}
    for i in cell2points:
        cell2wv_pos=[]
        for j in cell2points[ i ]:
            cell2wv_pos.append( point2position[ j ])
        cell2wv_pos = hulls(cell2wv_pos)
        wv_list = []
        for j in cell2wv_pos:
            wv_list.append( position2point[ j ] )
        cell2wv_list[ i ] = list(wv_list)
    
    # checking if the hulls skiped a vertex
    for i in cell2points:
        if not len( cell2points[ i ] ) == len( cell2wv_list[ i ] ):
            correct_wv_list_based_on_geometry( i, cell2wv_list, cell2points, cell_neighbourhood, point2cells, point2position)
    
    wv2pos={}
    for i in point2position:
        pos = point2position[i]
        wv2pos[ i ] = Vector3( float( pos[ 0 ] ), float( pos[ 1 ] ), 0. )
    
    
    create(wt, wv2pos=wv2pos, cell2wv_list=cell2wv_list)
    
    for i in wt.cells():
        if not len( wt.cell_neighbors( i ) ) == len( cell_neighbourhood[ i ] ):
            print " ! problem with neighborhood of cell: ", i
        
    return wt

def correct_wv_list_based_on_geometry( cell, cell2wv_list, cell2points, cell_neighbourhood, point2cells, point2position):
    """Corrects the wv_list of cell shortened by hulls based on the information
    from geometry.
        
    """
    print " # correcting non-convex cell: ", cell
    shape = cell2wv_list[ cell ]
    all_vertices = cell2points[ cell ]
    
    #if abs( len(shape) - len( all_vertices )) > 1:
    #    # currently we can only fill in one missing vertex
    #    raise NotImplementedError();
    
    missing_vertices = []
    for i in all_vertices:
        if i not in shape:
            missing_vertices.append( i )
    
    # for every missing vertex v we try to fit it to the current cell shape:
    # exchange a wall (described by two
    # consecutive vertices x1, x2 ) by two walls x1,v v,x2. we choose to fit the
    # vertex in a place where the difference in length is the smallest
    for i in missing_vertices:
        d = {}
        for j in range( len( shape ) ):
            a = shape[j]
            b = shape[ (j+1) % len(shape) ]
            ap = point2position[ a ]
            bp = point2position[ b ]
            d[ ( a, b ) ] = math.sqrt( math.pow(ap[0] - point2position[ i ][ 0 ],2) + math.pow(ap[1] - point2position[ i ][ 1 ], 2) )
            d[ ( a, b ) ] += math.sqrt( math.pow(point2position[ i ][ 0 ] - bp[0],2) + math.pow(point2position[ i ][ 1 ] - bp[1], 2) )
        
        min = inf
        min_edge = None
        for j in d:
            if d[ j ] < min:
                min = d[ j ]
                min_edge = j
        ind = shape.index( min_edge[0] )
        shape = shape[:ind+1]+[i]+shape[ind+1:]
    cell2wv_list[ cell ] = shape


def read_link_file( link_fn=None ):
    """Read graph representing the cell to cell conections.
    
    <Long description of the function functionality.>
    
    :parameters:
        link_fn : `string`
            Name of the file containing the cell to cell links.
    :rtype: [(cell_id,cell_id)]
    :return: List of cell_ids pairs.
    :raise Exception: <Description of situation raising `Exception`>
    """
    ret = []
    exp  = "[-+]?\d+ [-+]?\d+"
    r = compile( exp )
    f = open( link_fn )
    try:
        for line in f:
            if r.match( line ):
                ret.append( tuple( line.split() ) )
    finally:
        f.close()
    return ret
