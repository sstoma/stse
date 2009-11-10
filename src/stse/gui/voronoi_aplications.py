#!/usr/bin/env python
"""Rutines for compartment editor viewer.

:todo:
    To be revied by somebody skillfull in VTK/TraitsUI/tvtk

:bug:
    None known.
    
:organization:
    INRIA/Humboltd University Berlin

"""
# Module documentation variables:
__authors__="""Szymon Stoma    
"""
__contact__="<Your contact>"
__license__="Cecill-C"
__date__="<Timestamp>"
__version__="0.1"
__docformat__= "restructuredtext en"

# Standard library imports.
# Standard library imports.
import random
import math

# Enthought library imports.
from enthought.pyface.api import FileDialog, DirectoryDialog, GUI, OK, \
    ImageResource
from enthought.pyface.action.api import Action, MenuBarManager, \
    MenuManager, ToolBarManager

from enthought.traits.api import  Instance, HasTraits, Range, \
    on_trait_change, Color, HTML, Enum, Tuple, Int, Bool, Array, Float, Any, Str, Button

from enthought.tvtk.pyface.scene_editor import SceneEditor
from enthought.tvtk.api import tvtk

from enthought.traits.ui.api import View, Item, VGroup,  Tabbed, \
    HSplit, InstanceEditor, HGroup

from enthought.mayavi.tools.mlab_scene_model import MlabSceneModel
from enthought.mayavi.core.ui.mayavi_scene import MayaviScene
from enthought.mayavi import mlab
from enthought.mayavi.sources.vtk_data_source import VTKDataSource
from enthought.mayavi.modules.image_actor import ImageActor

from vtk.util import colors

from numpy import array, zeros, inf

# openalea
from openalea.stse.io.walled_tissue.vtk_representation import \
    walled_tissue2vtkPolyData, synchronize_id_of_wt_and_voronoi, \
    copy_cell_properties_from_voronoi_to_wt, copy_cell_properties_from_wt_to_voronoi
from openalea.stse.structures.walled_tissue import WalledTissue
from openalea.stse.io.walled_tissue.native_representation import \
    write_walled_tissue, read_walled_tissue
from openalea.stse.io.qhull import voronoi_centers_to_edges 
from openalea.stse.io.walled_tissue.qhull_representation import \
    read_qhull2walled_tissue
from openalea.stse.tools.emergency import kill_close_points
from openalea.stse.tools.convex_hull import int_points_in_polygon
from openalea.stse.structures.algo.walled_tissue import \
    calculate_cell_surface

# ---------------------------------------------------- GUI DATASTRUCTURE CLASSES


class VoronoiCenterVisRep(tvtk.Actor):
    """Represents the cell center of a cell.
    """
    cell_id = Int(-1)
    voronoi_center = Any
    was_inf = Bool(False)
    
    def __init__(self, center=(0, 0, 0), radius=0.1, resolution=16,
                     color=colors.white, opacity=1.0, cell_type='', **kwargs):
        """ Creates a sphere and returns the actor. """
        super(VoronoiCenterVisRep, self).__init__( **kwargs )
        source = tvtk.SphereSource(center=center, radius=radius,
                                   theta_resolution=resolution,
                                   phi_resolution=resolution)
        self.mapper = tvtk.PolyDataMapper(input=source.output)
        self.property = tvtk.Property(opacity=opacity, color=color)
    
    def default_traits_view( self ):    
        view = View(
            Item("cell_id", style='readonly'),
        )
        return view
    
    @on_trait_change('cell_id')
    def change_cell_id(self):
        pass
    
def default_voronoi_factory( center=(0, 0, 0), radius=0.1, resolution=16,
                     color=colors.white, opacity=1.0, **kwargs):
    """Used to generate voronoi centers.
    """
    return VoronoiCenterVisRep( center=center, radius=radius, resolution=resolution,
                     color=color, opacity=opacity, **kwargs )
    
class VoronoiCenterVisRepGeneral(VoronoiCenterVisRep):
    """Represents the cell center of a cell.
    """
    cell_center_color = Color()
    cell_type = Enum("A","B","C","D","E")
    custom_cell_property1 = Float(0.)
    custom_cell_property2 = Float(0.)
    custom_cell_property3 = Float(0.)
    custom_cell_property4 = Float(0.)
    custom_cell_property5 = Float(0.)
    
    def __init__(self, center=(0, 0, 0), radius=0.1, resolution=16,
                     color=colors.white, opacity=1.0, **kwargs):
        """ Creates a sphere and returns the actor. """
        super(VoronoiCenterVisRepGeneral, self).__init__( **kwargs )
        source = tvtk.SphereSource(center=center, radius=radius,
                                   theta_resolution=resolution,
                                   phi_resolution=resolution)
        self.mapper = tvtk.PolyDataMapper(input=source.output)
        self.property = tvtk.Property(opacity=opacity, color=color)
        self.voronoi_center=array(3)
        if kwargs.has_key( "cell_type" ):
            self.cell_type = kwargs["cell_type"]
            self.change_cell_center_color()
        
    def default_traits_view( self ):    
        view = View(
            Item("cell_id", style='readonly'),
            #Item("voronoi_center", style='readonly'),
            #Item("was_inf", style='readonly'),
            Item("cell_type",style='simple'),
            Item("custom_cell_property1",style='simple'),
            Item("custom_cell_property2",style='simple'),
            Item("custom_cell_property3",style='simple'),
            Item("custom_cell_property4",style='simple'),
            Item("custom_cell_property5",style='simple'),
        )
        return view
    
    @on_trait_change('cell_type')
    def change_cell_center_color(self):
        c = self.cell_center_color
        if self.cell_type == "A":
            self.property.color = colors.white
        elif self.cell_type == "B":
            self.property.color = colors.red
        elif self.cell_type == "C":
            self.property.color = colors.blue
        elif self.cell_type == "D":
            self.property.color = colors.black
        elif self.cell_type == "E":
            self.property.color = colors.pink    

def general_voronoi_factory( center=(0, 0, 0), radius=0.1, resolution=16,
                     color=colors.white, opacity=1.0, **kwargs):
    """Used to generate voronoi centers.
    """
    return VoronoiCenterVisRepGeneral( center=center, radius=radius, resolution=resolution,
                     color=color, opacity=opacity, **kwargs )
    
# ---------------------------------------------------- CUSTOMIZATION GUI CLASSES

    
class MyScene(MlabSceneModel):
    """Defined to get rid of default toolbar.
    """
    ## uncoment the line below to remove default view toolbar 
    #actions = []
    pass


class MyAction(Action):
    """Defined since the Actions in the toolbar/menu require some fields which
    are not defined in Action.
    """
    # why Action does not contain these variables??
    defined_when = ""
    enabled_when = ""
    checked_when = ""
    no_conf_string = Str("No configuration options")
    perform_btn = Button( label='Execute' )
    
    def __init__(self, **kwargs):
        """Init"""
        super(MyAction, self).__init__( **kwargs )
        self._application = kwargs['parent']
        
    def perform(self):
        """
        Adds action GUI to the control panel 
        """
        a = self._application
        a._selected_action = self
        
    def default_traits_view( self ):
        """Description of default view.
        """
        view = View(
            Item(
                'no_conf_string',
                show_label=False,
                style='readonly',
            ),
            Item(
                "perform_btn",
                show_label = False,
            ),
        )
        return view
    
    def _perform_btn_fired( self ):
        """Runs default action.
        """
        self.perform_calc()

    def perform_calc( self ):
        """Runs default action.
        """
        print " !: Perform not defined.."
 
general_cell_properties = {
        'custom_cell_property1': 0.,
        'custom_cell_property2': 0.,
        'custom_cell_property3': 0.,
        'custom_cell_property4': 0.,
        'custom_cell_property5': 0.,
        'cell_type': 'A',
}


class CompartmentWindow( HasTraits ):
    """
<h1>Interactions</h1>
<h2>Specific interactions:</h2>
These interactions are redefined for this application:
<ul>
<li>'z': Adds a voronoi center in the place of mouse cursor.
<li>'x': Removes a voronoi center in the place of mouse cursor.
<li>'c': Removes all voronoi centers.
<li>'p': Changes the selection (depicted with white wireframe sphere) to the voronoi center  under the mouse cursor. If no voronoi center is under the mouse cursor selection remains unchanged.
<li>To move a voronoi center, select it with 'p' key, press left mouse button and move the selection to the desired location. After releasing the left mouse button voronoi center position will be changed.
</ul>

<h2>Editing properties:</h2>
<ul>
<li>Sample tab: contains sample traitUI properties.
<li>All points tab: Allows to change the size of all actors.
<li>Selected point tab: Allows to change a name and a color of a sphere actor. NOTE: second bar must be used to change color (and enen then color will be refreshed only after changing view in 3D window).
<li>Help tab: Displays the information about application interface.
</ul>

<h2>Default mouse interaction</h2>
<p>These are the default interactions for tvtk.InteractorStyleImage():</p>

<ul>
<li>Holding down 'SHIFT' and the left mouse button down will pan the scene
<li>Holding down 'CONTROL' will rotate around the camera's axis (roll).
<li>Rotating the mouse wheel upwards will zoom in and downwards will zoom out.
</ul>

<h2>Default keyboard interaction</h2>
<p>The scene supports several features activated via keystrokes. These are:</p>
<ul>
<li>'3': Turn on/off stereo rendering. This may not work if the 'stereo' preference item is not set to True.
<li>'e'/'q'/'Esc': Exit full-screen mode.
<li>'f': Move camera's focal point to current mouse location. This will move the camera focus to center the view at the current mouse position.
<li>'l': Configure the lights that are illumining the scene. This will pop-up a window to change the light configuration.
<li>'r': Reset the camera focal point and position. This is very handy.
<li>'s': Save the scene to an image, this will first popup a file selection dialog box so you can choose the filename, the extension of the filename determines the image type.
<li>'='/'+': Zoom in.
<li>'-': Zoom out.
<li>'left'/'right'/'up'/'down' arrows: Pressing the left, right, up and down arrow let you rotate the camera in those directions. When 'SHIFT' modifier is also held down the camera is panned.
</ul>
    """        
    ## controls    
    # size of voronoi cell centers
    voronoi_center_size = Range(1,10.,0.1)

    ## displayed application internals 
    _help = HTML(__doc__)    
    scene_model = Instance( MlabSceneModel, () )
    _bg_image = Instance( ImageActor, () )
    _bw = Instance( tvtk.SphereWidget, () )
    ## not displayed application internals
    _voronoi_center_list = []
    _selected_voronoi_center = Any()#Instance( VoronoiCenterVisRep, () )
    _voronoi_wt = Instance( WalledTissue, () )
    _voronoi_vtk = Instance(  tvtk.PolyData, () )
    _voronoi_vtk_ds = Instance( VTKDataSource, ())
    _cell_scalars_active = Bool(False)
    _cell_scalars_active_name = Str("custom_cell_property1")
    _cell_scalars_dynamic = Bool(True)
    #_cell_scalars_opacity = Range(0,1)
    _selected_action =  Any()
    _cell_scalars_range = Array(Float, (2,1) )
    actions = {}
    
    def voronoi_centers( self ):
        """Returns a list of positions of voronoi centers.
        
        :rtype: [(x,y)]
        :return: A list of positions of voronoi centers in current scene.
        """
        l = []
        for i in self._voronoi_center_list:
            p = i.position
            l.append( (p[0], p[1]) )
        return l                                   

    @on_trait_change('voronoi_center_size')
    def update_plot(self):
        for i in self._voronoi_center_list:
            i.scale=array([self.voronoi_center_size,self.voronoi_center_size, \
                self.voronoi_center_size])
        self.scene_model.render()


    def remove_all_voronoi_centers( self, update_vtk_from_voronoi=False ):
        self.remove_voronoi_centers( self._voronoi_center_list, update_vtk_from_voronoi=False )
        self.select_voronoi_center( None )
        #self.update_vtk_from_voronoi( render_scene= render_scene)

    
    def add_voronoi_center( self, pos=(0,0,0), render_scene=True, update_vtk_from_voronoi=True ):
        vc = self.voronoi_centers()
        if (pos[0],pos[1]) in vc:
            return None
        s = self.voronoi_factory(resolution=8, radius=1. )
        s.scale=array([self.voronoi_center_size,self.voronoi_center_size, \
            self.voronoi_center_size])
        s.position = pos
        self.scene_model.add_actor( s )
        self._voronoi_center_list.append( s )
        if update_vtk_from_voronoi:
            self.update_vtk_from_voronoi( render_scene=render_scene)
        return s


    def add_voronoi_centers( self, pos_list=[], render_scene=True, \
        update_vtk_from_voronoi=True, **kwargs ):
        t = []
        for i in pos_list:
            s = self.voronoi_factory(resolution=8, radius=1., **kwargs )
            s.scale=array([self.voronoi_center_size,self.voronoi_center_size, \
                self.voronoi_center_size])
            s.position = i
            self._voronoi_center_list.append( s )
            t.append( s )
        self.scene_model.add_actors( t )
        if update_vtk_from_voronoi: self.update_vtk_from_voronoi( render_scene=render_scene)


    def select_voronoi_center( self, voronoi_center ):
        if voronoi_center:
            self._bw.prop3d = voronoi_center
            self._bw.center = voronoi_center.position
            # hack to avoid crash
            self._bw.place_widget(-2.,-1.,-2.,-1.,-2.,-1.)
            self.scene_model.render()
            self._bw.place_widget()
            self.scene_model.render()
        self._selected_voronoi_center = voronoi_center


    def remove_voronoi_center( self, voronoi_center, render_scene=True, update_vtk_from_voronoi=True ):
        self._voronoi_center_list.remove( voronoi_center )
        self.scene_model.remove_actor( voronoi_center )
        if self._voronoi_center_list:
            self.select_voronoi_center( self._voronoi_center_list[ 0 ] )
        else:
            self.select_voronoi_center( None )
        if update_vtk_from_voronoi:
            self.update_vtk_from_voronoi( render_scene= render_scene)



    def remove_voronoi_centers( self, voronoi_center_list=[], render_scene=True, update_vtk_from_voronoi=True ):
        for i in voronoi_center_list:
            self._voronoi_center_list = []
        self.select_voronoi_center( None )
        self.scene_model.disable_render = True
        self.scene_model.remove_actors( voronoi_center_list )
        self.scene_model.disable_render = False
        if render_scene: self.scene_model.render()
        if update_vtk_from_voronoi: self.update_vtk_from_voronoi( render_scene= render_scene)
        

    def register_actions( self ):        
        file_load_background_image = FileLoadBackgroundImage(
                parent=self,
                name = "Load background",
                toolip = "Loads background image file to the current scene",            
                action = "self.perform",
        )
        self.actions["file_load_background_image"] =file_load_background_image
        
        actions_update_voronoi_edges = ActionsUpdateVoronoiEdges(
            parent=self,
            name = "Update edges",
            toolip = "Updates voronoi edges", 
            action = "self.perform",
        )
        self.actions["actions_update_voronoi_edges"] =actions_update_voronoi_edges


    def display_tissue_scalar_properties( self, property, render_scene=True, voronoi_changed=False ):
        if voronoi_changed:
            #updates the WalledTissue properties with voronoi centers
            synchronize_id_of_wt_and_voronoi(self._voronoi_wt, self._voronoi_center_list)
            copy_cell_properties_from_voronoi_to_wt( self._voronoi_wt, \
                self._voronoi_center_list, self.cell_properties )
    
        t = self._voronoi_wt
        cell_nbr = len( t.cells() )
        prop_value = zeros( cell_nbr )
        max = -inf
        min = inf
        for i in range( cell_nbr ):
            p = t.cell_property( self._cell_id_vtk2wt[ i ], property )
            prop_value[ i ] = p
            if p > max: max = p
            if p < min: min = p
        
        self._voronoi_vtk.cell_data.scalars = prop_value
        self._voronoi_vtk.cell_data.scalars.name = property
        
        #engine.mlab.get_engine()
        #module_manager = engine.scenes[0].children[0].children[0]
        self._voronoi_cell_polygons.parent.scalar_lut_manager.use_default_range = False
        if not self._cell_scalars_dynamic:
            self._voronoi_cell_polygons.parent.scalar_lut_manager.data_range = \
                array( \
                    [ float( self._cell_scalars_range[ 0 ]), \
                    float( self._cell_scalars_range[ 1 ]) ] \
                )
        else:
            self._voronoi_cell_polygons.parent.scalar_lut_manager.data_range = \
                array( [ min, max ] )
            
        if render_scene: self._voronoi_vtk_ds.update()  


    def update_vtk_from_voronoi( self, render_scene = True, voronoi_changed=False ):
        # TODO
        d = walled_tissue2vtkPolyData( self._voronoi_wt )
        self._voronoi_vtk = d["tissue"]
        self._cell_id_vtk2wt = d["cell_id_vtk2wt"]
        self._cell_id_wt2vtk = d["cell_id_wt2vtk"]
        self._wv_id_wt2vtk = d["wv_id_wt2vtk"]
        self._wv_id_vtk2wv = d["wv_id_vtk2wt"]
        if not self._voronoi_vtk_ds:
            self._voronoi_vtk_ds = VTKDataSource(data=self._voronoi_vtk)
            engine = mlab.get_engine()
            engine.add_source( self._voronoi_vtk_ds ) 
            self._voronoi_cell_polygons = mlab.pipeline.surface(self._voronoi_vtk_ds, opacity=0.25)
            self._voronoi_cell_edges = mlab.pipeline.surface(mlab.pipeline.extract_edges(self._voronoi_vtk_ds),
                                    color=(0, 0, 0), )
        else:
            self._voronoi_vtk_ds.data = self._voronoi_vtk
            self._voronoi_vtk_ds.update()
        if self._cell_scalars_active:
            if self._cell_scalars_active_name in self.cell_properties.keys():
                self.display_tissue_scalar_properties( self._cell_scalars_active_name, render_scene=False, voronoi_changed=voronoi_changed )
        if render_scene: self.scene_model.render()


        
    def __init__( self, voronoi_factory=default_voronoi_factory, cell_properties={} ):
        super(CompartmentWindow, self).__init__()
        self.voronoi_factory = voronoi_factory
        self.cell_properties = cell_properties
        self._voronoi_cell_scalars = None
        #self.register_actions()


#----------------------------------------------------------------------------- IO OPERATIONS

class FileLoadBackgroundImage(MyAction):
    def perform(self):
        """Pops up a dialog used to load a background image."""
        a = self._application
        extns = ['*.bmp','*.png','*.tif','*.jpg','*']
        dlg = FileDialog( action='open',
                wildcard='*', title="Load image")
        
        if dlg.open() == OK:
            engine = mlab.get_engine()
            image_reader = engine.open( dlg.path )
            a._bg_image = ImageActor()
            engine.add_filter(a._bg_image, image_reader)
            (x1,x2) = a._bg_image.actor.x_range
            (y1,y2) = a._bg_image.actor.y_range
            if a.actions.has_key( "action_add_voronoi_centers" ):
                act = a.actions[ "action_add_voronoi_centers" ]
                a._cut_plane.place_widget(x1,x2,y1,y2,0.,0.)
                act.voronoi_centers_limit_left_bottom_position = (x1,y1)
                act.voronoi_centers_limit_right_top_position = (x2,y2)


class FileLoadWalledTissue(MyAction):
    def perform(self):
        """Pops up a dialog used to load WalledTissue"""
        a = self._application
        dlg = DirectoryDialog( action='open',
                wildcard='*', title="Load WalledTissue")
        
        if dlg.open() == OK:
            self.load( dlg.path )
            
    def load( self, path):
            a = self._application
            # TODO: add reading properties to voronoi center class
            a.remove_all_voronoi_centers( update_vtk_from_voronoi=False )
            a._voronoi_wt = read_walled_tissue( file_name=path  )
                
            pos_list = []
            for i in a._voronoi_wt.cells():
                pos_list.append( a._voronoi_wt.cell_property(i, "voronoi_center" ) )
            for i in a._voronoi_wt.tissue_property("outside_voronoi_centers"):
                pos_list.append( i )
            
            a.add_voronoi_centers( pos_list=pos_list, render_scene=False, \
                update_vtk_from_voronoi=False )

            #updates the properties of voronoi centers with WalledTissue properties 

            synchronize_id_of_wt_and_voronoi(a._voronoi_wt, a._voronoi_center_list)
            copy_cell_properties_from_wt_to_voronoi( a._voronoi_wt, \
                a._voronoi_center_list, a._voronoi_wt.const.cell_properties )
            
            
            a.update_vtk_from_voronoi()

#----------------------------------------------------------------------------- SHARED ACTIONS
    
class ActionsUpdateVoronoiEdges(MyAction):
    """ Produces and displays the voronoi edges. """
    def perform_calc(self):
        """ Performs the action. """
        a = self._application
        a.update_vtk_from_voronoi( render_scene=True )
    