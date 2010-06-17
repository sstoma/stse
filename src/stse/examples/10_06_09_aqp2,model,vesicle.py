__doc__ = """This is the file for test aqp simulation in a cell
"""

# working with svn version:
stse_svn_revision = 0

from openalea.stse.gui.compartment_viewer import start_gui
from openalea.stse.structures.algo.walled_tissue import avg_cell_property

    


from enthought.pyface.api import GUI
from vtk.util import colors
from enthought.tvtk.api import tvtk
from enthought.traits.api import  Instance, HasTraits, Range, \
    on_trait_change, Color, HTML, Enum, Tuple, Int, Bool, Array, Float, Any, Str
from enthought.traits.ui.api import View, Item, VGroup,  Tabbed, \
    HSplit, InstanceEditor
from numpy import array
import numpy as np
import os

import scipy
import scipy.integrate.odepack

from openalea.stse.gui.compartment_editor import ExampleWindow, VoronoiCenterVisRep, \
    default_voronoi_factory
from openalea.stse.gui.compartment_viewer import CompartmentViewerWindow
from openalea.stse.gui.compartment_editor import default_voronoi_factory

from openalea.stse.structures.algo.walled_tissue import calculate_cell_surface,\
    calculate_wall_length, cell_edge2wv_edge, cell_centers
from openalea.stse.io.walled_tissue.native_representation import \
    write_walled_tissue, read_walled_tissue

from openalea.plantgl.all import norm

import copy


def start_editor(  ):
    """Starts compartment editor adjusted to cancer cell.

    """
    # Create and open an application window.
    window = ExampleWindow( voronoi_factory=voronoi_factory, \
        cell_properties=cell_properties)
    window.edit_traits()
    window.do()
    GUI().start_event_loop()
    return window

def start_viewer(  ):
    """Starts compartment editor adjusted to cancer cell.

    """
    # Create and open an application window.
    window = CompartmentViewerWindow( voronoi_factory=voronoi_factory, \
        cell_properties=cell_properties)
    window.edit_traits()
    window.do()
    GUI().start_event_loop()
    return window


class DiffusionAction:
    """Diffusion of a substance A in a WalledTissue.
    """

    def __init__(self, window = None):
        self.t = 0.
        self.h = 1.
        self.c_change = -np.inf #acceptable change could not be smaller to classifie as error.
        self.c_max_steps = 2000 #maximum number of steps
        
                
        self.c_alpha = 0.1 #creation
        self.c_gamma = 100. #diffusion

        
        self.rtol = 0.0001
        self.atol = 0.0001
        
        #self.c_initial_A_value=self.c_alpha/self.c_beta
        
        self.capture_period = 10
        self.frame = 0
        self._last_capture_time = self.t
        
        self.window = window
        self.wt = window._voronoi_wt
        self.wt.init_tissue_property("time", "0.")

        self.wv_edge_area = {}
        self.cell_volume = {}
        self.cell_distance = {}
        
        self.prepare_geometry()

    def prepare_geometry( self ):
        cc = cell_centers( self.wt )
        for i in self.wt.cells():
            self.cell_volume[ i ] = calculate_cell_surface( self.wt, i)
            for j in self.wt.cell_neighbors( i ):
                self.wv_edge_area[ (i,j) ] = calculate_wall_length( self.wt, \
                    cell_edge2wv_edge(self.wt, (i,j) ))
                self.cell_distance[ (i, j) ] = norm( cc[ i ] - cc[ j ] )
        

    def A( self, cell, value=None ):
        return self.wt.cell_property( cell, "A", value=value)
    

    def apply( self ):
        self.stable_step( )
         
    def stable_step( self ):
        t = self.wt
        self.prepare_sys_map()
        stable=False
        i=0
        while not stable and i < self.c_max_steps:
            print " #: physiology A diffusion: loop=", i, " time=",self.t
            i+=1
            res= scipy.integrate.odepack.odeint( self.f, self.prepare_x0(), [self.t, self.t+self.h],rtol=self.rtol, atol=self.atol)
            self.t += self.h                
            stable = self.rate_error( res[0], res[1])
            self.update( res[1] )
            if self.t > self._last_capture_time + self.capture_period:
                self._last_capture_time = self.t
                self.window.display_tissue_scalar_properties(property="A")
                self.window.scene_model.save_png("%.4d.png"%self.frame)
                t.tissue_property("time", self.t)
                saved_tissue = write_walled_tissue( tissue=t, name="%.4d"%self.frame, desc="Diffusion in a cell: step"+str(self.frame) )
                self.frame+=1

        
    def update( self, x ):
        t = self.wt
        for i in t.cells():
            t0 = x[ self.cell2sys[ i ] ]
            t0 = max(0,t0)
            self.A( cell=i, value= t0)

    def rate_error( self, xn, xnprim ):
        t = True
        max = -float("infinity")
        for i in range( len( self.wt.cells() )):
            if abs( xn[i] - xnprim[i] ) > max:
                max=abs( xn[i] - xnprim[i] )
            if self.c_change < abs( xn[i] - xnprim[i] ):
                t=False 
        print " #: errror =  ", max# abs( xn[i] - xnprim[i] )
        return t

    def prepare_x0( self ):
        x0 = []
        t = self.wt
        for x in range( len(t.cells()) ):
            x0.append(0)
        for i in t.cells():
            x0[ self.cell2sys[ i ] ] = self.A( i )
        return x0

    def prepare_sys_map( self ):
        self.cell2sys = {}
        t = self.wt
        ind = 0
        for i in t.cells():
            self.cell2sys[ i ] = ind
            ind += 1
        
        
    def f( self, x, t ):

        def D( (i, j), t, x):
            return self.wv_edge_area[(i,j)]*(A(i,t,x)-A(j,t,x))/(self.cell_volume[i]*self.cell_distance[(i,j)])
        
        def A( cid, t, x ):
            return x[ self.cell2sys[ cid ] ]
        
        t = self.wt
        x2 = np.zeros_like( x )
        for i in t.cells():
            ct = t.cell_property( cell=i, property= "cell_type" )
            if ct == "cytoplasm" or ct == "kernel":
                if ct == "kernel":
                    x2[ self.cell2sys[ i ] ] += self.c_alpha #* self.i_A_signal_source( i )
                for n in t.cell_neighbors( cell=i ):
                    if t.cell_property( cell=n, property= "cell_type" ) != "internal_membrane":
                        x2[ self.cell2sys[ i ] ] += self.c_gamma*D((n,i),t,x)
        return x2
            
    def i_A_signal_source( self, cell ):
        t = self.wt
        if t.cell_property( cell=cell, property= "cell_type" ) == "kernel":
            return 1.
        return 0.

        
    #def init_A(self):
    #    t = self.wt
    #    for c in t.cells():
    #        self.A(cell= c, value= self.c_initial_A_value ) #+random.random() )

    def simulate( wt, steps ):
        da = DiffusionAction( window = window )

if __name__ == '__main__':
    window = start_gui()
    #exchange it with your data pointing to schmoo example
    data_dir ="/home/sstoma/svn/stse-data/trunk/data/10-06-09-aqp,model,vesicle,position"
        # proxy to actions
    a1 = window.actions['file_load_background_image']
    a2 = window.actions['file_load_walled_tissue']
    a3 = window.actions[ "actions_define_cell_types" ]
    a4 = window.actions[ "actions_calculate_average_expression" ]
    a5 = window.actions[ 'file_save_walled_tissue' ]
    
    # loading geometry
    a1.load_image( data_dir+"/scene-0.png" )

    