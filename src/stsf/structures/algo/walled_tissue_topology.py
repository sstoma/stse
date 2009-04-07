#!/usr/bin/env python

"""Algorithms specific for tissue topology.

This module was designed to keep the algorithms for tissue topology
information. 

:todo:
    Translate from class to algorithm.

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


import sets


def create( wtt, cell2wv_list = {} ):
    """Creates the WalledTissue structure from data.
        
        :param cell2wv_list: contains the mapping of cell ids to ORDERED (in the sens of walls) wv ids.
        :type cell2wv_list: hash( cell -> wv_list )
        
        TODO: TEST!!!!!
    """
    
    # to get the cell neighborhood from shared walls
    wv_edges = {}
    for i in cell2wv_list.keys():
        shape = cell2wv_list[ i ]
        l = len( shape )
        for j in shape:
            if j not in wtt._wvs.nodes():
                wtt.add_wv( j )
        wtt.add_cell( i )
        wtt.cell2wvs( cell=i, wv_list=cell2wv_list[ i ] )
        wtt._append_cell2wvs( wvs=cell2wv_list[ i ], c2=i )
        
        for j in range( l ):
            wtt.add_wv_edge( w1= shape[ j ], w2=shape[ (j+1)%l ] )
            if wv_edges.has_key( (shape[ j ], shape[ (j+1)%l  ] ) ):
                wv_edges[ (shape[ j ], shape[ (j+1)%l  ] ) ].append( i )
            else:
                wv_edges[ (shape[ j ], shape[ (j+1)%l  ] ) ] = [ i ] 
    
    for i in wv_edges.keys():
        #TODO we assume that the wall can be shared only between 2 cells
        (s, t) = i
        if len( wv_edges[ i ] ) == 2:
            wtt.add_cell_edge( wv_edges[ i ][ 0 ], wv_edges[ i ][ 1 ] )
        if wv_edges.has_key( (t,s) ):
            wtt.add_cell_edge( wv_edges[ i ][ 0 ], wv_edges[ (t,s) ][ 0 ] )

    # creating the wv2cell
    for c in wtt.cells():
        for w in wtt.cell2wvs( c ):
            #print c, w, wtt.cell2wvs( c ), wtt.wv2cells( w )
            if w not in wtt.cell2wvs( c ):
                wtt.cell2wvs( c, wtt.cell2wvs( c ).append( w ) )
            if c not in wtt.wv2cells( w ):
                wtt.wv2cells( w, wtt.wv2cells( w ).append( c ) )
    initial_find_the_inside_of_tissue( wtt )

def investigate_cell( wtt, cell ):
    """Gives some data about cell internal representation. Mainly for debugging.
    """
    if wtt._cells.has_node( cell ):
        print "Cell id:", cell
        print "Shape:", wtt.cell2wvs( cell ) 
        print "Neighbors:", wtt.cell_neighbors( cell=cell )
        print "WV in this cell are also in:"
        for w in wtt.cell2wvs( cell ):
            print " ", w, ": ", wtt.wv2cells( w )
        return True
    else:
        print "Cell",cell,"doesn't exist.."
        if (wtt._cell2wv_list.has_key( cell ) ):
            print "Problem in _cell2wv_list -- cell not cleared."
        return False

def initial_find_the_inside_of_tissue( wtt ):
    """Changes the internal cell representation to keep cells with the same
    chirality (L or R). The divide operation *should* keep this property.
    """
    #print "ic"
    #raw_input()
    fcell = wtt._cells.nodes()[ 0 ]
    already_searched = sets.Set()
    to_search = [fcell]
    already_searched.add( fcell )
    while len(to_search)>0:
        e = to_search.pop()
        cs = wtt.cell2wvs_edges_in_real_order( e )
        for c in wtt.cell_neighbors( cell = e ):
            if not c in already_searched:
                already_searched.add( c )
                to_search.append( c )
                cs2 = wtt.cell2wvs_edges_in_real_order( c )
                good_order = False
                for j in cs2:
                    rj = (j[1],j[0])
                    if rj in cs:
                        good_order = True
                        break
                if not good_order:
                    wtt.cell2wvs( c, wtt.cell2wvs( c ).reverse() ) 

                    
                        
def create_shapes_for_new_cells( shape, v1, v2 ):
    """Create new cell shapes with a shape from old ones and the data from v1 and v2 (sx, tx. vxd).
    This is internal method. It was made from a piece
    of code which was used inside of _divide_cell, becouse it was needed for division 
    unaffecting the structures. Returns two lists filled with vertices (TODO make expression
    defining these lists). 
    """
    s1, t1, v1d = v1
    s2, t2, v2d = v2
    wvc1 = []
    wvc2 = []
    ls = len( shape )
   
    for i in range( ls ):
        wvc1.append( shape[ i%ls ] )
        stop = i
        if tools.upe( ( shape[ i%ls ], shape[ (i+1)%ls ] ), (s1, t1) ):
            break

    wvc1.append( v1d )
    wvc1.append( v2d )
    wvc2.append( v2d )
    wvc2.append( v1d )

    for i in range( (stop+1)%ls, ls ):
        wvc2.append( shape[ i%ls ] )
        stop = i
        if tools.upe( (shape[ i%ls ], shape[ (i+1)%ls ]), (s2, t2) ) : 
            break 

    for i in range( (stop+1), ls ):
        wvc1.append( shape[ i ] )
    return wvc1, wvc2

    
def test_if_division_is_possible( wtt, shape ):
    """Returns True if cell can be divided. Currently the cell can't be divided if it has less than 3 walls. 
    """
    i = len( shape )
    if i < 3: 
        # TODO drop exception
        print "Skipping division of degenerated cell:", cell
        return False
    return True


def find_degenerated_cells( wtt ):
    for i in wtt.cells():
        if len( wtt.cell2wvs( cell=i ) ) < 3:
            print " ! degenerated cell:", i, wtt.cell2wvs( cell=i )
    for i in wtt.wvs():    
        if len( wtt.wv2cells( wv=i ) ) != 3 and len( wtt.wv2cells( wv=i ) ) != 2:
            print " ! degenerated wv:", i, wtt.wv2cells( wv=i )


