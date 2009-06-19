#!/usr/bin/env python
"""Influence zone rutines.

The code used to analyze influence zones.

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

from copy import copy

def set_property_on_tissue_component( wt=None, cell=None, f_component=None, tol=None, property=None, property_value=None,
                                     with_neighbors=True, fill_gaps=True, additional_vertices=[]):
    """Sets given property to given value on a component of tissue.
    
    <Long description of the function functionality.>
    
    :parameters:
        arg1 : `T`
            <Description of `arg1` meaning>
    :rtype: `T`
    :return: <Description of ``return_object`` meaning>
    :raise Exception: <Description of situation raising `Exception`>
    """
    
    from networkx import DiGraph
    from networkx.search import dfs_preorder
    g=DiGraph()
    
    #initialization cell
    g.add_node(cell)
    wt.cell_property( cell, property, property_value )

    #initialization cell neigh.
    if with_neighbors:
        for i in wt.cell_neighbors( cell ):
            g.add_node(i)
            wt.cell_property( i, property, property_value )

    for i in additional_vertices:
        g.add_node(i)
        wt.cell_property( i, property, property_value )
    
    for (i,j) in wt.cell_edges():
        if f_component(wt, (i, j)) > tol:
            g.add_edge(j, i)
        if f_component(wt, (j, i)) > tol:
            g.add_edge(i, j)
    dfs=dfs_preorder( g, cell)
    for i in dfs:
        wt.cell_property( i, property, property_value )

    added=copy(dfs)
    if with_neighbors:
        for j in wt.cell_neighbors( cell )+additional_vertices:
            if j not in dfs:
                for i in dfs_preorder( g, j):
                    wt.cell_property( i, property, property_value )
                    added.append( i )
    
    # filing the gaps
    if fill_gaps:
        changed=added
        for i in wt.cells():
            nei = wt.cell_neighbors( i )
            k = 0
            for n in nei:
                if n in changed:
                    k+=1
                else:
                    continue
                if k > len(nei)-2:
                    changed.append( i )
                    wt.cell_property( i, property, property_value )
                    break           
    
def set_property_with_weight_on_tissue_component( wt=None, cell=None, f_component=None, tol=None, property=None, property_value=None,
                                     with_neighbors=True, fill_gaps=True, additional_vertices=[]):
    """Sets given property to given value on a component of tissue.
    
    <Long description of the function functionality.>
    
    :parameters:
        arg1 : `T`
            <Description of `arg1` meaning>
    :rtype: `T`
    :return: <Description of ``return_object`` meaning>
    :raise Exception: <Description of situation raising `Exception`>
    """
    
    from networkx import DiGraph
    from networkx.search import dfs_preorder
    g=DiGraph()
    
    #initialization cell
    g.add_node(cell)
    wt.cell_property( cell, property, property_value )

    #initialization cell neigh.
    if with_neighbors:
        for i in wt.cell_neighbors( cell ):
            g.add_node(i)
            wt.cell_property( i, property, property_value )

    for i in additional_vertices:
        g.add_node(i)
        wt.cell_property( i, property, property_value )
    
    for (i,j) in wt.cell_edges():
        if f_component(wt, (i, j)) > tol:
            g.add_edge(j, i)
        if f_component(wt, (j, i)) > tol:
            g.add_edge(i, j)
    dfs=dfs_preorder( g, cell)
    for i in dfs:
        wt.cell_property( i, property, property_value )

    added=copy(dfs)
    if with_neighbors:
        for j in wt.cell_neighbors( cell )+additional_vertices:
            if j not in dfs:
                for i in dfs_preorder( g, j):
                    wt.cell_property( i, property, property_value )
                    added.append( i )
    
    # filing the gaps
    if fill_gaps:
        changed=added
        for i in wt.cells():
            nei = wt.cell_neighbors( i )
            k = 0
            for n in nei:
                if n in changed:
                    k+=1
                else:
                    continue
                if k > len(nei)-2:
                    changed.append( i )
                    wt.cell_property( i, property, property_value )
                    break           
    from networkx.path import single_source_dijkstra_path


    d = single_source_dijkstra_path(g, cell )
    # ind contains how many each vertex was met in the paths
    ind = {}
    for j in d.values():
        for i in j:
            if not ind.has_key(i):
                ind[ i ] = 1
            else:
                ind[ i ] = ind[ i ] + 1
    
    for i in wt.cells():
        if i in ind.keys():
            wt.cell_property( i, property, ind[ i ] )