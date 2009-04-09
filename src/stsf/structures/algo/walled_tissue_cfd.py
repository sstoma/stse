#!/usr/bin/env python
"""The "function cell to division selection" from tissue and strategies .

Here the functions which select the cells to division from the tissue
should be putted. The funtions should have following syntax:

``cfd_*: WalledTissue -> list( cell )``

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

from walled_tissue import calculate_cell_surface

def cfd_perimiter_rule(wtt):
    """Returns list of cells which should divide acording to perimiter rule"""
    to_divide = []
    for c in wtt.cells():
        if wtt.calculate_cell_perimiter( c ) > wtt.const.cs_peri_trashhold_perimiter_to_divide_cell: to_divide.append( c )
    return to_divide 

def cfd_surface_rule(wtt):
    """Returns list of cells which should divide acording to surface rule"""
    to_divide = []
    for c in wtt.cells():
        if calculate_cell_surface( wtt, c ) > wtt.const.cs_surf_max_surface_before_division: to_divide.append( c )
    return to_divide

def ds_perimiter( wtt, dscs ):
    """Division strategy: Divides cells acording to perimiter rule."""
    divide_cells = cfd_perimiter_rule( wtt )
    l = []
    for c in divide_cells:
        l.append( wtt.divide_cell( c, dscs ) )
    return l

def ds_surface( wtt, dscs, pre, post ):
    """Division strategy: Divides cells acording to perimiter rule."""
    divide_cells = cfd_surface_rule( wtt )
    print divide_cells
    l = []
    for c in divide_cells:
        r = pre( wtt, cell=c )
        d = wtt.divide_cell( c, dscs )
        r["div_desc"] = d
        post( wtt, r )
        l.append( d )
    return l