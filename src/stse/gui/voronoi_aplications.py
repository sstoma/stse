#!/usr/bin/env python

"""Rutines for compartment editor viewer.
:todo:
    To be revied by somebody skillfull in VTK/TraitsUI/tvtk
:bug:
    None known.
:organization:
    INRIA/Humboltd University Berlin"""
    
# Module documentation variables:
__authors__ = """Szymon Stoma"""
__contact__ = "<Your contact>"
__license__ = "Cecill-C"
__date__ = "<Timestamp>"
__version__ = "0.1"
__docformat__ = "restructuredtext en"


# ----------------------------------IMPORTS-----------

import random
import math
from copy import copy

from pylab import inf

from numpy import array, zeros, inf, infty

from pyface.api import FileDialog, DirectoryDialog, GUI, OK, ImageResource
from pyface.action.api import Action, MenuBarManager, MenuManager, ToolBarManager

from traits.api import  Instance, HasTraits, Range, on_trait_change, Color, HTML, \
    Enum, Tuple, Int, Bool, Array, Float, Any, Str, Button

from traits.trait_errors import TraitError

from tvtk.pyface.scene_editor import SceneEditor
from tvtk.api import tvtk

from traitsui.api import View, Item, VGroup, Tabbed, HSplit, InstanceEditor, HGroup

from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene
from mayavi import mlab
from mayavi.sources.vtk_data_source import VTKDataSource
from mayavi.modules.image_actor import ImageActor
from twisted.python.filepath import FilePath #TODO check if needed

from vtk.util import colors

from openalea.stse.structures.walled_tissue import WalledTissue
from openalea.stse.structures.walled_tissue_const import WalledTissueConst

from openalea.stse.io.walled_tissue.native_representation import write_walled_tissue, read_walled_tissue
from openalea.stse.io.walled_tissue.vtk_representation import synchronize_id_of_wt_and_voronoi
from openalea.stse.io.walled_tissue.qhull_representation import read_qhull2walled_tissue

from openalea.stse.io.qhull import voronoi_centers_to_edges

from openalea.stse.tools.emergency import kill_close_points
from openalea.stse.tools.convex_hull import int_points_in_polygon, hulls

from openalea.stse.structures.algo.walled_tissue import calculate_cell_surface, cell_centers, create
from openalea.stse.structures.algo.walled_tissue_topology import find_degenerated_cells, kill_degenerated_cells

from openalea.stse.tools.convex_hull import int_points_in_polygon, xy_minimal_bounding_box_of_polygon, point_inside_polygon

from openalea.plantgl.math import Vector3


# ----------------------------------GUI DATASTRUCTURE CLASSES------

# Represents the cell center of a cell.
class VoronoiCenterVisRep(tvtk.Actor):
    """Represents the cell center of a cell."""
    
    cell_id = Int(-1)
    voronoi_center = Any
    was_inf = Bool(False)
    
    # Init.
    def __init__(self, center = (0, 0, 0), radius = 0.1, resolution = 16,
            color = colors.white, opacity = 1.0, cell_type = '', **kwargs):
                     
        """ Creates a sphere and returns the actor. """
        super(VoronoiCenterVisRep, self).__init__( **kwargs )
        
        source = tvtk.SphereSource(center = center, radius = radius,
            theta_resolution = resolution, phi_resolution = resolution)
                                   
        self.mapper = tvtk.PolyDataMapper(input = source.output)
        self.property = tvtk.Property(opacity = opacity, color = color)
    
    # Prepare default view.
    def default_traits_view(self):    
        view = View(
            Item("cell_id", style = 'readonly'),
        )
        
        return view
    
    # Change cell id.
    @on_trait_change('cell_id')
    def change_cell_id(self):
        pass


# Generate voronoi centers.
def default_voronoi_factory(center = (0, 0, 0), radius = 0.1, resolution = 16,
        color = colors.white, opacity = 1.0, **kwargs):
                     
    """Used to generate voronoi centers."""
    return VoronoiCenterVisRep(center = center, radius = radius, resolution = resolution,
        color = color, opacity = opacity, **kwargs)


# Represents the cell center of a cell.
class VoronoiCenterVisRepGeneral(VoronoiCenterVisRep):
    """Represents the cell center of a cell."""
    
    cell_center_color = Color()
    cell_type = Enum("A", "B", "C", "D", "E", "F", "G", "H", "I")
    
    custom_cell_property1 = Float(0.)
    custom_cell_property2 = Float(0.)
    custom_cell_property3 = Float(0.)
    custom_cell_property4 = Float(0.)
    custom_cell_property5 = Float(0.)
    
    # Init.
    def __init__(self, center = (0, 0, 0), radius = 0.1, resolution = 16,
            color = colors.white, opacity = 1.0, **kwargs):
                     
        """Creates a sphere and returns the actor."""
        super(VoronoiCenterVisRepGeneral, self).__init__( **kwargs )
        source = tvtk.SphereSource(center = center, radius = radius,
            theta_resolution = resolution, phi_resolution = resolution)
                                   
        self.mapper = tvtk.PolyDataMapper(input = source.output)
        self.property = tvtk.Property(opacity = opacity, color = color)
        
        self.voronoi_center = array(3)
        
        if kwargs.has_key("cell_type"):
            self.cell_type = kwargs["cell_type"]
            self.change_cell_center_color()
        
    # Prepare default view.
    def default_traits_view(self):    
        view = View(
            Item("cell_id", style = 'simple'),
            Item("cell_type", style = 'simple'),
            Item("custom_cell_property1", style = 'simple'),
            Item("custom_cell_property2", style = 'simple'),
            Item("custom_cell_property3", style = 'simple'),
            Item("custom_cell_property4", style = 'simple'),
            Item("custom_cell_property5", style = 'simple'),
        )
        
        return view
    
    # Change cell center color.
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
        elif self.cell_type == "F":
            self.property.color = colors.banana    
        elif self.cell_type == "G":
            self.property.color = colors.brown   
        elif self.cell_type == "H":
            self.property.color = colors.green   
        elif self.cell_type == "I":
            self.property.color = colors.azure 


# Generate voronoi centers.
def general_voronoi_factory(center = (0, 0, 0), radius = 0.1, resolution = 16,
        color = colors.white, opacity = 1.0, **kwargs):
    
    """Used to generate voronoi centers."""
    return VoronoiCenterVisRepGeneral(center = center, radius = radius, resolution = resolution,
        color = color, opacity = opacity, **kwargs )


# ----------------------------------CUSTOMIZING GUI CLASSES------

# Defined to get rid of default toolbar.
class MyScene(MlabSceneModel):
    """Defined to get rid of default toolbar."""

    pass


# Defined since the Actions in the toolbar/menu require some fields which are not defined in Action.
class MyAction(Action):
    """Defined since the Actions in the toolbar/menu require some fields which are not defined in Action."""
    
    # Why Action does not contain these variables?
    defined_when = ""
    enabled_when = ""
    checked_when = ""
    
    no_conf_string = Str("No configuration options")
    perform_btn = Button(label = 'Execute')
    
    # Init. 
    def __init__(self, **kwargs):
        """Init"""
        super(MyAction, self).__init__(**kwargs)
        self._application = kwargs['parent']
    
    # Prepare default view.
    def default_traits_view(self):
        """Description of default view."""
        view = View(
            Item(
                'no_conf_string',
                show_label = False,
                style = 'readonly',
            ),
            Item(
                "perform_btn",
                show_label = False,
            ),
        )
        
        return view
    
    # Perform button.
    def perform(self):
        """Adds action GUI to the control panel."""
        a = self._application
        a._selected_action = self
    
    # Runs default action.
    def _perform_btn_fired(self):
        """Runs default action."""
        self.perform_calc()

    # Perform calc button.
    def perform_calc(self):
        """Runs default action."""
        print " !: Perform not defined."


# Define general cell properties.
general_cell_properties = {
    'custom_cell_property1': 0.,
    'custom_cell_property2': 0.,
    'custom_cell_property3': 0.,
    'custom_cell_property4': 0.,
    'custom_cell_property5': 0.,
    'cell_type': 'A',
}


# ----------------------------------COMPARTMENT WINDOW------

# Compartment window.
class CompartmentWindow(HasTraits):
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

The Voronoi diagram is created only for centers inside given insets. These insets are set automatically while the background image is loaded or manually using the "View/Cut plane ON/OFF".

<h2>Editing properties:</h2>
<ul>
<li>Action tab: contains details of the selected action. Actions are changed by choosing them from the Actions menu.
<li>Visualization: Allows to change different properties of the visualisation. Actor size and color mapping for mesh cells are the most important among them.
<li>Selected center tab: Allows to change a name and a color of a sphere actor. NOTE: second bar must be used to change color (and enen then color will be refreshed only after changing view in 3D window).
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
    
    ## Controls.    
    # Size of voronoi cell centers.
    voronoi_center_size = Range(1, 10., 0.1)

    ## Displayed application internals. 
    _help = HTML(__doc__)
    
    scene_model = Instance(MlabSceneModel, ())
    _bg_image = Instance(ImageActor, ())
    _bg_image_reader = Any()
    _bw = Instance(tvtk.SphereWidget, ())
    
    ## Not displayed application internals.
    _voronoi_center_list = []
    _selected_voronoi_center = Any()
    
    _voronoi_wt = Instance(WalledTissue, ())
    _voronoi_vtk = Instance(tvtk.PolyData, ())
    _voronoi_vtk_ds = Instance(VTKDataSource, ())
    
    _cell_scalars_active = Bool(False)
    _cell_scalars_active_name = Str("custom_cell_property1")
    _cell_scalars_dynamic = Bool(True)

    _selected_action =  Any()
    _cell_scalars_range = Array(Float, (2,1))
    
    actions = {}
    
    # Init.
    def __init__(self, voronoi_factory = default_voronoi_factory, cell_properties = {}):
        super(CompartmentWindow, self).__init__()
        
        self.voronoi_factory = voronoi_factory
        self.cell_properties = cell_properties
        
        self._voronoi_cell_scalars = None
    
    # Returns a list of positions of voronoi centers.
    def voronoi_centers(self):
        """Returns a list of positions of voronoi centers.
        :rtype: [(x,y)]
        :return: A list of positions of voronoi centers in current scene."""
        
        l = []
        for i in self._voronoi_center_list:
            p = i.position
            l.append((p[0], p[1]))
            
        return l                                   

    # Update plot.
    @on_trait_change('voronoi_center_size')
    def update_plot(self):
        for i in self._voronoi_center_list:
            i.scale = array([self.voronoi_center_size, self.voronoi_center_size, self.voronoi_center_size])
            
        self.scene_model.render()

    # Remove all voronoi centers.
    def remove_all_voronoi_centers(self, update_properties_from_wt2d_to_pm = False):
        self.remove_voronoi_centers(self._voronoi_center_list, update_properties_from_wt2d_to_pm = False)
        self.select_voronoi_center(None)

    # Add voronoi center.
    def add_voronoi_center(self, pos = (0, 0, 0), render_scene = True, update_properties_from_wt2d_to_pm = True):
        vc = self.voronoi_centers()
        
        if (pos[0], pos[1]) in vc:
            return None
            
        s = self.voronoi_factory(resolution = 8, radius = 1.)
        
        s.scale = array([self.voronoi_center_size, self.voronoi_center_size, self.voronoi_center_size])
        s.position = pos
        
        self.scene_model.add_actor(s)
        self._voronoi_center_list.append(s)
        
        if update_properties_from_wt2d_to_pm:
            a = self.actions["actions_add_voronoi_centers"]
                
            c1 = a.voronoi_centers_limit_left_bottom_position 
            c2 = a.voronoi_centers_limit_right_top_position
            
            if len(self._voronoi_center_list) > 4:
                # Create WalledTissue2d from voronoi centers structure.
                self.create_wt2d_from_vc(remove_infinite_cells = True, constraints = (c1, c2)) 

            # Update properties from WalledTissue2d to polygonal mesh.
            self.update_properties_from_wt2d_to_pm(render_scene = render_scene, voronoi_changed = True)
            
        return s

    # Add voronoi centers.
    def add_voronoi_centers(self, pos_list = [], render_scene = True, update_properties_from_wt2d_to_pm = True, **kwargs):
        t = []
        
        for i in pos_list:
            s = self.voronoi_factory(resolution = 8, radius = 1., **kwargs)
            
            s.scale = array([self.voronoi_center_size, self.voronoi_center_size, self.voronoi_center_size])
            s.position = i
            
            self._voronoi_center_list.append(s)
            t.append(s)
            
        self.scene_model.add_actors(t)
        
        if update_properties_from_wt2d_to_pm:
            a = self.actions["actions_add_voronoi_centers"]
                
            c1 = a.voronoi_centers_limit_left_bottom_position 
            c2 = a.voronoi_centers_limit_right_top_position
            
            if len(self._voronoi_center_list) > 4:
                # Create WalledTissue2d from voronoi centers structure.
                self.create_wt2d_from_vc(remove_infinite_cells = True, constraints = (c1, c2)) 

            # Update properties from WalledTissue2d to polygonal mesh.
            self.update_properties_from_wt2d_to_pm(render_scene = render_scene, voronoi_changed = True)

    # Select voronoi center.
    def select_voronoi_center(self, voronoi_center):
        if voronoi_center:
            self._bw.prop3d = voronoi_center
            self._bw.center = voronoi_center.position
            
            # Hack to avoid crash.
            self._bw.place_widget(-2., -1., -2., -1., -2., -1.)
            
            self.scene_model.render()
            self._bw.place_widget()
            self.scene_model.render()
            
        self._selected_voronoi_center = voronoi_center

    # Remove voronoi center.
    def remove_voronoi_center(self, voronoi_center, render_scene = True, update_properties_from_wt2d_to_pm = True):
        self._voronoi_center_list.remove(voronoi_center)
        self.scene_model.remove_actor(voronoi_center)
        
        if self._voronoi_center_list:
            self.select_voronoi_center(self._voronoi_center_list[0])
        else:
            self.select_voronoi_center(None)
            
        if update_properties_from_wt2d_to_pm:
            a = self.actions["actions_add_voronoi_centers"]
                
            c1 = a.voronoi_centers_limit_left_bottom_position 
            c2 = a.voronoi_centers_limit_right_top_position
            
            if len(self._voronoi_center_list) > 4:
                # Create WalledTissue2d from voronoi centers structure.
                self.create_wt2d_from_vc(remove_infinite_cells = True, constraints = (c1, c2)) 

            # Update properties from WalledTissue2d to polygonal mesh.
            self.update_properties_from_wt2d_to_pm(render_scene = render_scene, voronoi_changed = True)

    # Remove voronoi centers.
    def remove_voronoi_centers(self, voronoi_center_list = [], render_scene = True, update_properties_from_wt2d_to_pm = True):
        self._voronoi_center_list = []
            
        self.select_voronoi_center(None)
        
        self.scene_model.disable_render = True
        self.scene_model.remove_actors(voronoi_center_list)
        self.scene_model.disable_render = False
        
        if render_scene: 
            self.scene_model.render()
            
        if update_properties_from_wt2d_to_pm:
            a = self.actions["actions_add_voronoi_centers"]
                
            c1 = a.voronoi_centers_limit_left_bottom_position 
            c2 = a.voronoi_centers_limit_right_top_position
            
            if len(self._voronoi_center_list) > 4:
                # Create WalledTissue2d from voronoi centers structure.
                self.create_wt2d_from_vc(remove_infinite_cells = True, constraints = (c1, c2)) 

            # Update properties from WalledTissue2d to polygonal mesh.
            self.update_properties_from_wt2d_to_pm(render_scene = render_scene, voronoi_changed = True)
        
    # Display tissue scalar properties.    
    def display_tissue_scalar_properties(self, property, render_scene = True, voronoi_changed = False):
        if voronoi_changed:
            print "voronoi changed"
            
            # Update properties from voronoi centers to WalledTissue2d.
            self.update_properties_from_vc_to_wt2d(self._voronoi_wt, self._voronoi_center_list, self.cell_properties)
    
        t = self._voronoi_wt
        cell_nbr = len(t.cells())
        prop_value = zeros(cell_nbr)
        
        max = -inf
        min = inf
        
        for i in range(cell_nbr):
            p = t.cell_property(self._cell_id_vtk2wt[i], property)
            
            prop_value[i] = p
            
            if p > max: max = p
            if p < min: min = p
        
        self._voronoi_vtk.cell_data.scalars = prop_value
        self._voronoi_vtk.cell_data.scalars.name = property
        
        self._voronoi_cell_polygons.parent.scalar_lut_manager.use_default_range = False
        
        if not self._cell_scalars_dynamic:
            self._voronoi_cell_polygons.parent.scalar_lut_manager.data_range = \
                array([float(self._cell_scalars_range[0]), float(self._cell_scalars_range[1])])
        else:
            self._voronoi_cell_polygons.parent.scalar_lut_manager.data_range = \
                array([min, max])
            
        if render_scene: 
            self._voronoi_vtk_ds.update()

    # Update colormap.
    @on_trait_change('_cell_scalars_active')
    def update_colormap(self, render_scene = True, voronoi_changed = True):
        if self._cell_scalars_active:
            if self._cell_scalars_active_name in self.cell_properties.keys():
                self.display_tissue_scalar_properties(self._cell_scalars_active_name, render_scene = False, voronoi_changed = voronoi_changed)
                
                if render_scene: 
                    self.scene_model.render()
    
    
    #--- Synchronization methods.
    
    # Update properties from WalledTissue2d to voronoi centers structure.
    def update_properties_from_wt2d_to_vc(self, wt2d, vc, properties):
        """Copies cell properties from WalledTissue2d to voronoi structure.
        :parameters:
            wt2d : `WalledTissue2d`
                Source of properties.
            vc : []
                Target of properties.
            properties : {}
                Properties to be synchronize."""
        
        synchronize_id_of_wt_and_voronoi(wt2d, vc)

        if not properties is None:
            for i in properties:
                try:
                    for j in vc:
                        if j.cell_id != -1:
                            j.__setattr__(i, wt2d.cell_property(j.cell_id, i))
                            
                except TraitError:
                    print " !: problem while synchronising wt2d->vc:", i  
    
    
    # Update properties from voronoi centers structure to WalledTissue2d.
    def update_properties_from_vc_to_wt2d(self, wt2d, vc, properties, init_properties = True):
        """Copies cell properties from voronoi structure to WalledTissue2d.
        :parameters:
            wt2d : `WalledTissue2d`
                Source of properties.
            vc : []
                Target of properties.
            properties : {}
                Properties to be synchronized."""
        
        synchronize_id_of_wt_and_voronoi(wt2d, vc)

        if not properties is None:
            for i in properties:
                if init_properties:
                    wt2d.init_cell_property(i, properties[i])
                    
                try:
                    for j in vc:
                        if j.cell_id != -1:
                            wt2d.cell_property(j.cell_id, i, j.__getattribute__(i))
                            
                except AttributeError:
                    print " !: problem while synchronising vc->wt2d:", i
    
    
    # Update properties from WalledTissue2d to polygonal mesh.
    def update_properties_from_wt2d_to_pm(self, render_scene = True, voronoi_changed = False, color=(0, 0, 0)):
        d = self.create_pm_from_wt2d(self._voronoi_wt)

        self._voronoi_vtk = d["tissue"]
        
        self._cell_id_vtk2wt = d["cell_id_vtk2wt"]
        self._cell_id_wt2vtk = d["cell_id_wt2vtk"]
        
        self._wv_id_wt2vtk = d["wv_id_wt2vtk"]
        self._wv_id_vtk2wv = d["wv_id_vtk2wt"]
        
        if not self._voronoi_vtk_ds:
            self._voronoi_vtk_ds = VTKDataSource(data = self._voronoi_vtk)
            
            engine = mlab.get_engine()
            engine.add_source(self._voronoi_vtk_ds)
            
            self._voronoi_cell_polygons = mlab.pipeline.surface(self._voronoi_vtk_ds, opacity = 0.99)
            self._voronoi_cell_edges = mlab.pipeline.surface(mlab.pipeline.extract_edges(self._voronoi_vtk_ds), color = color)
        else:
            self._voronoi_vtk_ds.data = self._voronoi_vtk
            self._voronoi_vtk_ds.update()
            
        if self._cell_scalars_active:
            if self._cell_scalars_active_name in self.cell_properties.keys():
                self.display_tissue_scalar_properties(self._cell_scalars_active_name, render_scene = False, voronoi_changed = voronoi_changed)
                
        if render_scene: self.scene_model.render()
    
    
    # Create WalledTissue2d from voronoi centers structure.
    def create_wt2d_from_vc(self, tissue_properties = None, remove_infinite_cells = False, constraints = None):
        """Allows to create the WalledTissue based on the information
        from two files: first one containg definitions of voronoi centers
        in the rbox format, second one containing the computed voronoi
        vertices (by qvoronoi).
        
        <Long description of the function functionality.>
        :parameters:
            arg1 : `T`
                <Description of `arg1` meaning>
        :rtype: `T`
        :return: <Description of ``return_object`` meaning>
        :raise Exception: <Description of situation raising `Exception`>"""
        
        (voronoi_centers, voronoi_edges) = voronoi_centers_to_edges(self.voronoi_centers())
        
        self._voronoi_wt = read_qhull2walled_tissue(voronoi_centers, voronoi_edges, tissue_properties, remove_infinite_cells, constraints)
    
    
    # Create polygonal mesh from WalledTissue2d.
    def create_pm_from_wt2d(self, wt2d = None):
        """Converts WalledTissue2d to vtkPolyData.
        <Long description of the function functionality.>
        :parameters:
            wt2d : `walled_tissue`
                Walled tissue to be converted.
        :rtype: `vtkPolyData`
        :return: Converted tissue."""
        
        # Setting wvs.
        wvs = tvtk.Points()
        
        wv_id_wt2vtk = {}
        wv_id_vtk2wt = {}
        
        for i in wt2d.wvs():
            wvs.insert_point(i, tuple(wt2d.wv_pos(i))) 
            
            id = i
            
            wv_id_vtk2wt[id] = i
            wv_id_wt2vtk[i] = id
            
        cell_id_wt2vtk = {}
        cell_id_vtk2wt = {}
        
        cells = tvtk.CellArray()
        
        for i in wt2d.cells():
            cs = wt2d.cell2wvs(i)
            id = cells.insert_next_cell(len(cs))
            
            for j in cs:
                cells.insert_cell_point(j)
                
            cell_id_wt2vtk[i] = id
            cell_id_vtk2wt[id] = i
        
        tissue = tvtk.PolyData(points = wvs, polys = cells)

        return {
            "tissue": tissue,
            "cell_id_vtk2wt": cell_id_vtk2wt,
            "cell_id_wt2vtk": cell_id_wt2vtk,
            "wv_id_vtk2wt": wv_id_vtk2wt,
            "wv_id_wt2vtk": wv_id_wt2vtk,
        }

