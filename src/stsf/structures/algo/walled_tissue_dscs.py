#!/usr/bin/env python
"""The module containing division strategies.

Division strategies have the following signature:

``dscs_*: WalledTissue, cell -> ( (s1, t1, p1), (s2, t2, p2) ) ``

where ``sx``, ``tx`` are ``wv`` of divided wall, ``px`` is a point of division of wall ``sx``, ``tx``.

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
__date__="<Timestamp>"
__version__="0.1"
__docformat__= "restructuredtext en"
__revision__="$Id$"

import walled_tissue_topology
import openalea.plantgl.all as pgl

def dscs_shortest_wall( wt, cell ):
    """Divide Single Cell Strategy: divides taking the shortest possible wall. TODO explain.
    """
    shape = wt.cell2wvs( cell )
    walled_tissue_topology.test_if_division_is_possible( wt, shape )
    dshape = shape+shape
    ls = len(shape)
    vmin = float( "infinity" )
    for i in range( ls ): 
        s1t = wt.wv_pos( dshape[ i ] )
        t1t = wt.wv_pos( dshape[ i+1 ] )
        s2t = wt.wv_pos( dshape[ i+ls/2 ] )
        t2t = wt.wv_pos( dshape[ i+1+ls/2 ] )
        p1t = t1t + (s1t-t1t)/2.
        p2t = t2t + (s2t-t2t)/2.
        if pgl.norm( p1t-p2t ) < vmin:
        #if visual.mag( p1t-p2t ) < vmin:
            vmin = pgl.norm( p1t-p2t ) 
            #vmin = visual.mag( p1t-p2t ) 
            p1 = p1t
            p2 = p2t
            s1 = dshape[ i ]
            t1 = dshape[ i+1 ]
            s2 = dshape[ i+int(ls/2) ]
            t2 = dshape[ i+1+int(ls/2) ]
    return ( (s1, t1, p1), (s2, t2, p2) ) 

def dscs_shortest_wall_with_geometric_shrinking( wt, cell ):
    """Divide Single Cell Strategy: divides taking the shortest possible wall and aditionaly shinks new wall. 
    """
    ( (s1, t1, p1), (s2, t2, p2) ) = dscs_shortest_wall( wt, cell )
    d = (p1 - p2) *0.1
    return ( (s1, t1, p1-d), (s2, t2, p2+d) )


def dscs_first_wall( wt, cell ):
    """Divide Single Cell Strategy: divides taking the first possible wall. TODO explain.
    """
    shape = wt.cell2wvs( cell )
    i = len( shape )
    wt._test_if_division_is_possible( shape ) 
    s1 = shape[0]
    t1 = shape[1]
    s2 = shape[ i/2 ]
    t2 = shape[ i/2+1 ]
    p1 = wt.wv_pos( t1 ) + ( wt.wv_pos( s1 ) - wt.wv_pos( t1 ) )/2.
    p2 = wt.wv_pos( t2 ) + ( wt.wv_pos( s2 ) - wt.wv_pos( t2 ) )/2.
    return ( (s1, t1, p1), (s2, t2, p2) ) 

def dscs_shortest_wall_with_equal_surface( wt, cell, **keys ):
    """Divide Single Cell Strategy: divides taking the shortest possible wall but dividing the cells
    into two parts of same surface.
    
    keys:
    * nbr_of_segments_in_wall == 6
    * length_tolerance == 0.1
    """
    if keys.has_key("nbr_of_segments_in_wall"):
        z = keys[ "nbr_of_segments_in_wall" ]
    else:
        z = 6
    if keys.has_key("length_tolerance"):
        length_tolerance = keys[ "length_tolerance" ]
    else:
        length_tolerance = 0.1
    
    surfs = pqueue.PQueue()
    shape = wt.cell2wvs( cell )
    wt._test_if_division_is_possible( shape )
    dshape = shape+shape
    ls = len(shape)
    vmin = float( "infinity" )
    for i in range( ls ): 
        s1 = dshape[ i ] 
        t1 = dshape[ i+1 ] 
        s2 = dshape[ i+ls/2 ]
        t2 = dshape[ i+1+ls/2 ]
        s1t = wt.wv_pos( s1 )
        t1t = wt.wv_pos( t1 )
        s2t = wt.wv_pos( s2 )
        t2t = wt.wv_pos( t2 )
        
        # getting new cell shapes
        wvc1, wvc2 = wt._test_divide_cell( cell, (s1, t1), (s2, t2) )

        # creating the position dict
        wv2pos = {}
        for wv in shape:
              wv2pos[ wv ] = wt.wv_pos( wv )

        # this loops divide the each wall into 6 segments
        for k in range( 1,z ):
            p1t = t1t + k*(s1t-t1t)/(z+1.)
            p2t = t2t + k*(s2t-t2t)/(z+1.)
            # adding new points coords to calculate area
            wv2pos[ -1 ] = p1t
            wv2pos[ -2 ] = p2t
    
            surf1 = walled_tissue.calculate_cell_surfaceS( wvc1, wv2pos ) 
            surf2 = walled_tissue.calculate_cell_surfaceS( wvc2, wv2pos ) 

            surfs.insert( math.fabs( surf1 - surf2 ), ( (s1, t1, p1t), (s2, t2, p2t) )  )
    
    # getting the shortest wall according to the dscs_shortest_wall strategy
    shortest_possible = wt.dscs_shortest_wall( cell )
    ( (s1sp, t1sp, p1sp), (s2sp, t2sp, p2sp) ) = shortest_possible
    shortest_possible_len = pgl.norm( p1sp - p2sp )
    #shortest_possible_len = visual.mag( p1sp - p2sp )

    # we try to find first good (int terms of shortness) dividing wall
    while len( surfs ):
        val, ( (s1m, t1m, p1m), (s2m, t2m, p2m) ) = surfs.pop()
        if length_tolerance*pgl.norm( p1m - p2m ) < shortest_possible_len: 
        #if wt.const.dscs_shortest_wall_with_equal_surface_length_tolerance*visual.mag( p1m - p2m ) < shortest_possible_len: 
            return ( (s1m, t1m, p1m), (s2m, t2m, p2m) )

    # none of the walls dividing the cell on two semiequal parts is short enought, so we take the shortest
    return shortest_possible

    #return ( (s1m, t1m, p1m), (s2m, t2m, p2m) )
    



