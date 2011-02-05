#!/usr/bin/env python
"""This is the file demonstrating how to load WT2D structure and  display it using mayavi framework.
:todo:
    Nothing.
:bug:
    None known.
:organization:
    Humboldt University"""

# Module documentation variables:
__authors__="""Szymon Stoma"""
__contact__="<Your contact>"
__license__="Cecill-C"
__date__=""
__version__="0.1"
__docformat__= "restructuredtext en"

# Working with svn version:
stse_svn_revision = 136

from os.path import join
import os
from matplotlib.pyplot import scatter, legend, show, figure, xlabel, ylabel

from openalea.stse.gui.compartment_viewer import start_gui
from openalea.stse.structures.algo.walled_tissue import calculate_cell_surface, cell_center

if __name__ == '__main__':
    window = start_gui()
    
    # Be sure to have STSE_DIR set pointing to the root of STSE.
    stse_path = os.getenv("STSE_DIR")
    data_dir = "data/11-01-04-1cellTest"
    tissue_filename = "tissue01"
    
    # Proxy to actions.
    a2 = window.actions['file_load_walled_tissue']
    
    # Loading geometry.
    a2.load(join(stse_path, data_dir, tissue_filename))
    
    # Proxy to tissue.
    mesh = window._voronoi_wt

    print "# Example (geometrical properties of the mesh - in pixels):"
    print "  Example cell surface:", calculate_cell_surface(mesh, mesh.cells()[0])
    print "  Example cell center:", cell_center(mesh, mesh.cells()[0])

    # Visualisation setting.
    window._cell_scalars_active = False
    
    