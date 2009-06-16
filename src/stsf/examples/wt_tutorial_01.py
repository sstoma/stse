#!/usr/bin/env python

"""Tutorial demonstrating creation of one of the STSF compartment stucture: WalledTissue

 

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
__date__="04/2009"
__version__="0.1"
__docformat__= "restructuredtext en"
__revision__="$Id$"

from openalea.stse.structures.walled_tissue import WalledTissue
from openalea.stse.structures.walled_tissue_const import WalledTissueConst
from openalea.stse.structures.algo.walled_tissue import create
from openalea.plantgl.math import Vector3

# we define the set of settings for a tissue
wtc = WalledTissueConst( name = "Tissue01")
# we declare the set of properties for every cell i.e.
# every cell will have P1 property which will be initialized
# by default to 0. the cell properties can be reached by:
# wt.cell_property( cell_id ) where wt is an instance of
# WalledTissue
# Similar properties can be defined for wv, wv_edges, cell_edges, tissue.
wtc.cell_properties = { "P1" : 0. }
wtc.tissue_properties = { "P1" : "testProperty" }

# we create an empty tissue
wt = WalledTissue( const = wtc )

# we initialize the tissue by specifing two cells
# Please look at: help(create)
# Note: to understand this example geometry it is recomended to draw the cells
# first we specify cell corners and their geometry using the following mapping
wv2pos={
    1: Vector3(1., 1., 0),
    2: Vector3(-1., 1., 0),
    3: Vector3(-1., -1., 0),
    4: Vector3(1., -1., 0),
    5: Vector3(2., -1., 0),
    6: Vector3(2., 1., 0),
}
# second we specify cell shape of all cells
# it is important to note that the lists of vertices are ordered
cell2wv_list={
    1: [1,2,3,4],
    2: [1,4,5,6],
}
create(wt, wv2pos=wv2pos, cell2wv_list=cell2wv_list)

## sample cell inspection
from openalea.stse.structures.algo.walled_tissue import investigate_cell
investigate_cell(wt, 1)

## sample visualization using pylab
from openalea.stse.visu.walled_tissue_pylab import show_cells_with_wvs
show_cells_with_wvs(wt, True)


