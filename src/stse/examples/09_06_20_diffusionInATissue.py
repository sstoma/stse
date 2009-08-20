#!/usr/bin/env python
"""Diffusion on a tissue

<Long description of the module functionality.>

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
__date__="Fri Jun 19 16:02:57 CEST 2009"
__version__="0.1"
__docformat__= "restructuredtext en"
__svn_revision__= "15"

from openalea.stse.io.walled_tissue.dat_representation import read_dat2walled_tissue, read_link_file
import openalea.plantgl.all as pgl
import openalea.plantgl.ext.all as pd
from lib_09_06_06_influenceZones import vis, display_config 
from openalea.stse.io.walled_tissue.dat_config_processing import read_dat_tissue_directory, Config
from openalea.stse.visu.walled_tissue_pgl import visualisation_pgl_2D_varried_membrane_thickness, f_property2scalar, f_cell_marking, f_properties2material, f_weighted_property2material
from openalea.stse.structures.algo.walled_tissue import wv_edge2cell_edge
import scipy
import scipy.integrate.odepack
import copy

class DiffusionAction:
    """Diffusion of a substance A in a WalledTissue.
    """

    def __init__(self, tissue_system = None):
        self.t = 0
        self.h = 10
        self.c_change = 0.0001 #acceptable change could not be smaller to classifie as error.
        self.c_max_steps = 100 #maximum number of steps
        
        self.local_evacuation_properties = ["P1","P2","P3","P4","P5","P6",]
                
        self.c_alpha = 0.01 #creation
        self.c_beta = 0.01 #destruction
        self.c_gamma = 0.05#diffusion
        self.c_kappa = 0.05  #diffusion
        
        self.c_epsilon=0.01 #centre evacuate
        self.c_delta = 0.01 #prim evacuate


        self.c_initial_A_value=self.c_alpha/self.c_beta
        
        self.tissue_system = tissue_system


    def A( self, cell, value=None ):
        return self.tissue_system.tissue.cell_property( cell, "A", value=value)
    

    def apply( self ):
        self.stable_step( )
         
    def stable_step( self ):
        t = self.tissue_system.tissue
        self.prepare_sys_map()
        stable=False
        i=0
        while not stable and i < self.c_max_steps:
            print " #: physiology A diffusion: loop=", i, " time=",self.t
            i+=1
            res= scipy.integrate.odepack.odeint( self.f, self.prepare_x0(), [self.t, self.t+self.h],rtol=0.01, atol=0.001, full_output = 1 )
            self.t += self.h                
            stable = self.rate_error( res[0], res[1])
            self.update( res[1] )

        
    def update( self, x ):
        t = self.tissue_system.tissue
        for i in t.cells():
            t0 = x[ self.cell2sys[ i ] ]
            t0 = max(0,t0)
            self.A( cell=i, value= t0)

    def rate_error( self, xn, xnprim ):
        t = True
        max = -float("infinity")
        for i in range( len( self.tissue_system.tissue.cells() )):
            if abs( xn[i] - xnprim[i] ) > max:
                max=abs( xn[i] - xnprim[i] )
            if self.c_change < abs( xn[i] - xnprim[i] ):
                t=False 
        print " #: errror =  ", max# abs( xn[i] - xnprim[i] )
        return t

    def prepare_x0( self ):
        x0 = []
        t = self.tissue_system.tissue
        for x in range( len(t.cells()) ):
            x0.append(0)
        for i in t.cells():
            x0[ self.cell2sys[ i ] ] = self.A( i )
        return x0

    def prepare_sys_map( self ):
        self.cell2sys = {}
        t = self.tissue_system.tissue
        ind = 0
        for i in t.cells():
            self.cell2sys[ i ] = ind
            ind += 1
        
        
    def f( self, x, t ):

        def D( (i, j), t, x):
            return (A(i,t,x)-A(j,t,x))
        
        def A( cid, t, x ):
            return x[ self.cell2sys[ cid ] ]
        
        t = self.tissue_system.tissue
        x2 = copy.copy( x )
        for i in t.cells():
            x2[ self.cell2sys[ i ] ] = self.c_alpha - A(i,t,x)*(self.c_beta+self.c_epsilon*self.i_center_evacuate( i ))#OK
            if self.i_local_evacuate( i ):
                x2[ self.cell2sys[ i ] ] -= self.c_delta*A(i,t,x)
            for n in t.cell_neighbors( cell=i ):
                x2[ self.cell2sys[ i ] ] += self.c_gamma*D((n,i),t,x)
        return x2
            
    def i_local_evacuate( self, cell ):
        t = self.tissue_system.tissue
        for i in self.local_evacuation_properties:
            if t.cell_property( cell=cell, property= i ):
                return 1
        return 0
        
    def i_center_evacuate( self, cell ):
        t = self.tissue_system.tissue
        if t.cell_property( cell=cell, property="CZ") > 0:
            return 1
        else:
            return 0
        
    def init_A(self):
        t = self.tissue_system.tissue
        for c in t.cells():
            self.A(cell= c, value= self.c_initial_A_value ) #+random.random() )


class TissueSystem:
    """Structure to store different components of tissue-based experiments.
    """
    def __init__( self, wt=None, config=None, phys=[] ):
        """Inits tissue system
        
        <Long description of the function functionality.>
        
        :parameters:
            arg1 : WalledTissue
                Tissue structure
        
        """
        self.tissue = wt
        self.config = config
        self.phys = phys
        self.frame = 0
        self.visualise()
    
    def simulate( self, steps=1 ):
        """<Short description of the function functionality.>
        
        <Long description of the function functionality.>
        """
        for j in range( steps ):
            for i in self.phys:
                i.apply()
            self.visualise()
        
    def visualise( self, save=False, clear=True ):
        """<Short description of the function functionality.>
        
        <Long description of the function functionality.>
        """
        """Displaying of IZ and saving the results.
        """

        if clear: pd.SCENES[ pd.CURRENT_SCENE ].clear()
        pd.instant_update_viewer()
        visualisation_pgl_2D_varried_membrane_thickness( self.tissue,
                                            abs_intercellular_space=0.05,
                                            abs_membrane_space=0.25,
                                            stride=20,
                                            f_membrane_thickness = f_pin( self.tissue ),
                                            f_cell_marking = [f_cell_marking( properties=self.config.cell_regions.keys(), property_true_radius=0.2)], 
                                            #f_material = f_weighted_property2material( property="A", range=(0,1) ),
                                            )        
        pd.instant_update_viewer()
        self.frame += 1
        if save: pgl.Viewer.frameGL.saveImage( config.file_folder+"/"+str(self.frame).zfill(5)+".png" )

def f_pin( wt ):
    """Function returning function which returns the membrane thickness according
    to PIN cell_edge property.
    
    <Long description of the function functionality.>
    
    :parameters:
        wt : `WalledTissue`
            Tissue containing cell data
    :rtype: function
    :return: Function which returns the membrane thickness according
    to PIN cell_edge property.
    """

    def f( cell, edge ):
        try:
            ce = wv_edge2cell_edge( wt, edge )
            if ce[ 1 ] == cell: ce=(ce[1],ce[0])
            #print wt.cell_property( ce[ 0 ], "A") - wt.cell_property(ce[ 0 ], "A" )
            v = min(1., 100.*max( 0., wt.cell_property( ce[ 0 ], "A") - wt.cell_property(ce[ 1 ], "A" ) ) )
        except TypeError:
            v = 0.
        #print v
        return v
    return f

def reset_IZ( wt, c ):
    for i in c.regions2cells:
        for j in wt.cells():
            wt.cell_property(j, i+"_IZ", False)

def compute_A_gradient( wt ):
    for ce in wt.cell_edges():
        wt.directed_cell_edge_property(ce, "PIN", min(1., 100.*max( 0., wt.cell_property( ce[ 0 ], "A") - wt.cell_property(ce[ 1 ], "A" ) ) ) )

def set_computed_influence_zones( wt, config=None, **keys):
    def f( wt, directed_cell_edge ):
        return wt.directed_cell_edge_property( directed_cell_edge, "PIN")
    
    from openalea.stse.structures.algo.walled_tissue_influence_zones import set_property_on_tissue_component
    for i in config.regions2cells:
        #print zones[ i ]
        for j in config.regions2cells[ i ]:
            set_property_on_tissue_component( wt=wt,
                                 cell= j,
                                 f_component=f,
                                 tol=0.1,
                                 property=i+"_IZ",
                                 property_value=1.,
                                 with_neighbors=False,
                                 fill_gaps=False,
                                 additional_vertices=[])
    
path = "/Users/stymek/src/stse/trunk/data/09-06-10-marianne-wt2-diff/"

wt = read_dat_tissue_directory( path +"config.py" )
c = Config( path+"config.py" )
ts = TissueSystem( wt=wt, config=c, phys=[ DiffusionAction() ])
ts.phys[0].tissue_system = ts

#import pickle
#pickle.dump(l, file(c.file_folder+"/"+"A.pro","w"))

#ts.phys[0].init_A()

import pickle
l = pickle.load(file(c.file_folder+"/"+"A.pro","r"))
for i in wt.cells():
    wt.cell_property( i, "A", l[ i ])

#max=0
#for i in wt.cell_edges():
#    m = wt.cell_property( i[0], "A" ) - wt.cell_property( i[1], "A" )
#    if m > max:
#        max = m
#print max
#assert False

reset_IZ( wt, c )
compute_A_gradient( wt )
set_computed_influence_zones( wt, c )
    
ts.visualise()
display_config()

