#!/usr/bin/env python
"""Application allowing for 2D tissue digitalization.

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


# ---------------------------------------------------------------- IMPORTS
# Standard library imports.
import random
import math

# Enthought library imports.
from enthought.pyface.api import FileDialog, DirectoryDialog, GUI, OK, \
    ImageResource
from enthought.pyface.action.api import Action, MenuBarManager, \
    MenuManager, ToolBarManager

from enthought.traits.api import  Instance, HasTraits, Range, \
    on_trait_change, Color, HTML, Enum, Tuple, Int, Bool, Array, Float, Any

from enthought.tvtk.pyface.scene_editor import SceneEditor
from enthought.tvtk.api import tvtk

from enthought.traits.ui.api import View, Item, VGroup,  Tabbed, \
    HSplit, InstanceEditor

from enthought.mayavi.tools.mlab_scene_model import MlabSceneModel
from enthought.mayavi.core.ui.mayavi_scene import MayaviScene
from enthought.mayavi import mlab
from enthought.mayavi.sources.vtk_data_source import VTKDataSource
from enthought.mayavi.modules.image_actor import ImageActor

from vtk.util import colors

from numpy import array, zeros

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


# ---------------------------------------------------- GUI DATASTRUCTURE CLASSES


class VoronoiCenterVisRep(tvtk.Actor):
    """Represents the cell center of a cell.
    """
    cell_id = Int(-1)
    voronoi_center = Any
    was_inf = Bool(False)
    
    def __init__(self, center=(0, 0, 0), radius=0.1, resolution=16,
                     color=colors.white, opacity=1.0, **kwargs):
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
                     color=colors.white, opacity=1.0,):
    """Used to generate voronoi centers.
    """
    return VoronoiCenterVisRep( center=center, radius=radius, resolution=resolution,
                     color=color, opacity=opacity )
    
class VoronoiCenterVisRep1(VoronoiCenterVisRep):
    """Represents the cell center of a cell.
    """
    cell_center_color = Color()
    cell_type = Enum("outside","cytoplasm","membrane","kernel")
    custom_cell_type1 = Int(0)
    custom_cell_type2 = Int(0)
    custom_cell_type3 = Int(0)
    custom_cell_type4 = Int(0)
    aqp2 = Range(0,1.)

    
    def __init__(self, center=(0, 0, 0), radius=0.1, resolution=16,
                     color=colors.white, opacity=1.0, **kwargs):
        """ Creates a sphere and returns the actor. """
        super(VoronoiCenterVisRep1, self).__init__( **kwargs )
        source = tvtk.SphereSource(center=center, radius=radius,
                                   theta_resolution=resolution,
                                   phi_resolution=resolution)
        self.mapper = tvtk.PolyDataMapper(input=source.output)
        self.property = tvtk.Property(opacity=opacity, color=color)
        self.voronoi_center=array(3)
    
    def default_traits_view( self ):    
        view = View(
            Item("cell_id", style='readonly'),
            #Item("voronoi_center", style='readonly'),
            #Item("was_inf", style='readonly'),
            Item("cell_type",style='simple'),
            Item("aqp2"),
            Item("custom_cell_type1",style='simple'),
            #Item("custom_cell_type2",style='simple'),
            #Item("custom_cell_type3",style='simple'),
            #Item("custom_cell_type4",style='simple'),
        )
        return view
    
    @on_trait_change('cell_type')
    def change_cell_center_color(self):
        c = self.cell_center_color
        if self.cell_type == "cytoplasm":
            self.property.color = colors.blue
        elif self.cell_type == "membrane":
            self.property.color = colors.red
        elif self.cell_type == "outside":
            self.property.color = colors.white
        elif self.cell_type == "kernel":
            self.property.color = colors.black    

def voronoi_factory_aqp1( center=(0, 0, 0), radius=0.1, resolution=16,
                     color=colors.white, opacity=1.0,):
    """Used to generate voronoi centers.
    """
    return VoronoiCenterVisRep1( center=center, radius=radius, resolution=resolution,
                     color=color, opacity=opacity )
    
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
    def __init__(self, **kwargs):
        """Init"""
        super(MyAction, self).__init__( **kwargs )
        self._application = kwargs['parent']

# ---------------------------------------------------------------------- ACTIONS

        
class ActionsAddRandomVoronoiCenters(MyAction):
    def perform(self):
        """
        Adds random voronoi centers.
        """
        a = self._application
        p=[]
        (xmin,ymin) = a.voronoi_centers_limit_left_bottom_position
        (xmax,ymax) = a.voronoi_centers_limit_right_top_position
        x_range = xmax-xmin
        y_range = ymax-ymin
        for i in range( a.voronoi_centers_add_number ):
            p.append( (xmin+x_range*random.random(), ymin+y_range*random.random(), 0.) )
        a.add_voronoi_centers( pos_list=p, render_scene=False )    
        a.scene_model.render()
   
        
class ActionsAddGridVoronoiCenters(MyAction):
    def perform(self):
        a = self._application
        p=[]
        (xmin,ymin) = a.voronoi_centers_limit_left_bottom_position
        (xmax,ymax) = a.voronoi_centers_limit_right_top_position
        x_range = xmax-xmin
        y_range = ymax-ymin
        area = x_range*y_range
        small_area = area/ float(a.voronoi_centers_add_number)
        delta = math.sqrt( small_area )
        x_nbr = int(x_range / delta)
        y_nbr = int(y_range / delta)
        for i in range( x_nbr ):
            for j in range( y_nbr ):
                p.append( ( (j%2)*delta/2.+xmin+(delta/2.)+i*delta, (ymin+(delta/2.)+j*delta), 0. ) )
        a.add_voronoi_centers( pos_list=p, render_scene=False )    
        a.scene_model.render()


class ActionsUpdateVoronoiEdges(MyAction):
    """ Produces and displays the voronoi edges. """
    def perform(self):
        """ Performs the action. """
        a = self._application
        a.update_vtk_from_voronoi( render_scene=True )


class FileLoadBackgroundImage(MyAction):
    def perform(self):
        """Pops up a dialog used to load a background image."""
        a = self._application
        extns = ['*.bmp','*.png','*.tif','*.jpg']
        dlg = FileDialog( action='open',
                wildcard='|'.join(extns), title="Load image")
        
        if dlg.open() == OK:
            engine = mlab.get_engine()
            image_reader = engine.open( dlg.path )
            a._bg_image = ImageActor()
            engine.add_filter(a._bg_image, image_reader)
            (x1,x2) = a._bg_image.actor.x_range
            (y1,y2) = a._bg_image.actor.y_range
            a.voronoi_centers_limit_left_bottom_position = (x1,y1)
            a.voronoi_centers_limit_right_top_position = (x2,y2)


class FileSaveWalledTissue(MyAction):
    def perform(self):
        """Pops up a dialog used to save WalledTissue."""
        a = self._application
        extns = ['*']
        dlg = FileDialog( action='save as',
                wildcard='|'.join(extns), title="Save WalledTissue")
        
        if dlg.open() == OK:
            t = a._voronoi_wt
            
            
            #updates the WalledTissue properties with voronoi centers
            synchronize_id_of_wt_and_voronoi(a._voronoi_wt, a._voronoi_center_list)
            copy_cell_properties_from_voronoi_to_wt( a._voronoi_wt, \
                a._voronoi_center_list, a.cell_properties )
            
            ovc = []
            for i in a._voronoi_center_list:
                if i.cell_id != -1 :
                    t.cell_property( i.cell_id, "voronoi_center", i.position)
                else:
                    ovc.append(i.position)
            t.tissue_property( "outside_voronoi_centers", ovc )
            
            saved_tissue = write_walled_tissue( tissue=a._voronoi_wt, name=dlg.path, desc="Test tissue" )


class FileLoadWalledTissue(MyAction):
    def perform(self):
        """Pops up a dialog used to load WalledTissue"""
        a = self._application
        extns = ['*']
        dlg = DirectoryDialog( action='open',
                wildcard='|'.join(extns), title="Load WalledTissue")
        
        if dlg.open() == OK:
            # TODO: add reading properties to voronoi center class
            a.remove_all_voronoi_centers( update_vtk_from_voronoi=False )
            a._voronoi_wt = read_walled_tissue( file_name=dlg.path  )
                
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

# ------------------------------------------------------------------ APPLICATION

                
class ExampleWindow( HasTraits ):
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
    # 
    voronoi_centers_limit_left_bottom_position = Tuple(0., 0.)
    voronoi_centers_limit_right_top_position = Tuple(100., 100.)
    voronoi_centers_add_number = Int(100)
    ## displayed application internals 
    _help = HTML(__doc__)    
    scene_model = Instance( MlabSceneModel, () )
    _bg_image = Instance( ImageActor, () )
    _bw = Instance( tvtk.SphereWidget, () )
    ## not displayed application internals
    _voronoi_center_list = []
    _selected_voronoi_center = Instance( VoronoiCenterVisRep, () )
    _voronoi_wt = Instance( WalledTissue, () )
    _voronoi_vtk = Instance(  tvtk.PolyData, () )
    _voronoi_vtk_ds = Instance( VTKDataSource, ())

    
    def default_traits_view( self ):
        """Description of default view.
        """
        self.actions = {}
        # defining menu/toolbar positions
        # note: they can be shared
        action_add_random_voronoi_centers = ActionsAddRandomVoronoiCenters(
                parent=self,
                name = "Add random centers",
                action = "self.perform",
                toolip = "Adds randomly placed voronoi centers to the current scene",
                )
        self.actions["action_add_random_voronoi_centers"] =action_add_random_voronoi_centers
        
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
        
        actions_add_grid_voronoi_centers = ActionsAddGridVoronoiCenters(
            parent=self,
            name = "Add grid centers",
            toolip = "Adds voronoi centers distributed on grid", 
            action = "self.perform",
        )
        self.actions["actions_add_grid_voronoi_centers"] =actions_add_grid_voronoi_centers
        
        file_save_walled_tissue = FileSaveWalledTissue(
            parent=self,
            name = "Save WalledTissue",
            toolip = "Saves WalledTissue", 
            action = "self.perform",
        )
        self.actions["file_save_walled_tissue"] =file_save_walled_tissue
        
        file_load_walled_tissue = FileLoadWalledTissue(
            parent=self,
            name = "Load WalledTissue",
            toolip = "Loads WalledTissue", 
            action = "self.perform",
        )
        self.actions["file_load_walled_tissue"] =file_load_walled_tissue
        
        # specifying the view
        view = View(
            # specifying the layout of the window,
            # look at:
            # http://code.enthought.com/projects/traits/docs/html/TUIUG/advanced_view.html
            # http://code.enthought.com/projects/traits/docs/html/TUIUG/view.html
            HSplit(
                Item(
                    name='scene_model',
                    editor=SceneEditor(
                        # custom scene is used to get rid of default
                        # scene toolbar
                        scene_class=MayaviScene,
                    ),
                    show_label=False,
                ),
                Tabbed(
                    VGroup(
                        VGroup(
                            Item(
                                "voronoi_centers_limit_left_bottom_position",
                                label="Left bottom",
                            ),
                            Item(
                                "voronoi_centers_limit_right_top_position",
                                label="Right top",
                            ),
                            Item(
                                "voronoi_centers_add_number",
                                label="# centers",
                                # Number of voronoi centers to add
                            ),
                            show_border = True,
                            label = 'Add Voronoi centers',
                        ),
                        show_border = True,
                        label = 'Actions',
                    ),
                    VGroup(
                        "voronoi_center_size",                        
                        show_border = True,
                        label = 'Visualisation',
                    ),
                    VGroup(
                        Item(
                            name='_selected_voronoi_center',
                            editor=InstanceEditor(),
                            enabled_when='_selected_voronoi_center is not None',
                            style='custom',
                            label='',
                            show_label=False,
                        ),
                        show_border = True,
                        label = 'Selected center',
                    ),
                    VGroup(
                        Item(
                            name='_help',
                            show_label=False,
                        ),
                        show_border = True,
                        label = 'Help',
                    ),
                ),
            ),
            # specyfing type of the window,
            # look at:
            # http://code.enthought.com/projects/traits/docs/html/TUIUG/custom_view.html
            kind='live',
            title='MyApplication',
            resizable=True,
            width=800,
            height=600,
            # defining menubar content
            menubar = MenuBarManager(
                MenuManager(
                    file_load_background_image,
                    file_save_walled_tissue,
                    file_load_walled_tissue,
                    name = '&File',
                ),
                MenuManager(
                    action_add_random_voronoi_centers,
                    actions_update_voronoi_edges,
                    actions_add_grid_voronoi_centers,
                    name = '&Actions',
                ),
            ),
            ## defining toolbar content
            toolbar= ToolBarManager(
                file_load_background_image,
                actions_add_grid_voronoi_centers,
            ),
        )
        return view

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
                                   
    def do( self ):
        """Sets the application after initialization.
        """
        self._bw = tvtk.SphereWidget(interactor=self.scene_model.interactor, place_factor=1.05)
        if len(self._voronoi_center_list):
            self._bw.prop3d=self._voronoi_center_list[0]
            self.selecte_voronoi_center( self._voronoi_center_list[0] )
            self._bw.scale = False
            self._bw.place_widget()

        def callback_end(widget, event):
            """This callback sets the """
            if self._bw.prop3d:
                self._bw.prop3d.position = self._bw.center
                self.update_vtk_from_voronoi( render_scene=True )                   
        self._bw.add_observer("EndInteractionEvent", callback_end)
        self._bw.on()
        
        # switching the spheres using picker - key 'p'
        def rmc2_callback(widget, event):
            """Alternative right mouse click callback"""
            if self.scene_model.picker.pointpicker.actor in self._voronoi_center_list:
                self.select_voronoi_center( self.scene_model.picker.pointpicker.actor )
        self.scene_model.picker.pointpicker.add_observer("PickEvent", rmc2_callback)
        self.scene_model.picker.show_gui = False
        
        # region picking 'b'
        def pick_voronoi_region_callback(widget, event):
            """Alternative right mouse click callback"""
            if widget.GetKeyCode() == 'b':
                pos = widget.GetEventPosition()
                self.d = self.scene_model.picker.pick_cell(pos[ 0 ], pos[ 1 ])
                #print " #: updated d..", self.d.cell_id
        self.scene_model.interactor.add_observer("KeyPressEvent", pick_voronoi_region_callback)
 
        # adding a sphere using key interaction - key 'z'
        def add_actor_callback(widget, event):
            """Alternative right mouse click callback"""
            if widget.GetKeyCode() == 'z':
                pos = widget.GetEventPosition()
                d = self.scene_model.picker.pick_point(pos[ 0 ], pos[ 1 ])
                self.select_voronoi_center( self.add_voronoi_center(pos=(d.coordinate[ 0 ], d.coordinate[ 1 ], 0.) ) )
                #self.event_w = widget
        self.scene_model.interactor.add_observer("KeyPressEvent", add_actor_callback)

        # adding a sphere using key interaction - key 'x'
        def remove_voronoi_center_callback(widget, event):
            """Removes selected voronoi center"""
            if widget.GetKeyCode() == 'x':
                if self._selected_voronoi_center:
                    self.remove_voronoi_center( self._selected_voronoi_center )
                    if self._voronoi_center_list:
                        self.select_voronoi_center( self._voronoi_center_list[ 0 ] )
        self.scene_model.interactor.add_observer("KeyPressEvent", remove_voronoi_center_callback)

        # removing all voronoi centers - key 'c'
        def remove_all_voronoi_centers_callback(widget, event):
            """Removes selected voronoi center"""
            if widget.GetKeyCode() == 'c':
                self.remove_all_voronoi_centers()
        self.scene_model.interactor.add_observer("KeyPressEvent", \
            remove_all_voronoi_centers_callback)

        # comment it if you would like "normal" 3d interactor instead of the one
        # described in __doc__
        self.scene_model.interactor.interactor_style = \
            tvtk.InteractorStyleImage()
        
        self.scene_model.parallel_projection=True
        
        self._voronoi_ds_vtk = None


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
        s = self.voronoi_factory(resolution=4, radius=1. )
        s.scale=array([self.voronoi_center_size,self.voronoi_center_size, \
            self.voronoi_center_size])
        s.position = pos
        self.scene_model.add_actor( s )
        self._voronoi_center_list.append( s )
        if update_vtk_from_voronoi: self.update_vtk_from_voronoi( render_scene=render_scene)
        return s


    def add_voronoi_centers( self, pos_list=[], render_scene=True, update_vtk_from_voronoi=True ):
        t = []
        for i in pos_list:
            s = self.voronoi_factory(resolution=4, radius=1. )
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
            self._bw.place_widget()
            self.scene_model.render()
        self._selected_voronoi_center = voronoi_center


    def remove_voronoi_center( self, voronoi_center, render_scene=True, update_vtk_from_voronoi=True ):
        self._voronoi_center_list.remove( voronoi_center )
        self.scene_model.remove_actor( voronoi_center )
        if self._voronoi_center_list:
            self.select_voronoi_center( self._voronoi_center_list[ 0 ] )
        else: self.select_voronoi_center( None )
        if update_vtk_from_voronoi: self.update_vtk_from_voronoi( render_scene= render_scene)


    def remove_voronoi_centers( self, voronoi_center_list=[], render_scene=True, update_vtk_from_voronoi=True ):
        for i in voronoi_center_list:
            self._voronoi_center_list = []
        self.select_voronoi_center( None )
        self.scene_model.disable_render = True
        self.scene_model.remove_actors( voronoi_center_list )
        self.scene_model.disable_render = False
        if render_scene: self.scene_model.render()
        if update_vtk_from_voronoi: self.update_vtk_from_voronoi( render_scene= render_scene)
        
    def update_vtk_from_voronoi( self, render_scene = True ):
        # TODO
        if len( self._voronoi_center_list ) > 4:
            (i,o) = voronoi_centers_to_edges( self.voronoi_centers() )
            c1 = self.voronoi_centers_limit_left_bottom_position 
            c2 = self.voronoi_centers_limit_right_top_position
            self._voronoi_wt = read_qhull2walled_tissue(i, o, remove_infinite_cells=True, constraints=(c1, c2) )
            self._voronoi_vtk, self._cell_id_vtk2wt, self._cell_id_wt2vtk = \
                walled_tissue2vtkPolyData( self._voronoi_wt )
            
        
        if not self._voronoi_ds_vtk:
            self._voronoi_ds_vtk = VTKDataSource(data=self._voronoi_vtk)
            engine = mlab.get_engine()
            engine.add_source( self._voronoi_ds_vtk ) 
            mlab.pipeline.surface(self._voronoi_ds_vtk, opacity=0.05)
            mlab.pipeline.surface(mlab.pipeline.extract_edges(self._voronoi_ds_vtk),
                                    color=(0, 0, 0), )
        else:
            self._voronoi_ds_vtk.data = self._voronoi_vtk
            self._voronoi_ds_vtk.update()
        
        if render_scene: self.scene_model.render()
    
    def display_tissue_scalar_properties( self, property='aqp2' ):
        #updates the WalledTissue properties with voronoi centers
        synchronize_id_of_wt_and_voronoi(self._voronoi_wt, self._voronoi_center_list)
        copy_cell_properties_from_voronoi_to_wt( self._voronoi_wt, \
            self._voronoi_center_list, self.cell_properties )
    
        t = self._voronoi_wt
        cell_nbr = len( t.cells() )
        prop_value = zeros( cell_nbr )
        for i in range( cell_nbr ):
            prop_value[ i ] = t.cell_property( self._cell_id_vtk2wt[ i ], property )
        
        self._voronoi_vtk.cell_data.scalars = prop_value
        self._voronoi_vtk.cell_data.scalars.name = property
        #id = self._voronoi_vtk.cell_data.add_array( prop_value )
        #self._voronoi_vtk.cell_data.get_array(id).name = property
        
        if not self._voronoi_cell_scalars:
            self._voronoi_cell_scalars = self.scene_model.mlab.pipeline.set_active_attribute(
                self._voronoi_vtk)
        self._voronoi_cell_scalars.cell_scalars_name = property
        
    def __init__( self, voronoi_factory, cell_properties ):
        super(ExampleWindow, self).__init__()
        self.voronoi_factory = voronoi_factory
        self.cell_properties = cell_properties
        self._voronoi_cell_scalars = None
        


def mesh_editing():
    cell_properties = {
    }
    return ExampleWindow( voronoi_factory=default_voronoi_factory, \
        cell_properties=cell_properties)

def aqp_editing():
    cell_properties = {
        'custom_cell_type1': 1,
        'cell_type': 'outside',
        'aqp2': 0.,
    }
    return ExampleWindow( voronoi_factory=voronoi_factory_aqp1, \
        cell_properties=cell_properties)

if __name__ == '__main__':
    # Create and open an application window.
    #window = mesh_editing()
    window = aqp_editing()
    window.edit_traits()
    GUI().start_event_loop()
    window.do()
        
