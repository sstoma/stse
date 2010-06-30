__doc__ = """This is the file demonstrating how to perform a dynamic simulation with  STSE.
"""

# working with svn version:
stse_svn_revision = 54

from openalea.stse.gui.compartment_viewer import start_gui
from openalea.stse.structures.algo.walled_tissue import avg_cell_property
from openalea.stse.structures.algo.walled_tissue import calculate_cell_surface,\
    calculate_wall_length, cell_edge2wv_edge, cell_centers

import sys
import copy
import time
import os.path
import os

# for simulation
from numpy import array
import numpy as np
import scipy
import scipy.integrate.odepack
from openalea.plantgl.all import norm

import copy


class DiffusionAction:
    """Diffusion of a substance A in a WalledTissue.
    """

    def __init__(self, window = None):
        self.t = 0.
        self.h = 1.
        self.c_change = -np.inf #acceptable change could not be smaller to classifie as error.
        self.c_max_steps = 2000 #maximum number of steps
        
                
        self.c_alpha = 0.01 #creation of FUS3
        self.c_beta = 0.001 #decay of FUS3
        self.c_gamma = 50. # FUS3 diffusion const.

        
        self.rtol = 0.0001
        self.atol = 0.0001
        
        #self.c_initial_A_value=self.c_alpha/self.c_beta
        
        self.capture_period = 10.
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

    def FUS3( self, cell, value=None ):
        return self.wt.cell_property( cell, "custom_cell_property1", value=value)
    

    def apply( self ):
        self.stable_step( )
         
    def stable_step( self ):
        t = self.wt
        self.prepare_sys_map()
        stable=False
        i=0
        while not stable and i < self.c_max_steps:
            print " #: physiology FUS3 diffusion: loop=", i, " time=",self.t
            i+=1
            res= scipy.integrate.odepack.odeint( self.f, self.prepare_x0(), [self.t, self.t+self.h],rtol=self.rtol, atol=self.atol)
            self.t += self.h                
            stable = self.rate_error( res[0], res[1])
            self.update( res[1] )
            if self.t > self._last_capture_time + self.capture_period:
                self._last_capture_time = self.t
                self.window.display_tissue_scalar_properties(property=self.window._cell_scalars_active_name)
                self.window.scene_model.save_png("%.4d.png"%self.frame)
                t.tissue_property("time", self.t)
                #saved_tissue = write_walled_tissue( tissue=t, name="%.4d"%self.frame, desc="Step"+str(self.frame) )
                self.frame+=1

        
    def update( self, x ):
        t = self.wt
        for i in t.cells():
            t0 = x[ self.FUS32sys[ i ] ]
            t0 = max(0,t0)
            self.FUS3( cell=i, value= t0)
        

    def rate_error( self, xn, xnprim ):
        t = True
        max = -float("infinity")
        for i in range( len( self.wt.cells() )):
            if abs( xn[i] - xnprim[i] ) > max:
                max=abs( xn[i] - xnprim[i] )
            if self.c_change < abs( xn[i] - xnprim[i] ):
                t=False 
        print " #: error =  ", max# abs( xn[i] - xnprim[i] )
        return t

    def prepare_x0( self ):
        x0 = []
        t = self.wt
        for x in range( len(t.cells()) ):
            x0.append(0)
        
        for i in t.cells():
            x0[ self.FUS32sys[ i ] ] = self.FUS3( i )
        return x0

    def prepare_sys_map( self ):
        self.FUS32sys = {}
        t = self.wt
        ind = 0
        for i in t.cells():
            self.FUS32sys[ i ] = ind
            ind += 1
        
        
    def f( self, x, t ):

        def D( (i, j), t, x):
            return self.wv_edge_area[(i,j)]*(FUS3(i,t,x)-FUS3(j,t,x))/(self.cell_volume[i]*self.cell_distance[(i,j)])
        
        def FUS3( cid, t, x ):
            return x[ self.FUS32sys[ cid ] ]

        
        t = self.wt
        x2 = np.zeros_like( x )
        for i in t.cells():
            ct = t.cell_property( cell=i, property= "cell_type" )
            
            # diffusion of FUS3 inside a cell
            if ct == "B" or ct == "F":
                for n in t.cell_neighbors( cell=i ):
                    nct =  t.cell_property( cell=n, property= "cell_type" )
                    if nct != "A" and nct != "C" and nct != "D" and nct != "E":
                        x2[ self.FUS32sys[ i ] ] += self.c_gamma*D((n,i),t,x)
                        
            # creation of FUS3 in the schmoo tip
            if ct == "F":
                x2[ self.FUS32sys[ i ] ] += self.c_alpha

            # decay of FUS3 inside a cell
            if ct == "B" or ct == "F":
                x2[ self.FUS32sys[ i ] ] += - self.c_beta*FUS3(i, t, x)
        return x2

if __name__ == '__main__':

    
    window = start_gui()
    #exchange it with your data pointing to schmoo example
    # please adjust the path to access the files from data directory of stsf
    # project
    stse_path = os.getenv("STSE_DIR")
    data_dir =stse_path+"/data/10-04-27-schmoo"
    expression_data_files = [
        "schmoo-0",
    ]
    expression_channels2cell_types  = {
        '0': 'B',
        '1': 'C',
        '2': 'D',
        '3': 'E',
        '4': 'F',       
    }
    cell_type2biological_name ={
        'A': 'outside',
        'B': 'cytoplasm',
        'C': 'nucleus',
        'D': 'cell_membrane',
        'E': 'nuceus_membrane',
        'F': 'schmoo_tip',
    }
    
    # proxy to actions
    a1 = window.actions['file_load_background_image']
    a2 = window.actions['file_load_walled_tissue']
    #a3 = window.actions[ "actions_define_cell_types" ]
    #a4 = window.actions[ "actions_calculate_average_expression" ]
    a5 = window.actions[ 'file_save_walled_tissue' ]
    
    # loading geometry
    a1.load_image( data_dir+"/"+expression_data_files[ 0 ]+'0'+".png" )
    a2.load( data_dir+"/"+expression_data_files[ 0 ]+"-auto" )
    
    # proxy
    mesh = window._voronoi_wt
    
    # clearing the FUS3 readout
    for i in mesh.cells():
        mesh.cell_property(i,  "custom_cell_property1", 0.)

    
    window._cell_scalars_active_name = "custom_cell_property1"
    window._cell_scalars_dynamic=False
    window._cell_scalars_active = True    
    window._cell_scalars_range[1]=0.065
    
    da = DiffusionAction( window = window )
