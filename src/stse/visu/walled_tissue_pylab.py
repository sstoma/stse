#!/usr/bin/env python

"""Functions containing walled_tissue pylab visualisation.


:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    INRIA/HU

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

##BEGIN DOC REMOVE
import networkx as nx
import pylab as pl
##END DOC REMOVE
from ..structures.algo.walled_tissue import pos2tuple_pos, cell_centers

def show_cells( wt, with_labels = True, cell_node_size=0.1 ):
    """Plot cells projection on XY plane (does not draw walls).
    """
    nx.draw_networkx( wt._cells.to_undirected(), pos2tuple_pos( cell_centers( wt ) ), with_labels=with_labels, style='dotted', node_size= cell_node_size )
    nx.draw_networkx_edges( wt._wvs, pos2tuple_pos( wt._wv2pos ), edge_color='r' )
    pl.show()

def show_cells_with_wvs( wt, with_labels = True, cell_node_size=0.1, wv_node_size=0.1 ):
    """Plot cells projection on XY plane (draws walls).
    """
    nx.draw_networkx( wt._cells.to_undirected(), pos2tuple_pos( cell_centers( wt ) ), with_labels=with_labels, style='dotted', node_size= cell_node_size )
    nx.draw_networkx( wt._wvs, pos2tuple_pos( wt._wv2pos ), edge_color='r', with_labels=with_labels,node_size= wv_node_size )
    pl.show()