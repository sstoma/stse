#!/usr/bin/env python

"""Class containing the WalledTissue typical algorithms.

This class was designed to keep together the WalledTissue typical algorithms. 

:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    INRIA

"""

# Module documentation variables:
__authors__="""Szymon Stoma    
"""
__contact__=""
__license__="Cecill-C"
__date__="pia mar 30 14:50:15 CEST 2007"
__version__="0.1"
__docformat__= "restructuredtext en"
__revision__="$Id$"


import math
import copy

import openalea.plantgl.all as pgl
import walled_tissue_topology

def create( wt, wv2pos = {}, cell2wv_list = {} ):
    """Creates the WalledTissue structure from data.
        
        :param wv2pos: contains the mapping of ids of wallvertices to their position.
        :param cell2wv_list: contains the mapping of cell ids to ORDERED (in the sens of walls) wv ids.
        :type wv2pos: hash( wv -> pos )
        :type cell2wv_list: hash( cell -> wv_list )
    """
    wt.clear_all()
    walled_tissue_topology.create( wt, cell2wv_list=cell2wv_list)
    
    for i in wv2pos.keys():
        wt.add_wv( wv=i, pos=pgl.Vector3( wv2pos[ i ].x, wv2pos[ i ].y, wv2pos[ i ].z ), call_inherited=False )
    

def cell_center( wt, cell = None ):
    """Return baricenter of cell.
    """
    center = pgl.Vector3() 
    #center = visual.vector() 
    l = wt.cell2wvs( cell )
    for w in l:
        center += wt.wv_pos( w )
    # calculate the baricenter
    #
    return center/ len( l )

def cell_centers( wt):
    """Returns the vertex3 hash of cell 2 baricenter of the cell.
    """
    cc = {}
    for c in wt._cells.nodes():
        cc[ c ] = cell_center( wt, c ) 
    return cc

def _pos2tuple_pos( cell2baricenter ):
    """Returns the hash cell 2 tuple x, y where the x, y are
    coordinats of the baricenter.
    """
    t = {}
    for c in cell2baricenter:
        t[ c ] = (cell2baricenter[ c ].x, cell2baricenter[ c ].y)
    return t

def _pos2tuple_pos_revxy( cell2baricenter ):
    """Returns the hash cell 2 tuple x, y where the x, y are
    coordinats of the baricenter.
    """
    m = pgl.Matrix3().axisRotation((0,0,1),math.pi)
    t = {}
    for c in cell2baricenter:
        t[ c ] = m*cell2baricenter[ c ]
        t[ c ] = (-t[ c ].y, -t[ c ].x)
    return t

def pos2tuple_pos( cell2baricenter ):
    """Returns the hash cell 2 tuple x, y where the x, y are
    coordinats of the baricenter.
    """
    t = {}
    for c in cell2baricenter:
        t[ c ] = (cell2baricenter[c].x, cell2baricenter[c].y)
    return t



def calculate_average_cell_surface( wt ):
    """Calculates the avarage cell surface for all cells in the tissue. Importatnt thing: check for degenerated cells
    before.
    """
    s = 0
    for c in wt.cells():
        s += calculate_cell_surface( wt, cell = c )
    return s/len( wt.cells() )



def investigate_cell( wt, cell ):
    """Gives some data about cell internal representation. Mainly for debugging.
    """
    r = walled_tissue_topology.investigate_cell( wt, cell )
    if r:
        t = wt._cell2properties[ cell ]
        for i in t:
            print "  @",  i, ":", t[ i ]
        #print "  @", "aux_conc",":", wt.cell_property(cell, "auxin_level")/wt.calculate_cell_surface( cell )
        return True
    else:
        return False
    

def find_top_cell_by_z_coord( wt ):
    cell2center = wt.cell_centers()
    max = float("infinity")
    top_cell = wt.cells()[ 0 ]
    for i in cell2center.keys():
        #print cell2center[ i ]
        if max < cell2center[ i ].z:
            max = cell2center[ i ].z
            top_cell = i
    return top_cell

    
def find_top_cell_by_2d_distance_to_center( wt ):
    """Finds top cell by making projection of all cell centers to 2d xy plane
    and finding the closest cell to the overall gravity center.
    
    :return: dict ("center_cell_id", "gravity_center")
    """
    cc = wt.cell_centers()
    #gc = visual.vector()
    gc = pgl.Vector3()    
    for i in cc.values():
        gc += i
    gc = gc/len( cc )
    #gc0 = visual.vector( gc )
    gc0 = pgl.Vector3( gc )
    gc0.z = 0
    r = {}
    for i in cc:
        v = gc0 - cc[ i ]
        v.z = 0
        #r[ visual.mag( v ) ] = i
        r[ pgl.norm( v ) ] = i
    
    return {"center_cell_id": r[ min(r.keys()) ], "gravity_center":gc}


def wv_edge2cell_edge( wt, wv_edge ):
    """<Short description of the function functionality.>
    
    <Long description of the function functionality.>
    
    :parameters:
        arg1 : `T`
            <Description of `arg1` meaning>
    :rtype: `T`
    :return: <Description of ``return_object`` meaning>
    :raise Exception: <Description of situation raising `Exception`>
    """
    cl1 = wt._wv2cell_list[ wv_edge[ 0 ] ]
    cl2 = wt._wv2cell_list[ wv_edge[ 1 ] ]    
    s = []
    for i in cl1:
        if i in cl2:
            s.append( i )
    if len( s ) != 2:
        raise TypeError("Unable to convert from wv_edge to cell_edge")
    return tuple( s )

def cell_edge2wv_edge( wt, cell_edge ):
    """<Short description of the function functionality.>
    
    <Long description of the function functionality.>
    
    :parameters:
        arg1 : `T`
            <Description of `arg1` meaning>
    :rtype: `T`
    :return: <Description of ``return_object`` meaning>
    :raise Exception: <Description of situation raising `Exception`>
    """
    cl1 = wt.cell2wvs_edges( cell=cell_edge[ 0 ] )
    cl2 = wt.cell2wvs_edges( cell=cell_edge[ 1 ] )
    s = []
    for i in cl1:
        if i in cl2:
            return tuple( i )


def calculate_cell_perimiter(wtt, c):
    """Calculates the perimiter of cell cell_id.
    """
    p = 0
    shape = wtt.cell2wvs( c )
    for i in range( len( shape )-1 ):
        p += pgl.norm( wtt.wv_pos( shape[i] ) - wtt.wv_pos( shape[i+1] ) )
        #p += visual.mag( wtt.wv_pos( shape[i] ) - wtt.wv_pos( shape[i+1] ) )
    #print "cell perimiter: ", p
    return p

def calculate_cell_surface( wtt, cell=None, refresh=False ):
    """Calculates cell c surface. Surface is created finding the baricenter,
    and adding the surfaces of triangles which are build up with edge (of the cell)
    and its edges to center. With caching.
    """

        
    shape = wtt.cell2wvs( cell )
    wv2pos = wtt._wv2pos
    return calculate_cell_surfaceS( shape, wv2pos )
    

def calculate_wall_length( wt, wv_edge=None ):
    """Calculate the wall length.
           
    Calculate the wall length.
           
        :parameters:
            wt : `WalledTissue`
                Tissue which contains wall
            wv_edge : ``2tuple of int``
                The wall id.
        :rtype: `float`
        :return: Returns the length of wall
        :raise Exception: TODO
    """
    try:
        p = pgl.norm( wt.wv_pos( wv=wv_edge[ 0 ] ) - wt.wv_pos( wv=wv_edge[ 1 ] ) )
    except Exception:
        print " ! calculate_wall_length exception.."
        return 0.
    return p


def calculate_cell_surfaceS( shape, wv2pos ):
    s = 0
    b = pgl.Vector3() 
    #b = visual.vector() 
    ls = len( shape )
    for i in shape:
        b += wv2pos[ i ]
    b = b/ls
    for i in range( ls ):
        vi_vip = wv2pos[ shape[ (i+1)%ls ] ] - wv2pos[ shape[i] ] 
        vi_b = b - wv2pos[ shape[i] ]
        s += pgl.norm( pgl.cross( vi_vip, vi_b )/2 )
        #s += visual.mag( visual.cross( vi_vip, vi_b )/2 )
    #print "surf:", s
    return s
#calculate_cell_surfaceS = staticmethod( calculate_cell_surfaceS )


def clear_incorrect_neighborhood( wt=None ):
    """Clears wrong neighborhood (as an artifact of editing tools).
    
    <Long description of the function functionality.>
    
    :parameters:
        arg1 : `WalledTissue`
            tissue to be cleaned.
    :raise Exception: <Description of situation raising `Exception`>
    """
    for i in wt.cells():
        for j in wt.cell_neighbors( i ):
            if None==cell_edge2wv_edge( wt, cell_edge=(i,j) ):
                wt._cells.remove_edge(i,j)
                

def avg_cell_property( wt=None, property=None, property_filter=None, property_filter_value=None, consider_surface=False ):
    """Returns avg. cell property for a 
    
    <Long description of the function functionality.>
    
    :parameters:
        arg1 : `WalledTissue`
            tissue to be cleaned.
    :raise Exception: <Description of situation raising `Exception`>
    """    
    mem = 0.
    mem_val = 0.
    for i in wt.cells():
        if wt.cell_property(cell=i, property=property_filter) == property_filter_value:
            if not consider_surface:
                mem_val += wt.cell_property(i, property)
                mem += 1
            else:
                s = calculate_cell_surface( wt, cell=i)
                mem_val += wt.cell_property(i, property) / s
    if not consider_surface:
        if mem > 0: return mem_val / mem
        else: return 0.
    else:  return mem_val
