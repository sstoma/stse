#!/usr/bin/env python
"""This is the file demonstrating how to load WT2D structure and  display it using mayavi framework.

:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    Humboldt University

"""
# Module documentation variables:
__authors__="""Szymon Stoma    
"""
__contact__="<Your contact>"
__license__="Cecill-C"
__date__=""
__version__="0.1"
__docformat__= "restructuredtext en"

# working with svn version:
stse_svn_revision = 136

from os.path import join
import os
from matplotlib.pyplot import scatter, legend, show, figure, xlabel, ylabel

from openalea.stse.gui.compartment_viewer import start_gui
from openalea.stse.structures.algo.walled_tissue import calculate_cell_surface,\
    cell_center
from openalea.stse.structures.algo.walled_tissue import *
from openalea.stse.structures.algo.walled_tissue_dscs import *
from openalea.stse.structures.algo.walled_tissue_cfd import *
    


def tgs_linear_growth (wt2d, center, steps, growth_factor):
	"""Increases the size of cell in defined as paramater number of steps and growth_factor.
	"""
	for steps_counter in range(steps):
		for i in wt2d.wvs():
			wt2d.wv_pos( i, wt2d.wv_pos( i ) - (center -  wt2d.wv_pos( i ) ) * growth_factor )


def scs_surface (wt2d, size):
	"""Returns list of cells which should divide acording to surface rule"""
	to_divide = []
	for c in wt2d.cells():
		if calculate_cell_surface( wt2d, c ) > size:
			to_divide.append( c ) 
	return to_divide
	

def chd_surface(wt2d, max_surface, divide_strategy):
	"""Dividing cells which has higher surface than max_surface"""
	cells_to_divide = scs_surface(wt2d, max_surface)
	if cells_to_divide:
		cell_to_divide_index = wt2d.cells().index(cells_to_divide[0])
		wt2d.divide_cell( wt2d.cells()[ cell_to_divide_index ], divide_strategy )
		
		
def dcs_shortest_wall( wt2d, cell ):
	"""Divide Single Cell Strategy: divides taking the shortest possible wall. TODO explain.
	"""
	shape = wt2d.cell2wvs( cell )
	test_if_division_is_possible( wt2d, shape )
	dshape = shape+shape
	ls = len(shape)
	vmin = float( "infinity" )
	for i in range( ls ): 
		s1t = wt2d.wv_pos( dshape[ i ] )
		t1t = wt2d.wv_pos( dshape[ i+1 ] )
		s2t = wt2d.wv_pos( dshape[ i+ls/2 ] )
		t2t = wt2d.wv_pos( dshape[ i+1+ls/2 ] )
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
	

def test_if_division_is_possible( wt2d, shape ):
	"""Returns True if cell can be divided. Currently the cell can't be divided if it has less than 3 walls. 
	"""
	i = len( shape )
	if i < 3: 
		# TODO drop exception
		print "Skipping division of degenerated cell:", cell
		return False
	return True



if __name__ == '__main__':
    window = start_gui()
    # be sure to have STSE_DIR set pointing to the root of STSE 
    stse_path = os.getenv("STSE_DIR")
    data_dir = "data/11-01-04-1cellTest"
    tissue_filename = "tissue01"
    
    # proxy to actions
    a2 = window.actions['file_load_walled_tissue']
    
    # loading geometry
    a2.load( join( stse_path, data_dir, tissue_filename ) )
    
    # proxy to tissue
    mesh = window._voronoi_wt

    print "# Example (geometrical properties of the mesh - in pixels):"
    print "  Example cell surface:", calculate_cell_surface(mesh, mesh.cells()[0] )
    print "  Example cell center:", cell_center(mesh, mesh.cells()[0] )

    # visualisation setting
    window._cell_scalars_active = False
    mesh = window._voronoi_wt
	
    i = 0
    while i < 50:
        tgs_linear_growth (mesh, cell_center(mesh, mesh.cells()[0] ), 1, 0.01)
        chd_surface(mesh, 200, dcs_shortest_wall)
        i = i + 1
        window.update_vtk_from_voronoi(  )
