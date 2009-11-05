#!/usr/bin/env python
"""Application allowing for 2D tissue viewing.

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
__date__="Thu Aug 13 11:45:26 CEST 2009"
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
    on_trait_change, Color, HTML, Enum, Tuple, Int, Bool, Array, Float, Any, Str

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

import os
import os.path

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
from openalea.stse.gui.voronoi_aplications import VoronoiCenterVisRep, \
    VoronoiCenterVisRepGeneral, MyScene, MyAction, general_cell_properties, \
    default_voronoi_factory, general_voronoi_factory, CompartmentWindow, \
    FileLoadBackgroundImage, ActionsUpdateVoronoiEdges, FileLoadWalledTissue \


# ---------------------------------------------------- GUI DATASTRUCTURE CLASSES
    

# ---------------------------------------------------------------------- ACTIONS

        
class FileLoadWalledTissueSerie(MyAction):
    def perform(self):
        """Pops up a dialog used to load WalledTissue series"""
        a = self._application
        extns = ['*']
        dlg = DirectoryDialog( action='open',
                wildcard='|'.join(extns), title="Load WalledTissue serie")
        
        if dlg.open() == OK:
            dirname = dlg.path
            for i in [f for f in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, f))]:
                print " #: loading ", i
                a.remove_all_voronoi_centers( update_vtk_from_voronoi=False )
                a._voronoi_wt = read_walled_tissue( file_name=os.path.join(dirname, i) )        

                #pos_list = []
                #for i in a._voronoi_wt.cells():
                #    pos_list.append( a._voronoi_wt.cell_property(i, "voronoi_center" ) )
                #for i in a._voronoi_wt.tissue_property("outside_voronoi_centers"):
                #    pos_list.append( i )
                #
                #a.add_voronoi_centers( pos_list=pos_list, render_scene=False, \
                #    update_vtk_from_voronoi=False )
                #
                ##updates the properties of voronoi centers with WalledTissue properties 
                #
                #synchronize_id_of_wt_and_voronoi(a._voronoi_wt, a._voronoi_center_list)
                #copy_cell_properties_from_wt_to_voronoi( a._voronoi_wt, \
                #    a._voronoi_center_list, a._voronoi_wt.const.cell_properties )
                #
                a.update_vtk_from_voronoi()

                a.display_tissue_scalar_properties(property=a._cell_scalars_active_name)
                a.scene_model.save_png(os.path.join(dirname, str(i)+".png") )            


class FileSaveWalledTissue(MyAction):
    def perform(self):
        """Pops up a dialog used to save WalledTissue."""
        a = self._application
        extns = ['*']
        dlg = FileDialog( action='save as',
                wildcard='|'.join(extns), title="Save WalledTissue")
        
        if dlg.open() == OK:
            t = a._voronoi_wt
            saved_tissue = write_walled_tissue( tissue=a._voronoi_wt, name=dlg.path, desc="Test tissue" )


# ------------------------------------------------------------------ APPLICATION

                
class CompartmentViewerWindow( CompartmentWindow ):
    def register_actions( self ):
        super(CompartmentViewerWindow, self).register_actions()
        # defining menu/toolbar positions
        # note: they can be shared
        
        file_load_background_image = FileLoadBackgroundImage(
                parent=self,
                name = "Load background",
                toolip = "Loads background image file to the current scene",            
                action = "self.perform",
        )
        self.actions["file_load_background_image"] =file_load_background_image
                
        file_load_walled_tissue = FileLoadWalledTissue(
            parent=self,
            name = "Load WalledTissue",
            toolip = "Loads WalledTissue", 
            action = "self.perform",
        )
        self.actions["file_load_walled_tissue"] =file_load_walled_tissue
        
        file_save_walled_tissue = FileSaveWalledTissue(
            parent=self,
            name = "Save WalledTissue",
            toolip = "Saves WalledTissue", 
            action = "self.perform",
        )
        self.actions["file_save_walled_tissue"] =file_save_walled_tissue
        
        file_load_walled_tissue_serie = FileLoadWalledTissueSerie(
            parent=self,
            name = "Load WalledTissue serie",
            toolip = "Loads a serie of walled tissue simulations", 
            action = "self.perform",
        )
        self.actions["file_load_walled_tissue_serie"] = file_load_walled_tissue_serie
    
    def default_traits_view( self ):
        """Description of default view.
        """
        self.register_actions()
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
                        Item(
                            '_selected_action',
                            style='custom',
                            editor=InstanceEditor(),
                            label='',
                            show_label=False,
                        ),
                        show_border = True,
                        label = 'Actions',
                    ),
                    VGroup(
                        Item(
                            "voronoi_center_size",
                            label="Voronoi center size",
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
                            enabled_when='not _cell_scalars_dynamic',
                        ),
                        Item(
                            "_cell_scalars_dynamic",
                            label = "Use auto Min/Max value",
                        ),
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
            title='Compartment Viewer',
            resizable=True,
            width=800,
            height=600,
            # defining menubar content
            menubar = MenuBarManager(
                MenuManager(
                    self.actions[ "file_load_background_image"],
                    self.actions[ "file_save_walled_tissue"],
                    self.actions[ "file_load_walled_tissue"],
                    self.actions[ "file_load_walled_tissue_serie"],
                    name = '&File',
                ),
                MenuManager(
                    name = '&Actions',
                ),
            ),
            ## defining toolbar content
            #toolbar= ToolBarManager(
            #    file_load_background_image,
            #),
        )
        return view

                               
                                   
    def do( self ):
        """Sets the application after initialization.
        """
        self._bw = tvtk.SphereWidget(interactor=self.scene_model.interactor, place_factor=1.05)
        if len(self._voronoi_center_list):
            self._bw.prop3d=self._voronoi_center_list[0]
            self.select_voronoi_center( self._voronoi_center_list[0] )
            self._bw.scale = False
            self._bw.place_widget()
        self._bw.on()
        self._bw.translation = 0
        
        # switching the spheres using picker - key 'p'
        def rmc2_callback(widget, event):
            """Alternative right mouse click callback"""
            if self.scene_model.picker.pointpicker.actor in self._voronoi_center_list:
                self.select_voronoi_center( self.scene_model.picker.pointpicker.actor )
        self.scene_model.picker.pointpicker.add_observer("PickEvent", rmc2_callback)
        self.scene_model.picker.show_gui = False
        
        # comment it if you would like "normal" 3d interactor instead of the one
        # described in __doc__
        self.scene_model.interactor.interactor_style = \
            tvtk.InteractorStyleImage()
        
        self.scene_model.parallel_projection=True
        
        self._voronoi_vtk_ds = None
        
        self.scene_model.anti_aliasing_frames = 0


def mesh_viewing():
    returnCompartmentViewerWindow()

def general_viewing():
    return CompartmentViewerWindow( voronoi_factory=general_voronoi_factory, \
        cell_properties=general_cell_properties)    

def start_gui():
    # Create and open an application window.
    window = general_viewing()
    window.edit_traits()
    window.do()
    GUI().start_event_loop()

if __name__ == '__main__':
    start_gui() 
        
