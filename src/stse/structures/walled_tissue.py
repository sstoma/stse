#!/usr/bin/env python

"""Class containing the WalledTissue object.

This class was designed to keep the walled tissue information. The tissue is represented as polygonal mesh.
Currently a tissue consists from topological and physiological information.

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
__version__="0.2"
__docformat__= "restructuredtext en"
__revision__="$Id$"


import copy
import walled_tissue_topology


class WalledTissue(walled_tissue_topology.TissueTopology):
    """
    Gathers information (curently Topology+Physiology) about Tissue. This is
    main *data structure* for storing Tissue related properties. It extends
    ``walled_tissue_topology.TissueTopology`` to store tissue physiology and
    basic physiology editing algorithms. It inherits because the physiology
    requires topology.
    """

    def __init__( self, const=None ):
        """Basic constructor. Const is the configuration Class.
        """
        walled_tissue_topology.TissueTopology.__init__( self, const=const )
        
        self._wv_edge2properties={}
        """#: contains properties of wv_edge"""
        self._wv2properties={}
        """#: contains properties of wv"""
        self._cell2properties={}
        """#: contains properties of cell"""
        self._cell_edge2properties={}
        """#: contains properties of cell_edge"""
        self._wv2pos = {}
        """:# to store the positions"""
        self._tissue_properties = {}
        """:# to store information about the tissue"""
                
        self._init_tissue_properties()

    def wv_pos( self, wv=None, pos = None ):
        """Returns/Sets the position of wall vertex
        """
        if (pos == None):
            return self._wv2pos[ wv ]
        else:
            self._wv2pos[ wv ] = pos
        return None

 
    def add_cell_edge( self, c1=None, c2=None):
        """ Add the cell neighborhood between cells: c1 and c2.
        """
        c = walled_tissue_topology.TissueTopology.add_cell_edge( self, c1=c1, c2=c2 )
        self._init_cell_edge_properties(  c )
        return c

    def add_cell( self, cell=None, shape=None):
        """ Adds the cell neighborhood between c1 and c2.
        If shape is given the microtubules orientation is set
        """
        if shape==None:
            cell_id = walled_tissue_topology.TissueTopology.add_cell( self, cell=cell )
            self._init_cell_properties( cell_id )
        else:
            self.cell2wvs( cell=cell, wv_list=shape )
                        
        return cell_id
           
    def add_wv_edge( self, w1=None, w2=None):
        """Adds wall between w1 and w2. If w1 or w2 doesn't exist
        throw exception
        """
        w = walled_tissue_topology.TissueTopology.add_wv_edge( self, w1=w1, w2=w2 )
        self._init_wv_edge_properties(  w )
        return w
 
    def add_wv( self, wv = None, pos = (0., 0., 0.), call_inherited=True ):
        """Adds wall vertex with position.
        """
        if call_inherited:
            wv_id = walled_tissue_topology.TissueTopology.add_wv( self, wv = wv )
        else:
            wv_id = wv
        self._init_wv_properties( wv=wv_id )
        self.wv_pos( wv=wv_id, pos=pos )
        return wv_id

    def clear_all( self ):
        """Clears structure.
        """
        walled_tissue_topology.TissueTopology.clear_all( self )
        self._wv2pos = {}
        self._wv_edge2properties={}
        self._wv2properties={}
        self._cell2properties={}
        self._cell_edge2properties={}
        self._tissue_properties = {}
        self._init_tissue_properties()

    
    # BEGIN Physiology related methods
    
    # BEGIN wv_edge properties
    def _init_wv_edge_properties( self, wv_edge=None):
        """Inits wv edge properties. All properties should be initialised here.
        """
        self._wv_edge2properties[ wv_edge ] = {}
        for i in self.const.wv_edge_properties:
            self._wv_edge2properties[ wv_edge ][ i ] = self.const.wv_edge_properties[ i ]

    def  wv_edge_property( self, wv_edge=None, property=None, value=None ):
        """Returns/sets property for wv_edge
        """
        if value == None:
            return self._wv_edge2properties[ self.wv_edge_id( wv_edge ) ][ property ]
        else:
            self._wv_edge2properties[ self.wv_edge_id( wv_edge ) ][ property ] = value
    
    # END wv_edge properties
    
    # BEGIN wv properties
    def _init_wv_properties( self, wv=None):
        """Inits wv properties. All properties should be initialised here.
        """
        self._wv2properties[ wv ] = {}
        for i in self.const.wv_properties:
            self._wv2properties[ wv ][ i ] = self.const.wv_properties[ i ]
 
    def  wv_property( self, wv=None, property=None, value=None ):
        """Returns/sets property for wv
        """
        if value == None:
            return self._wv2properties[ wv  ][ property ]
        else:
            self._wv2properties[ wv  ][ property ] = value
    
    # END wv properties
    
    # BEGIN cell properties
    def _init_cell_properties( self, cell=None):
        """Inits wv properties. All properties should be initialised here.
        """
        self._cell2properties[ cell ] = {}
        for i in self.const.cell_properties:
            self._cell2properties[ cell ][ i ] = self.const.cell_properties[ i ]
                
    def  cell_property( self, cell=None, property=None, value=None ):
        """Returns/sets property for cell
        """
        if value == None:
            return self._cell2properties[ cell ][ property ]
        else:
            self._cell2properties[ cell  ][ property ] = value

    def has_cell_property( self, cell=None, property=None):
        """True iff property exists
        """
        return self._cell2properties[ cell ].has_key( property )

    # END cell properties
    
    # BEGIN tissue properties
    def _init_tissue_properties( self ):
        """Inits tissue properties. All properties should be initialised here.
        """
        for i in self.const.tissue_properties.keys():
            self._tissue_properties[ i ] = self.const.tissue_properties[ i ]


            
    def  tissue_property( self, property=None, value=None ):
        """Returns/sets property for cell
        """
        if value == None:
            return self._tissue_properties[ property ]
        else:
            self._tissue_properties[ property ] = value

    def has_tissue_property( self, property=None):
        """True iff property exists
        """
        return self._tissue_properties.has_key( property )


    # END tissue properties
    
    # BEGIN cell edge properties
    def _init_cell_edge_properties( self, cell_edge=None):
        """Inits cell_edge properties. All properties should be initialised here.
        """
        k,l = cell_edge
        self._cell_edge2properties[ cell_edge ] = {}
        self._cell_edge2properties[ (l,k) ] = {}
        for i in self.const.cell_edge_properties:
            #print " #Initializing: ", i
            #self._cell_edge2properties[ self.cell_edge_id( cell_edge ) ][ i ] = copy.copy( self.const.cell_edge_properties[ i ] )
            self._cell_edge2properties[ cell_edge ][ i ] = copy.copy( self.const.cell_edge_properties[ i ] )
            self._cell_edge2properties[ (l,k) ][ i ] = copy.copy( self.const.cell_edge_properties[ i ] )
            
    def  cell_edge_property( self, cell_edge=None, property=None, value=None ):
        """Returns/sets property for non-directed cell_edge. Property is set
        for both directions. When asking about property value, one of the
        cell_edges is queried.
        """
        if value == None:
            #return self._cell_edge2properties[ self.cell_edge_id( cell_edge ) ][ property ]
            return self._cell_edge2properties[ cell_edge ][ property ]
        else:
            #self._cell_edge2properties[ self.cell_edge_id( cell_edge ) ][ property ] = value
            self._cell_edge2properties[ cell_edge ][ property ] = value
            self._cell_edge2properties[ ( cell_edge[ 1 ], cell_edge[ 0 ] ) ][ property ] = value
            
    def  directed_cell_edge_property( self, cell_edge=None, property=None, value=None ):
        """Returns/sets property for directed cell_edge.
        """
        if value == None:
            return self._cell_edge2properties[ cell_edge ][ property ]
        else:
            self._cell_edge2properties[ cell_edge ][ property ] = value

    
    # END cell edge properties
    
    # END Physiology related methods





    def divide_cell( self, cell, dscs, pre_fun=None, post_fun=None):
        """Divides a cell acording to dscs strategy.
        
        TODO: i should put division pre/post in the divide_cells. it should be done to edit properties, etc.
        """
        
        # TODO swith to properties.
        if pre_fun:
            pre_res = pre_fun( self, cell )
        
        ( (s1, t1, p1), (s2, t2, p2) ) = dscs( self, cell )
        r = walled_tissue_topology.TissueTopology.divide_cell( self, cell=cell, dscs=dscs )
        changed , ( ( v1d, s1 ), ( v1d, t1 ),( v2d, s2 ),( v2d, t2 ),( v1d, v2d ) ) = r[0]
        if not changed:
            x = ( v1d, p1 ), (v2d, p2)
            self.wv_pos( wv=v1d, pos=p1 )
            self.wv_pos( wv=v2d, pos=p2 )
        else:
            x = ( v1d, p2 ), (v2d, p1)    
            self.wv_pos( wv=v1d, pos=p2 )
            self.wv_pos( wv=v2d, pos=p1 )
        r = (x, ( ( v1d, s1 ), ( v1d, t1 ),( v2d, s2 ),( v2d, t2 ),( v1d, v2d ) ) , r[1:] )
        
        if post_fun:
            post_res = post_fun( self, pre_res=pre_res, div_res=r )
                             
        return r

            
    def remove_cell( self, cell=None ):
        """Removes the cell.
        
        :param cell: cell to remove
        :type cell: ``cell`` id
        """
        
        for n in self.cell_neighbors( cell = cell ):
            del self._cell_edge2properties[ self.cell_edge_id( (cell,n) ) ] 
        try:
            del self._cell2properties[ cell ]
        except:
            print "!properties does not exist.."
        return walled_tissue_topology.TissueTopology.remove_cell( self, cell = cell )
        
        
    def clear_properties( self ):
        self.clear_cell_properties()
        #self.clear_cell_edge_properties()
        self.clear_tissue_properties()
        #self.clear_wv_properties()
        #self.clear_wv_edge_properties()

    def clear_cell_properties( self ):
        for i in self.cells():
            self._init_cell_properties( i )

    def clear_tissue_properties( self ):
        self._init_tissue_properties()





    
if __name__ == '__main__':
    ##DEPANDS FROM CONF CODE
    #wt = WalledTissue( TwoCellsConst() )
    #
    #print "__ INIT CELL"
    #for c in wt.cells(): wt.investigate_cell( c )
    #for i in range(2):
    #    for c in wt.cells():
    #        print "__ DIVIDING CELL", c
    #        wt.divide_cell( c, walled_tissue_topology.TissueTopology.dscs_first_wall )
    #        for c in wt.cells(): wt.investigate_cell( c )
    #    wt.show_cells_with_wvs(True)
    #for i in wt.cells():
    #    print "__ REMOVING CELL", i
    #    wt.remove_cell( i )
    #    wt.show_cells_with_wvs(True)
    pass
