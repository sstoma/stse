#!/usr/bin/env python

"""Class containing the tissue topology.

This class was designed to keep the tissue topology information. The tissue is represented as polygonal mesh.

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
__date__="pi mar 30 14:50:15 CEST 2007"
__version__="0.1"
__docformat__= "restructuredtext en"
__revision__="$Id$"

##BEGIN DOC REMOVE
import networkx as nx
##END DOC REMOVE
import copy

import openalea.stsf.tools.misc as tools
import openalea.plantgl.all as pgl
from  openalea.stsf.structures.algo.walled_tissue_topology import create_shapes_for_new_cells

## BEGIN pickle visual vectors
#import visual
#import cPickle as pickle
#import copy_reg
#def dump_visual_vector( v ):
#    return (visual.vector, ( v.x,v.y,v.z ) )
#copy_reg.pickle(visual.vector, dump_visual_vector)
## END pickle visual vectors

class TissueTopology:
    """This is basic class to store tissue topology information. The types used:
    
        * wv: wall vertex (cell corner)
        * wv_edge: (cell wall)
        * cell: (cell)
        * cell_edge: (cell neighborhood relation)
    
    Positions of `wv` are somehow separeted from properties. This is due
    to the fact that they need to be accessed faster than other properties -
    they are used in physical simulation.
    
    TODO:
    
    next time very important feature could be used:
    
    the cells2wvs should be replaced by cells2edges and edges2cells. all the 
    relation between the cells and its geometry should be between cell to wall edge
    and not like it is now cell to wall vertex. this will simplyfy many other rutines 
    and having a set of edges easily a set of ordered wvs can  be computed. 
    """
    def __init__( self, const = "!SetCorrectConstants!"  ):
        self._wvs = nx.Graph( name = 'CellWalls' )
        """#: to store the information about the cell wvs"""
        self._cells = nx.Graph( name = 'Cells' )
        """#: to store the information about the cell neigborhood relation"""
        self._cell2wv_list = {}
        """#: to store the relation between cells and *ordered* wv"""
        self._wv2cell_list = {}
        """#: to store the realation between walls and cells"""
        
        self._last_wv_id = 0
        """#: to store the free id for wv"""
        self._last_cell_id = 0
        """#: to store the free id for cell"""

        self.const = const
        """#: constants used in simulations."""
 
    
    def clear_all( self ):
        """ Clears the tissue. After this operation the structure is empty
        (cells and walls are removed).
        """
        self._cells.clear()
        self._wvs.clear()
        self._cell2wv_list = {}
        self._wv2cell_list = {}

    def add_cell( self, cell = None ):
        """ Adds new cell. If cell is given it is used to identify a
        cell. Otherwise the new one is generated using _new_cell_id. Currently
        no checking is done if the cell id is not already taken.
        
        :param cell: new cell id ( None to autoassign).
        :type cell:  cell id (currently int)
        """
        if cell == None:
            cell = self._new_cell_id()
        self._update_last_cell_id( cell )
        self._cells.add_node( cell )
        self._cell2wv_list[ cell ] = []
        return cell
    
    def add_wv( self, wv = None ):
        """Adds wall vertex with position. If wv is given it is used to identify a wall vertex.
        Otherwise the new one is generated using _new_wv_id. Currently
        no checking is done if the wv id is not already taken.
        
        :param wv: new wv id ( None to autoassign).
        :type wv:  wv id (currently int)
        """
        if wv == None:
            wv = self._new_wv_id()
        self._update_last_wv_id( wv )
        self._wvs.add_node( wv )
        self._wv2cell_list[ wv ] = [] 
        return wv

    def add_cell_edge( self, c1=None, c2=None):
        """Adds the edge between cells: c1 and c2.
         
        :raise KeyError: if the c1 or c2 does not exist.
        :param c1: first cell.
        :type c1:  cell id (currently int)
        :param c2: second cell.
        :type c2:  cell id (currently int)
        :return: id of added cell edge.
        :rtype: cell_edge id (currently ordered int 2tuple)
        """
        if not self._cells.has_node( c1 ) or not self._cells.has_node( c2 ):
            raise KeyError("No cell vertex.")
        else:
            self._cells.add_edge( c1, c2 )
            return self.cell_edge_id( (c1, c2 ) )
        
    def add_wv_edge( self, w1=None, w2=None):
        """Adds wall between w1 and w2. If w1 or w2 doesn't exist
        throw exception.

        :raise KeyError: if the w1 or w2 does not exist.
        :Parameters:
            `w1` : wv id (currently int)
                first wv.
            `w2` : wv id (currently int)
                second wv.
            
        :return: id of added wv_edge.
        :rtype: wv_edge id (currently ordered int 2tuple)
        """
        if not self._wvs.has_node( w1 ) or not self._wvs.has_node( w2 ):
            raise KeyError("No wall vertex.")
        else:
            self._wvs.add_edge( w1, w2 )
            return  self.wv_edge_id( (w1,w2) )       

    def cells( self ):
        """Returns collection of cells.
        """
        return self._cells.nodes()
    
    def cell_neighbors( self, cell = None ):
        """Returns neighbors of the cell.
        """
        try:
            return self._cells.neighbors( cell )
        except Exception:
            print " !cell neighbor does not exist.."
            return []
        
    def wvs( self ):
        """Returns collection of wvs.
        """
        return self._wvs.nodes()
    
    def cell_edges( self ):
        """Return the collection of cell edges.
        """
        l = self._cells.edges()
        z = []
        for i in l:
            (i1, i2) = i
            if i1 < i2:
                z.append(i)
            else:
                z.append((i2,i1))
        return z

    def wv_edges( self ):
        """Returns the collection of cell edges.
        """
        l = self._wvs.edges()
        z = []
        for i in l:
            (i1, i2) = i
            if i1 < i2:
                z.append(i)
            else:
                z.append((i2,i1))
        return z

    def nth_layer_from_cell( self, cell=None, distance=1, smaller_than=False ):
        """Returns  the list of cells with discret (graph) distance from ``cell`` equal/smaller ``distance``.
        
        :Parameters:
            cell : ``cell`` id
                the cell from which distance is measured.
            distance : int
                distance ( default=1 )
            smaller_than : bool
                if True the cells which are <= are returned insted of = (default=False) 
        """
        l = nx.bfs_length( self._cells, cell )
        result = []
        for i in l.keys():
            if smaller_than:
                if l[ i ] <= distance:
                    result.append( i )
            else:                
                if l[ i ] == distance:
                    result.append( i )
        return result
    
    
    def cell2wvs( self, cell, wv_list = None):
        """Returns/Sets **ordered** list of vertices associated with the cell.
        
        :Parameters:
            cell : `cell`
                `cell` to return/set the list of vertices.
            wv_list : ``list( wv )`` or ``None``
                if `wv_list` is  ``None`` the curent value for `cell` is returned. Otherwise it is set to `wv_list``. 
        """
        if wv_list == None:
            return self._cell2wv_list[ cell ]
        else:
            self._cell2wv_list[ cell ] = wv_list
        return None

    def wv2cells( self, wv, cell_list = None ):
        """Returns/Sets list of cells associated with the wv.

        :Parameters:
            `cell_list` : ``list( cell )`` or ``None`` 
                ``cells`` to assign to ``wv``.
            `wv` :  wv
                if ``cell_list`` is  ``None`` the curent value for ``wv`` is returned. Otherwise it is set to ``cell_list``. 
        """
        if cell_list == None:
            return self._wv2cell_list[ wv ]
        else:
            self._wv2cell_list[ wv ] = cell_list
        return None


    def remove_cell( self, cell=None ):
        """Removes the cell.
        
        :Parameters:
            `cell` : ``cell`` id
                id of the cell to be removed.
        :return: a dictionary containing removed `wv_edges` id list and removed `wv` id list  
        :rtype: dict{"removed_wv_edges": [..], "removed_wv" : [..]}
        """
        cell_shape = self.cell2wvs( cell )
        cell_shape_edges = self.cell2wvs_edges( cell )
        wv2del = []
        wv_edge2del = []
        for wv in cell_shape:
            if self.wv2cells( wv ) == [ cell ]:
                wv2del.append( wv )
        
        neighbors_edges = []
        for n in self.cell_neighbors( cell ):
            for e in self.cell2wvs_edges( n ):
                neighbors_edges.append( e )
        
        for e in cell_shape_edges:
            if not e in neighbors_edges:
                wv_edge2del.append( e )
                
        for wv in wv2del:
            self._remove_wv( wv )
        
        for wv_edge in wv_edge2del:
            self._wvs.delete_edge( wv_edge[ 0 ], wv_edge[ 1 ] )

        for wv in self.cell2wvs( cell ):
            #try:
            #    self.wv2cells( wv, self.wv2cells( wv ).remove( cell ) )
            #except ValueError:
            #    #TODO why??    
            #    pass
            self.wv2cells( wv, self.wv2cells( wv ).remove( cell ) )
        self._cell2wv_list.pop( cell )
        self._cells.delete_node( cell )

        return {"removed_wv_edges": wv_edge2del, "removed_wv" : wv2del}

    def cell_has_wall( self, c, (s, t)):
        """Returns True if cell contains wall (s, t).
        """
        shape = self.cell2wvs( c )
        ls = len( shape )
        for i in range( ls ):
            if ( s == shape[ i%ls ] and t == shape[ (i+1)%ls ] ) or ( t == shape[ i%ls ] and s == shape[ (i+1)%ls ] ): 
                return True
        return False


    def cell2wvs_edges( self, cell ):
        """ Return a list of wvs_edges which surround the cell. 
        
        """
        l = []
        shape = self.cell2wvs( cell )
        ls = len( shape )
        for i in range( ls ):
            if  shape[ i ] < shape[ (i+1)%ls ]:
                l.append( (shape[ i ], shape[ (i+1)%ls ]) )
            else:
                l.append( (shape[ (i+1)%ls ], shape[ i ]) )
        return l

    def cell2wvs_edges_in_real_order( self, cell ):
        """ Return a list of wvs_edges which surround the cell. 
        
        Note: returned ids *may not* be valid wall ids.
        """
        l = []
        shape = self.cell2wvs( cell )
        ls = len( shape )
        for i in range( ls ):
            l.append( (shape[ i ], shape[ (i+1)%ls ]) )
        return l

    def wv_edge_id( self, wv_edge=None ):
        """Returns good id for wv_edge 
        
        :param wv_edge: id of the wv_edge
        :type wv_edge: 2tuple of wall_vertex_id (currenty int tuple)
        :return: correct id of the wv_edge
        :rtype: 2tuple of wall_vertex_id (currenty int tuple)"""

        w1, w2 = wv_edge
        if w1 > w2:
            return (w2, w1)
        else:
            return wv_edge


    def cell_edge_id( self, id ):
        """Returns good id for cell_edge 
        
        :param id: id of the cell_edge
        :type id: 2tuple of cell_id (currenty int tuple)
        :return: correct id of the cell_edge
        :rtype: 2tuple of cell_id (currenty int tuple)"""

        w1, w2 = id
        if w1 > w2:
            return (w2, w1)
        else:
            return id

    def divide_cell( self, cell, dscs):
        """Divides the cell with given strategy of the division.
        """
        ( (s1, t1, p1), (s2, t2, p2) ) = dscs( self, cell )
        return self._divide_cell( cell, (s1, t1), (s2, t2) )
    
    def _clear_unasigned_wvs( self ):
        """Clears wvs which are not assigned to any cell
        """
        for wv in self.wvs(): 
            if self.wv2cells( wv ) == []:
                self._wv2cell_list.pop( wv )
                self._wvs.delete_node( wv )

    def _remove_wv( self, wv ):
        """Removes the wv from the tissue.
        
        Note: _cell2wv_list *IS NOT* updated
        """
        for c in self.wv2cells( wv ):
            self.cell2wvs( c, self.cell2wvs( c ).remove( wv ) )
        self._wv2cell_list.pop( wv )
        self._wvs.delete_node( wv )
    


    def _new_cell_id( self ):
        """Creates new id for a cell
        """
        self._last_cell_id += 1
        return self._last_cell_id

    def _new_wv_id( self ):
        """Creates new id for a wv 
        Note: i assume that it is never negative (i use it will 'testadding' new vertices while 
        new cell shape 'testcreating'..)
        """
        self._last_wv_id += 1
        return self._last_wv_id


    def _update_last_wv_id( self, id ):
        """Updates id for wv.
        """
        if self._last_wv_id < id:
            self._last_wv_id = id

    def _update_last_cell_id( self, id ):
        """Updates id for cell.
        """
        if self._last_cell_id < id:
            self._last_cell_id = id



    
    def _divide_cell( self, cell, i1,  i2 ):
        """Internal cell division updating all the structures.

        return format:
        (v1d, v2d) - added vertices descriptors
        (removed_wall1, removed_wall2
        ( v1d, s1 )
        ( v1d, t1 )
        ( v2d, s2 )
        ( v2d, t2 )
        ( v1d, v2d )
        return ( ( changed , ( ( v1d, s1 ), ( v1d, t1 ),( v2d, s2 ),( v2d, t2 ),( v1d, v2d ) ) ), {"removed_cell":cell, "added_cell1":  c1, "added_cell2": c2} )
        """
        ( s1, t1 ) = i1
        ( s2, t2 ) = i2
        # finding good order of s1, t1 and s2, t2
        shape = self.cell2wvs( cell )
        # finding which edge is first
        s1, t1 = tools.find_edge_order( s1, t1, shape)
        s2, t2 = tools.find_edge_order( s2, t2, shape)
        first_order = copy.copy((s1, t1, s2, t2))
        second_order = tools.find_edges_order( s1, t1, s2, t2, shape)
        s1, t1, s2, t2 = second_order
        if first_order == second_order:
            changed = False
        else:
            changed = True
        # now we have assumptions:
        # -- for i in {1,2}: si, ti is in shape on positions: if shape[k_i]=si then shape[(k+1)_i]=ti
        # -- k_1 < k_2
        v1d = self.add_wv( None )
        v2d = self.add_wv( None )
        
        self.add_wv_edge( v1d, s1 )
        self.add_wv_edge( v1d, t1 )
        self.add_wv_edge( v2d, s2 )
        self.add_wv_edge( v2d, t2 )
        self.add_wv_edge( v1d, v2d )

        # the v1d, v2d must be added to neighbor cells
        for c in self._cells.neighbors( cell ):
            #print "self.cell_has_wall( c, (s1, t1 ) ):", c, (s1, t1)
            if self.cell_has_wall( c, (s1, t1 ) ):
                #print "ok"
                self._append_cell2wvs( [v1d], c )
                break
        for c in self._cells.neighbors( cell ):
            #print "self.cell_has_wall( c, (s1, t1 ) ):", c, (s2, t2)
            if self.cell_has_wall( c, (s2, t2 ) ):
                #print "ok"
                self._append_cell2wvs( [v2d], c )
                break

        wvc1, wvc2 = create_shapes_for_new_cells( shape, (s1, t1, v1d), (s2, t2, v2d) )
        
        c1 = self.add_cell()
        c2 = self.add_cell()
        self.cell2wvs( c1, wvc1 )
        self.cell2wvs( c2, wvc2 )
        self.add_cell_edge( c1, c2 )
        
        c1n = []
        for wv in wvc1:
            c1n += self.wv2cells( wv )
        for c in dict(map(lambda a: (a,1), c1n)).keys(): 
            self.add_cell_edge( c, c1 )

        c2n = []
        for wv in wvc2:
            c2n += self.wv2cells( wv )
        for c in dict(map(lambda a: (a,1), c2n)).keys():
            self.add_cell_edge( c, c2 )
        
        for z in [c1, c2]:
            for wv in self.cell2wvs( z ):
                for c in self.wv2cells( wv ):
                    self.add_cell_edge( c, z )

        ##m_f
        neighbor_cells = []
        for i in [s1, t1, s2, t2]:
            neighbor_cells += self.wv2cells( i )
        neighbor_cells = dict(map(lambda a: (a,1), neighbor_cells)).keys()
        for c in neighbor_cells:
            self._exchange_wvs( c, (s1,t1), v1d )
            self._exchange_wvs( c, (s2,t2), v2d )
        
        self._wvs.delete_edge( s1, t1 )
        self._wvs.delete_edge( s2, t2 )

        self._append_cell2wvs( wvc1, c1)
        self._append_cell2wvs( wvc2, c2)

        ##m_f
        self.remove_cell( cell )

        #self.investigate_cell( c1 )
        #self.investigate_cell( c2 )
        
        # return format:
        # (v1d, v2d) - added vertices descriptors
        # (removed_wall1, removed_wall2
        #( v1d, s1 )
        #( v1d, t1 )
        #( v2d, s2 )
        #( v2d, t2 )
        #( v1d, v2d )
        return ( ( changed , ( ( v1d, s1 ), ( v1d, t1 ),( v2d, s2 ),( v2d, t2 ),( v1d, v2d ) ) ), {"removed_cell":cell, "added_cell1":  c1, "added_cell2": c2} )



    def _append_cell2wvs( self, wvs, c2):
        """Sets wv2cells for each wv in wvs. 
        """
        if not self._cells.has_node( c2 ): raise Exception("Cell doesn't exist.") 
        for wv in wvs:
            t = self.wv2cells( wv )
            t.append( c2 )
            #filter
            self.wv2cells( wv, dict(map(lambda a: (a,1), t)).keys() )

    def _exchange_wvs( self, c, (s1,t1), v1d ):
        """Exchange the wall s1, t1 for cell c with two walls s1 v1d and v1d t1. Do nothing
        if the wall can not be found.
        """
        #TODO opt
        if not self.cell_has_wall( c, (s1, t1) ): return
        shape = self.cell2wvs( c )
        ls = len( shape )
        i = shape.index( s1 )
        if t1 == shape[ (i+1)%ls ]: 
            i += 1
            self.cell2wvs( c, shape[:i]+[v1d]+shape[i:])
        else:
             self._exchange_wvs( c, (t1,s1), v1d )



