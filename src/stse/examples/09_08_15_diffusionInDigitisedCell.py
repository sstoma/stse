#!/usr/bin/env python
"""Example: diffusion in a digitized cell.

<Long description of the module functionality.>

:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    INRIA

"""
# Module documentation variables:
__authors__="""<Your name>    
"""
__contact__="<Your contact>"
__license__="Cecill-C"
__date__="<Timestamp>"
__version__="0.1"
__docformat__= "restructuredtext en"
__svn_revision__= "211"
__run_command__ = """
ipython -wthread
(when shell starts use 'run file_name')
open an background image (go to $STSE_DATA/data/data/09-08-14-prostateCancerCell/ProstateCancerCell.png)
open a saved tissue:  $STSE_DATA/data/data/09-08-14-prostateCancerCell/initial_tissue_with_membranes
change a substance concentation using GUI
run simulation of diffusion:
da = DiffusionAction(window=window)
da.stable_step()
"""



from pyface.api import GUI
from vtk.util import colors
from tvtk.api import tvtk
from traits.api import  Instance, HasTraits, Range, \
    on_trait_change, Color, HTML, Enum, Tuple, Int, Bool, Array, Float, Any, Str
from traitsui.api import View, Item, VGroup,  Tabbed, \
    HSplit, InstanceEditor
from numpy import array
import numpy as np

import scipy
import scipy.integrate.odepack

from openalea.stse.gui.compartment_editor import VoronoiCenterVisRep, \
    default_voronoi_factory
from openalea.stse.gui.compartment_viewer import CompartmentViewerWindow
from openalea.stse.gui.compartment_editor import default_voronoi_factory, CompartmentEditorWindow

from openalea.stse.structures.algo.walled_tissue import calculate_cell_surface,\
    calculate_wall_length, cell_edge2wv_edge, cell_centers
from openalea.stse.io.walled_tissue.native_representation import \
    write_walled_tissue, read_walled_tissue

from openalea.plantgl.all import norm

import copy

class VoronoiCenterVisRepCancerCell(VoronoiCenterVisRep):
    """Represents the cell center of a cell.
    """
    cell_center_color = Color()
    cell_type = Enum("outside","cytoplasm","outside_membrane", \
                     "internal_membrane", "vakuole", "kernel")
    A = Range(0,1.)
    A_signal_source = Bool(False)
    A_receptor = Bool(False)
    B = Range(0,1.)

    
    def __init__(self, center=(0, 0, 0), radius=0.1, resolution=16,
                     color=colors.white, opacity=1.0, **kwargs):
        """ Creates a sphere and returns the actor. """
        super(VoronoiCenterVisRep, self).__init__( **kwargs )
        source = tvtk.SphereSource(center=center, radius=radius,
                                   theta_resolution=resolution,
                                   phi_resolution=resolution)
        self.mapper = tvtk.PolyDataMapper(input=source.output)
        self.property = tvtk.Property(opacity=opacity, color=color)
        self.voronoi_center=array(3)
        if kwargs.has_key("cell_type"):
            self.cell_type = kwargs["cell_type"]
            self.change_cell_center_color()
    
    def default_traits_view( self ):    
        view = View(
            Item("cell_id", style='readonly'),
            Item("cell_type",style='simple'),
            Item("A",style='simple'),
            Item("A_signal_source",style='simple'),
            Item("A_receptor", style='simple'),
            Item("B", style='simple'),
        )
        return view
    
    @on_trait_change('cell_type')
    def change_cell_center_color(self):
        c = self.cell_center_color
        if self.cell_type == "cytoplasm":
            self.property.color = colors.blue
        elif self.cell_type == "outside_membrane":
            self.property.color = colors.red
        elif self.cell_type == "internal_membrane":
            self.property.color = colors.orange
        elif self.cell_type == "outside":
            self.property.color = colors.white
        elif self.cell_type == "kernel":
            self.property.color = colors.black
        elif self.cell_type == "vakuole":
            self.property.color = colors.green

cell_properties = {
    'cell_type': 'cytoplasm',
    'A': 0.,
    'B': 0.,
    'A_signal_source': False,
    'A_receptor': False,
}

def voronoi_factory( center=(0, 0, 0), radius=0.1, resolution=16,
                     color=colors.white, opacity=1.0, **kwargs):
    """Used to generate voronoi centers.
    """
    return VoronoiCenterVisRepCancerCell( center=center, radius=radius, resolution=resolution,
                     color=color, opacity=opacity, **kwargs )    


def start_editor(  ):
    """Starts compartment editor adjusted to cancer cell.

    """
    # Create and open an application window.
    window = CompartmentEditorWindow( voronoi_factory=voronoi_factory, \
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
    window = start_editor()
    #window = start_viewer()
    #da = DiffusionAction(window=window)
    