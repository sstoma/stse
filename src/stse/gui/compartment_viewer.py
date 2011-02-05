#!/usr/bin/env python

"""Application allowing for 2D tissue viewing.
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
__date__ = "Thu Aug 13 11:45:26 CEST 2009"
__version__ = "0.1"
__docformat__ = "restructuredtext en"


# ----------------------------------IMPORTS-----------

import random
import math

from numpy import array, zeros

from enthought.pyface.api import FileDialog, DirectoryDialog, GUI, OK, ImageResource
from enthought.pyface.action.api import Action, MenuBarManager, MenuManager, ToolBarManager

from enthought.traits.api import Instance, HasTraits, Range, \
    on_trait_change, Color, HTML, Enum, Tuple, Int, Bool, Array, Float, Any, Str

from enthought.tvtk.pyface.scene_editor import SceneEditor
from enthought.tvtk.api import tvtk

from enthought.traits.ui.api import View, Item, VGroup,  Tabbed, HSplit, InstanceEditor

from enthought.mayavi.tools.mlab_scene_model import MlabSceneModel
from enthought.mayavi.core.ui.mayavi_scene import MayaviScene
from enthought.mayavi import mlab
from enthought.mayavi.sources.vtk_data_source import VTKDataSource
from enthought.mayavi.modules.image_actor import ImageActor

from vtk.util import colors

import os
import os.path

from openalea.stse.structures.walled_tissue import WalledTissue
from openalea.stse.io.walled_tissue.native_representation import write_walled_tissue, read_walled_tissue

from openalea.stse.tools.convex_hull import int_points_in_polygon, xy_minimal_bounding_box_of_polygon

from openalea.stse.gui.voronoi_aplications import VoronoiCenterVisRep, VoronoiCenterVisRepGeneral, MyScene, MyAction, \
    general_cell_properties, default_voronoi_factory, general_voronoi_factory, CompartmentWindow
    
    
# ----------------------------------MENU ACTIONS------


# ------------------------
# menubar: "File"


# "Load background."
class FileLoadBackgroundImage(MyAction):
    """Load background image."""
    
    # Perform button.
    def perform(self):
        """Pops up a dialog used to load a background image."""
        extns = ['*.bmp', '*.png', '*.tif', '*.jpg', '*']
        dlg = FileDialog(action = 'open',
                wildcard = '*', title = "Load image")
        
        if dlg.open() == OK:
            self.__load_image(dlg.path)
    
    # Private method called by perform button.
    def __load_image(self, file_name):
        """Loads image to GUI."""
        a = self._application
        engine = mlab.get_engine()
        
        if not a._bg_image_reader:
            a._bg_image_reader = engine.open(file_name)
            a._bg_image = mlab.pipeline.image_actor(a._bg_image_reader)
        else:
            a._bg_image.remove()
            a._bg_image_reader.remove()
            a._bg_image_reader = engine.open(file_name)
            a._bg_image = mlab.pipeline.image_actor(a._bg_image_reader)
            
        a._bg_image.module_manager.scalar_lut_manager.lut_mode = 'gray'
        
        (x1, x2) = a._bg_image.actor.x_range
        (y1, y2) = a._bg_image.actor.y_range
        
        if a.actions.has_key("actions_add_voronoi_centers"):
            act = a.actions["actions_add_voronoi_centers"]
            a._cut_plane.place_widget(x1, x2, y1, y2, 0., 0.)
            
            act.voronoi_centers_limit_left_bottom_position = (x1, y1)
            act.voronoi_centers_limit_right_top_position = (x2, y2)
            
        return a._bg_image_reader


# "Save WalledTissue."
class FileSaveWalledTissue(MyAction):
    """Save WalledTissue."""
    
    # Perform button.
    def perform(self):
        """Pops up a dialog used to save WalledTissue."""
        a = self._application
        extns = ['*']
        
        dlg = FileDialog(action = 'save as',
                wildcard = '|'.join(extns), title = "Save WalledTissue")
        
        if dlg.open() == OK:
            t = a._voronoi_wt
            saved_tissue = write_walled_tissue(tissue = a._voronoi_wt, name = dlg.path, desc = "Test tissue")


# "Load WalledTissue."
class FileLoadWalledTissue(MyAction):
    """Load WalledTissue."""
    
    # Perform button.
    def perform(self):
        """Pops up a dialog used to load WalledTissue."""
        a = self._application
        dlg = DirectoryDialog(action = 'open',
                wildcard = '*', title = "Load WalledTissue")
        
        if dlg.open() == OK:
            self.load(dlg.path)
    
    # Method called by perform button.
    def load(self, path):
            """Load WalledTissue."""
            a = self._application
            
            # TODO: Add reading properties to voronoi center class.
            a.remove_all_voronoi_centers(update_properties_from_wt2d_to_pm = False)
            a._voronoi_wt = read_walled_tissue(file_name = path)
                
            pos_list = []
            for i in a._voronoi_wt.cells():
                pos_list.append(a._voronoi_wt.cell_property(i, "voronoi_center"))
                
            for i in a._voronoi_wt.tissue_property("outside_voronoi_centers"):
                pos_list.append(i)
            
            a.add_voronoi_centers(pos_list = pos_list, render_scene = False, update_properties_from_wt2d_to_pm = False)

            # Update properties from WalledTissue2d to voronoi centers structure.
            a.update_properties_from_wt2d_to_vc(a._voronoi_wt, a._voronoi_center_list, a._voronoi_wt.const.cell_properties)
             
            # Update properties from WalledTissue2d to polygonal mesh.
            a.update_properties_from_wt2d_to_pm(voronoi_changed = False)


# "Load WalledTissueSerie."
class FileLoadWalledTissueSerie(MyAction):
    """Load WalledTissueSerie."""
    
    # Perform button.
    def perform(self):
        """Pops up a dialog used to load WalledTissue series."""
        a = self._application
        extns = ['*']
        
        dlg = DirectoryDialog(action = 'open',
                wildcard = '|'.join(extns), title = "Load WalledTissue serie")
        
        if dlg.open() == OK:
            dirname = dlg.path
            for i in [f for f in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, f))]:
                print " #: loading ", i
                
                a.remove_all_voronoi_centers(update_properties_from_wt2d_to_pm = False)
                a._voronoi_wt = read_walled_tissue(file_name = os.path.join(dirname, i))        

                a.update_properties_from_wt2d_to_pm()

                a.display_tissue_scalar_properties(property = a._cell_scalars_active_name)
                
                a.scene_model.save_png(os.path.join(dirname, str(i) + ".png"))            


# ----------------------------------APPLICATION------


# Compartment window.
class CompartmentViewerWindow(CompartmentWindow):
    """Compartment window"""
    
    # Register menu actions.
    def register_actions(self):
        """Defining menubar positions."""
        # ---Defining menubar: "File".
        
        # "Load background."
        file_load_background_image = FileLoadBackgroundImage(
            parent = self,
            name = "Load background",
            toolip = "Loads background image file to the current scene",            
            action = "self.perform",
        )
        self.actions["file_load_background_image"] = file_load_background_image
        
        # "Save WalledTissue." 
        file_save_walled_tissue = FileSaveWalledTissue(
            parent = self,
            name = "Save WalledTissue",
            toolip = "Saves WalledTissue", 
            action = "self.perform",
        )
        self.actions["file_save_walled_tissue"] = file_save_walled_tissue
        
        # "Load WalledTissue."
        file_load_walled_tissue = FileLoadWalledTissue(
            parent = self,
            name = "Load WalledTissue",
            toolip = "Loads WalledTissue", 
            action = "self.perform",
        )
        self.actions["file_load_walled_tissue"] = file_load_walled_tissue
        
        # "Load WalledTissueSerie."
        file_load_walled_tissue_serie = FileLoadWalledTissueSerie(
            parent = self,
            name = "Load WalledTissue serie",
            toolip = "Loads a serie of walled tissue simulations", 
            action = "self.perform",
        )
        self.actions["file_load_walled_tissue_serie"] = file_load_walled_tissue_serie
    
    # Register listeners.
    def do(self):
        """Sets the application after initialization."""
        
        self._bw = tvtk.SphereWidget(interactor = self.scene_model.interactor, place_factor = 1.05)
        
        if len(self._voronoi_center_list):
            self._bw.prop3d = self._voronoi_center_list[0]
            self.select_voronoi_center(self._voronoi_center_list[0])
            
            self._bw.scale = False
            self._bw.place_widget()
            
        self._bw.on()
        self._bw.translation = 0
        
        # Switching the spheres using picker - key 'p'.
        def rmc2_callback(widget, event):
            """Alternative right mouse click callback"""
            if self.scene_model.picker.pointpicker.actor in self._voronoi_center_list:
                self.select_voronoi_center(self.scene_model.picker.pointpicker.actor)
                
        self.scene_model.picker.pointpicker.add_observer("PickEvent", rmc2_callback)
        self.scene_model.picker.show_gui = False
        
        # Comment it if you would like "normal" 3d interactor instead of the on described in __doc__.
        self.scene_model.interactor.interactor_style = tvtk.InteractorStyleImage()
        self.scene_model.parallel_projection=True
        self._voronoi_vtk_ds = None
        self.scene_model.anti_aliasing_frames = 0
    
    # Prepare default view. Main Window.
    def default_traits_view(self):
        """Description of default view."""
        self.register_actions()
        
        view = View(
            HSplit(
                Item(
                    name = 'scene_model',
                    editor = SceneEditor(
                        # Custom scene is used to get rid of default scene toolbar.
                        scene_class = MayaviScene,
                    ),
                    show_label = False,
                ),
                Tabbed(
                    VGroup(
                        Item(
                            '_selected_action',
                            style = 'custom',
                            editor = InstanceEditor(),
                            label = '',
                            show_label = False,
                        ),
                        show_border = True, label = 'Actions',
                    ),
                    VGroup(
                        Item(
                            "voronoi_center_size",
                            label = "Voronoi center size",
                        ),
                        Item(
                            "_cell_scalars_active",
                            label = "Display cell property",
                        ),
                        Item(
                            "_cell_scalars_active_name",
                            label = "Name of disp. prop.",
                        ),
                        Item(
                            "_cell_scalars_range",
                            label = "Min/Max value of disp. prop.",
                            enabled_when = 'not _cell_scalars_dynamic',
                        ),
                        Item(
                            "_cell_scalars_dynamic",
                            label = "Use auto Min/Max value",
                        ),
                        show_border = True, label = 'Visualisation',
                    ),
                    VGroup(
                        Item(
                            name = '_selected_voronoi_center',
                            editor = InstanceEditor(),
                            enabled_when = '_selected_voronoi_center is not None',
                            style = 'custom',
                            label = '',
                            show_label = False,
                        ),
                        show_border = True, label = 'Selected center',
                    ),
                    VGroup(
                        Item(
                            name = '_help',
                            show_label = False,
                        ),
                        show_border = True, label = 'Help',
                    ),
                ),
            ),
            # Specyfing type of the window.
            kind = 'live', title = 'Compartment Viewer', resizable = True,
            width = 800, height = 600,
            menubar = MenuBarManager(
                # ---menubar: "File".
                MenuManager(
                    self.actions["file_load_background_image"],
                    self.actions["file_save_walled_tissue"],
                    self.actions["file_load_walled_tissue"],
                    self.actions["file_load_walled_tissue_serie"],
                    name = '&File',
                ),
                # ---menubar: "Actions".
                MenuManager(
                    name = '&Actions',
                ),
            ),
        )
        
        return view

    # Update colormap.
    def update_colormap(self, render_scene = True, voronoi_changed = False):
        if self._cell_scalars_active:
            if self._cell_scalars_active_name in self.cell_properties.keys():
                self.display_tissue_scalar_properties(self._cell_scalars_active_name, render_scene = False, voronoi_changed = voronoi_changed)
                if render_scene: 
                    self.scene_model.render()

    # Update colormap.
    @on_trait_change('_cell_scalars_active')
    def update_colormap_on_cell_scalars_active_change(self, render_scene = True, voronoi_changed = False):
        if self._cell_scalars_active:
            if self._cell_scalars_active_name in self.cell_properties.keys():
                # To workaround the bug in Traits voronoi_changed has to be set to False not with the default option but explicitly.
                self.display_tissue_scalar_properties(self._cell_scalars_active_name, render_scene = False, voronoi_changed = False)
                if render_scene: 
                    self.scene_model.render()


# Start application.
def start_gui():
    """Start application."""
    
    # Create and open an application window.
    window = CompartmentViewerWindow(voronoi_factory = general_voronoi_factory, cell_properties = general_cell_properties)  
    
    window.edit_traits()
    window.do()
    GUI().start_event_loop()
    
    return window


if __name__ == '__main__':
    start_gui() 
        
