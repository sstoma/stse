#!/usr/bin/env python
"""This is the file demonstrating how to make phyllotaxis simulation using STSE. The algorithm of phyllotaxis: Hoffmeisters rule.
:todo:
    Nothing.
:bug:
    None known.
:organization:
    INRIA"""

# Module documentation variables:
__authors__="""Szymon Stoma"""
__contact__="<Your contact>"
__license__="Cecill-C"
__date__=""
__version__="0.1"
__docformat__= "restructuredtext en"

# Working with svn version:
__svn_revision__= "211"
__run_command__ = "ipython -wthread (when shell starts use 'run file_name')"

from os.path import join
import os
from matplotlib.pyplot import scatter, legend, show, figure, xlabel, ylabel
import math

import openalea.plantgl.all as pgl

from openalea.stse.gui.compartment_viewer import start_gui
from openalea.stse.structures.algo.walled_tissue import calculate_cell_surface, cell_center
import openalea.stse.growth.walled_tissue as growth
from openalea.stse.growth.remove_cell_strategy import RemoveBasedOnDistance



    
    
class Phyllotaxis:    
    time = 1
    prim_direction_history = [pgl.Vector3(1,0,0)]
    prim_time_history = [0]

    
    def __init__(self, window, c_ring_property, c_prim_property ):
        self.window = window
        self.center = center
        self.c_ring_property = c_ring_property
        self.c_prim_property = c_prim_property
    def execute( self ):
        print " !: Not implemented"
        


class HoffmeisterPhyllotaxis(Phyllotaxis):
    c_phyllotaxis_period = 15
    c_angle = pgl.axisRotation(pgl.Vector3(0,0,1), math.pi*(3-math.sqrt(5)))

    def execute( self ):
        if self.time % self.c_phyllotaxis_period == 0:
            print " #: searching for prim..."
            self.create_prim()
        self.time += 1

    def create_prim( self ):        
        # find prim direction
        last = self.prim_direction_history[-1]
        new = self.c_angle * last
        
        mesh = self.window._voronoi_wt
        min_angle = 2*math.pi
        min_cell = -1
        for i in mesh.cells():
            # cell is in compt ring
            if mesh.cell_property(i, self.c_ring_property) == 1:
                diff = pgl.angle(new, cell_center(mesh, i))
                if diff < min_angle:
                    min_angle = diff
                    min_cell = i
        
        if min_cell != -1:
            self.prim_time_history.append( self.time )
            self.prim_direction_history.append( cell_center(mesh, min_cell) )
            mesh.cell_property(min_cell, self.c_prim_property, 1)
        else: print " !: problem - prim not found..."
        
        
class Simulation:
    c_central_ring_min = 8
    c_central_ring_max = 14 #10 to have too small central zone / 14 normal golden angle
    c_cell_size = 15
    c_steps = 500
    
    c_prim_property = "custom_cell_property1"
    c_ring_property = "custom_cell_property2"
    c_visualisation_property = "custom_cell_property5"
    
    removed_prim_direction_history = []
    removed_prim_time_history = []
    
    def __init__(self, window, center):
        self.window = window
        self.center = center
        self.removeStrategy = RemoveBasedOnDistance( system = window._voronoi_wt, distance = 20)
        self.phyllotaxis = HoffmeisterPhyllotaxis( window = window, c_ring_property=self.c_ring_property, c_prim_property=self.c_prim_property )

    
    def central_ring(self):
        mesh = self.window._voronoi_wt
        for i in mesh.cells():
            c =cell_center( mesh, i)
            if pgl.norm(self.center - c) < self.c_central_ring_max and pgl.norm(self.center - c ) > self.c_central_ring_min:
                mesh.cell_property(i, self.c_ring_property, 1)
            else:
                mesh.cell_property(i, self.c_ring_property, 0)
                    
    
    def mark_cells( self ):
        mesh = self.window._voronoi_wt
        for i in mesh.cells():
            # clean disp prop
            mesh.cell_property(i, self.c_visualisation_property, 0.)
            # set disp prop
            if mesh.cell_property(i, self.c_ring_property) == 1:
                mesh.cell_property(i, self.c_visualisation_property, 0.1)
            if mesh.cell_property(i, self.c_prim_property):
                mesh.cell_property(i, self.c_visualisation_property, 1)
    
    def register_removed_primordia( self, loptr ):
        mesh = self.window._voronoi_wt
        for c in loptr:
            if mesh.cell_property(c, self.c_prim_property) != 0:
                self.removed_prim_direction_history.append(cell_center(mesh, c))
                self.removed_prim_time_history.append(self.phyllotaxis.time)
        
    def execute( self ):
        def pre_fun( wt, cell ):
            # before the division
            mesh = wt
            # store properties
            p = {}
            for (k,v) in mesh.const.cell_properties.items():
                p[k]=wt.cell_property(cell, k)
            return p
                
        def post_fun( wt, pre_res, div_res ):
            # post division
            mesh = wt
            a = div_res[2][0]["added_cell1"]
            b = div_res[2][0]["added_cell2"]
            for (k, v) in pre_res.items():
                if k == self.c_prim_property:
                    mesh.cell_property(a, k, v)
                    mesh.cell_property(b, k, 0)
                else:
                    mesh.cell_property(a, k, v)
                    mesh.cell_property(b, k, v)

        mesh = self.window._voronoi_wt    
        i = 0
        while i < self.c_steps:
            # step of tissue growth
            growth.tgs_linear_growth (mesh, self.center, 1, 0.03)
            
            # select cells for division based on surface
            # divide all selected cells according to division strategy
            growth.chd_surface(mesh, self.c_cell_size, growth.dcs_shortest_wall_with_geometric_shrinking, pre_fun=pre_fun, post_fun=post_fun )
            
            loctr = self.removeStrategy.cells_to_remove()
            self.register_removed_primordia( loctr )
            for c in loctr:
                mesh.remove_cell(c)
            
            # modify a zone of prim creation
            self.central_ring()
            
            # phyllotaxis
            self.phyllotaxis.execute()
            
            # update the view
            i = i + 1
            self.mark_cells()
            self.window.update_properties_from_wt2d_to_pm( color = (0, 255, 0) )
            self.window.scene_model.save_png("res/%.4d.png"%self.phyllotaxis.time)

    def make_plot(self):
        import pylab
        x = []
        t = range(len(self.phyllotaxis.prim_direction_history))
        for i in t[:-1]:
            x.append( pgl.angle(self.phyllotaxis.prim_direction_history[i], self.phyllotaxis.prim_direction_history[i-1]) )
        x2 = []
        t2 = range(len(self.removed_prim_direction_history))
        for i in t2[:-1]:
            x2.append( pgl.angle(self.removed_prim_direction_history[i], self.removed_prim_direction_history[i-1]) )

        pylab.plot( t[:-1], x, 'x-', t2[:-1], x2, 'o-', t[:-1], (len(t)-1)*[math.pi*(3-math.sqrt(5))], '--'  )
        pylab.legend(["Angle@CZ", "Angle@Exit", "Golden angle"])
        pylab.xlabel("Primordium number")
        pylab.ylabel("Divergance angle")
        pylab.show()
        #

if __name__ == '__main__':
    window = start_gui()
    
    # Be sure to have STSE_DIR set pointing to the root of STSE.
    stse_path = os.getenv("STSE_DIR")
    data_dir = "data/11-01-04-1cellTest"
    tissue_filename = "tissue01"
    
    # Proxy to actions.
    a2 = window.actions['file_load_walled_tissue']
    
    # Loading geometry.
    a2._load(join(stse_path, data_dir, tissue_filename))
    
    # Proxy to tissue.
    mesh = window._voronoi_wt

    print "# Example (geometrical properties of the mesh - in pixels):"
    print "  Example cell surface:", calculate_cell_surface(mesh, mesh.cells()[0])
    print "  Example cell center:", cell_center(mesh, mesh.cells()[0])

    # Visualisation setting.
    window._cell_scalars_active = False
    
    c = pgl.Vector3()
    for i in mesh.wvs():
        c += mesh.wv_pos(i)
    c = c / len(mesh.wvs())
    for i in mesh.wvs():
        mesh.wv_pos(i, mesh.wv_pos(i)-c)


    
    #setting center for growth algorithm
    center = cell_center(mesh, mesh.cells()[0])

    # cleaning voronois
    window.remove_all_voronoi_centers()

    #subdividing first mesh
    for i in range(50):
        growth.chd_surface(mesh, 20, growth.dcs_shortest_wall_with_geometric_shrinking )
    
    window.update_properties_from_wt2d_to_pm()
    
    s = Simulation( window, center)
    
    window._cell_scalars_active_name = s.c_visualisation_property
    window._cell_scalars_dynamic = False
    window._cell_scalars_active = True
    window._cell_scalars_range[1]=1
    #s.execute()

