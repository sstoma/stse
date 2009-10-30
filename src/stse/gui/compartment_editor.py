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
from openalea.stse.tools.emergency import kill_close_points
from openalea.stse.tools.convex_hull import int_points_in_polygon, xy_minimal_bounding_box_of_polygon
from openalea.stse.structures.algo.walled_tissue import \
    calculate_cell_surface
from openalea.stse.gui.voronoi_aplications import VoronoiCenterVisRep, \
    VoronoiCenterVisRepGeneral, MyScene, MyAction, general_cell_properties, \
    default_voronoi_factory, general_voronoi_factory, CompartmentWindow, \
    FileLoadBackgroundImage, ActionsUpdateVoronoiEdges, FileLoadWalledTissue \

# ---------------------------------------------------------------------- ACTIONS

        
class ActionsAddVoronoiCenters(MyAction):
    method = Enum("Grid", "Random")
    voronoi_centers_limit_left_bottom_position = Tuple(0., 0.)
    voronoi_centers_limit_right_top_position = Tuple(100., 100.)
    voronoi_centers_add_number = Int(100)

    def perform_calc( self ):
        if self.method == "Grid":
            a = self._application
            p=[]
            (xmin,ymin) = self.voronoi_centers_limit_left_bottom_position
            (xmax,ymax) = self.voronoi_centers_limit_right_top_position
            x_range = xmax-xmin
            y_range = ymax-ymin
            area = x_range*y_range
            small_area = area/ float(self.voronoi_centers_add_number)
            delta = math.sqrt( small_area )
            x_nbr = int(x_range / delta)
            y_nbr = int(y_range / delta)
            for i in range( x_nbr ):
                for j in range( y_nbr ):
                    p.append( ( (j%2)*delta/2.+xmin+(delta/2.)+i*delta, (ymin+(delta/2.)+j*delta), 0. ) )
            a.add_voronoi_centers( pos_list=p, render_scene=False )    
            a.scene_model.render()
        elif self.method == "Random":
            a = self._application
            p=[]
            (xmin,ymin) = self.voronoi_centers_limit_left_bottom_position
            (xmax,ymax) = self.voronoi_centers_limit_right_top_position
            x_range = xmax-xmin
            y_range = ymax-ymin
            for i in range( self.voronoi_centers_add_number ):
                p.append( (xmin+x_range*random.random(), ymin+y_range*random.random(), 0.) )
            a.add_voronoi_centers( pos_list=p, render_scene=False )    
            a.scene_model.render()
    
    def set_bounds(self, xmin, xmax,ymin,ymax):
        self.voronoi_centers_limit_left_bottom_position = (xmin, ymin)
        self.voronoi_centers_limit_right_top_position = (xmax,ymax)
        
    def default_traits_view( self ):
        """Description of default view.
        """
        view = View(
            VGroup(
                Item(
                    "method",
                ),
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
                Item(
                    "perform_btn",
                    show_label = False,
                ),
                show_border = True,
                label = 'Add Voronoi centers',
            ),
        )
        return view

        
class ActionsAddMembrane(MyAction):
    p1 = Array(Float, (2,1) )
    p2 = Array(Float, (2,1) )
    number_of_points = Int(10)
    thickness = Float(10.)
    click_counter = Int(0)
    inside_type = Str('B')
    outside_type = Str('A')
    
    def default_traits_view( self ):
        """Description of default view.
        """
        view = View(
            VGroup(
                Item(
                    "p1",
                    label="Start point",
                    style="readonly",
                ),
                Item(
                    "p2",
                    label="End point",
                    style="readonly",
                ),
                Item(
                    "number_of_points",
                    label="# points",
                ),
                Item(
                    "thickness",
                    label="membrane thickness",
                    # Number of voronoi centers to add
                ),
                Item(
                    "inside_type",
                    label="inside cell type",
                    # Number of voronoi centers to add
                ),
                Item(
                    "outside_type",
                    label="outside cell type",
                    # Number of voronoi centers to add
                ),
                Item(
                    "perform_btn",
                    show_label = False,               
                ),
                show_border = True,
                label = 'Add membrane',
            ),
        )
        return view
    
    def set_point( self, point ):
        if self.click_counter == 0:
            self.p1[0] = point[0]
            self.p1[1] = point[1]
            self.click_counter = 1
            self.trait_property_changed('p1', self.p1)
        else:
            self.p2[0] = point[0]
            self.p2[1] = point[1]
            self.click_counter = 0
            self.trait_property_changed('p2', self.p1)   
    
    def perform_calc(self):
        a = self._application
        op=[]
        ip=[]
        dir_x = self.p2[0] - self.p1[0]
        dir_y = self.p2[1] - self.p1[1]
        norm_per = math.sqrt( dir_x*dir_x+dir_y*dir_y)
        per_x = -dir_y / norm_per * self.thickness / 2.
        per_y = dir_x / norm_per * self.thickness / 2.
        
        n = float(self.number_of_points)
        for i in range( self.number_of_points ):
            for j in [-1, 1]:
                op.append( ( float(self.p1[0]+i*dir_x/n+j*per_x), float(self.p1[1]+i*dir_y/n+j*per_y), 0.))
            ip.append( ( float(self.p1[0]+i*dir_x/n), float(self.p1[1]+i*dir_y/n), 0.))
        a.add_voronoi_centers( pos_list=ip, render_scene=False, cell_type=self.inside_type )    
        a.add_voronoi_centers( pos_list=op, render_scene=False, cell_type=self.outside_type )    
        a.scene_model.render()
        




class ActionsCalculateAverageExpression(MyAction):
    expression_name = Str("custom_cell_property1")
    red_channel = Bool(True)
    green_channel = Bool(True)
    blue_channel = Bool(True)

    def __init__(self, **kwargs):
        """Init"""
        super(ActionsCalculateAverageExpression, self).__init__( **kwargs )
        #self.expression_name = Enum( kwargs["cell_properties"].keys() )
        
    def perform_calc(self):
        """Calculate average expression level based on the image.""" 
        a = self._application
        t = a._voronoi_wt
        
        # checking if there is one cell or more
        if len( t.cells() ) == 0:
            print " !: Add more voronoi centers to have non empty mesh"
            return
        
        if not a.cell_properties.has_key( self.expression_name ):
            print " !: Specify an existing cell property name in Corresponding property"
            return
        
        t.init_cell_property( self.expression_name, a.cell_properties[ self.expression_name ] )
        
        #i = t.cells()[ 0 ]
        for i in t.cells():
            cs = t.cell2wvs( i )
            cs_pos = map( t.wv_pos, cs)
            pl = int_points_in_polygon( cs_pos )
            exp = 0.
            for j in pl:
                ind = a._bg_image.actor.input.find_point(j[0], j[1], 0)
                d = a._bg_image.actor.input.point_data.scalars[ ind ]
                if self.green_channel:
                    exp += d[ 0 ]
                if self.red_channel:
                    exp += d[ 1 ]
                if self.blue_channel:
                    exp += d[ 2 ]
            surf  = calculate_cell_surface( t, i )
            t.cell_property( i, self.expression_name, exp / surf)
        
        synchronize_id_of_wt_and_voronoi(a._voronoi_wt, a._voronoi_center_list)
        copy_cell_properties_from_wt_to_voronoi( a._voronoi_wt, a._voronoi_center_list, [self.expression_name])
        
        
    def default_traits_view( self ):
        """Description of default view.
        """
        view = \
        View(
            VGroup(
                #Item(
                #    "expression_name",
                #    #editor=InstanceEditor(),
                #    style='simple',
                #),
                Item(
                    "expression_name",
                    label = "Corresponding property",
                ),
                Item(
                    "red_channel"
                ),
                Item(
                    "green_channel"
                ),
                Item(
                    "blue_channel"
                ),
                Item(
                    "perform_btn",
                    show_label = False,               
                ),
                show_border = True,
                label = 'Calculate expressions',
            ),
        )
        return view
    
    
class ActionsCleanVoronoi(MyAction):
    distance = Float(0.1)
    def perform_calc(self):
        """Kills voronoi centers too close to each other."""
        a = self._application
        kill_close_points(a._voronoi_center_list, self.distance )

    def default_traits_view( self ):
        """Description of default view.
        """
        view = \
        View(
            VGroup(
                Item(
                    "distance",
                ),
                Item(
                    "perform_btn",
                    show_label = False,               
                ),
            )
        )
        return view
    


class ViewSwitchCutPlane(MyAction):
    def perform(self):
        """swith"""
        a = self._application
        a._cut_plane.enabled = not a._cut_plane.enabled
        


class FileSaveWalledTissue(MyAction):
    def perform(self):
        """Pops up a dialog used to save WalledTissue."""
        a = self._application
        dlg = FileDialog( action='save as',
                wildcard='*', title="Save WalledTissue")
        
        if dlg.open() == OK:
            t = a._voronoi_wt
            
            # kill double voronoi
            kill_close_points(a._voronoi_center_list, 0.1)
            
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


# ------------------------------------------------------------------ APPLICATION

                
class CompartmentEditorWindow( CompartmentWindow ):
    def register_actions( self ):
        super(CompartmentEditorWindow, self).register_actions()
        # defining menu/toolbar positions
        # note: they can be shared
        
        action_add_voronoi_centers = ActionsAddVoronoiCenters(
                parent=self,
                name = "Add voronoi centers",
                action = "self.perform",
                toolip = "Adds  voronoi centers to the current scene",
                )
        self.actions["action_add_voronoi_centers"] =action_add_voronoi_centers
                
        actions_add_membrane = ActionsAddMembrane(
            parent=self,
            name = "Add membrane",
            toolip = "Adds voronoi centers creating thin membrane between points", 
            action = "self.perform",
        )
        self.actions["actions_add_membrane"] =actions_add_membrane
        
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
        
        actions_clean_voronoi = ActionsCleanVoronoi(
            parent=self,
            name = "Removes voronoi placed too close to each other",
            toolip = "Removes voronoi closer than given distance to each other", 
            action = "self.perform",
        )
        self.actions["actions_clean_voronoi"] = actions_clean_voronoi
        
        actions_calculate_average_expression = ActionsCalculateAverageExpression(
            parent=self,
            name = "Calculates expressions",
            toolip = "Calculates the avarege expression for each cell in a mesh based on the image", 
            action = "self.perform",
            cell_properties = self.cell_properties,
        )
        self.actions["actions_calculate_average_expression"] = actions_calculate_average_expression

        view_switch_cut_plane = ViewSwitchCutPlane(
            parent=self,
            name = "Cut plane ON/OFF",
            toolip = "Switches cut plane ON/OFF", 
            action = "self.perform",
        )
        self.actions["view_switch_cut_plane"] = view_switch_cut_plane

    
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
            title='Compartment Editor',
            resizable=True,
            width=800,
            height=600,
            # defining menubar content
            menubar = MenuBarManager(
                MenuManager(
                    self.actions[ "file_load_background_image" ],
                    self.actions[ "file_save_walled_tissue" ],
                    self.actions[ "file_load_walled_tissue" ],
                    name = '&File',
                ),
                MenuManager(
                    self.actions[ "action_add_voronoi_centers" ],
                    self.actions[ "actions_update_voronoi_edges" ],
                    self.actions[ "actions_add_membrane" ],
                    self.actions[ "actions_clean_voronoi" ],
                    self.actions[ "actions_calculate_average_expression" ],
                    name = '&Actions',
                ),
                MenuManager(
                    self.actions[ "view_switch_cut_plane" ],
                    name = '&View',
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
        self._bw = tvtk.SphereWidget(interactor=self.scene_model.interactor, place_factor=1.3)
        if len(self._voronoi_center_list):
            self._bw.prop3d=self._voronoi_center_list[0]
            self.select_voronoi_center( self._voronoi_center_list[0] )
            self._bw.scale = False
            self._bw.place_widget()
            
        # setting up image clipper
        self._cut_plane = tvtk.BoxWidget(interactor=self.scene_model.interactor)
        #self._cut_plane.place_widget()
        self._cut_plane.off()
        self._cut_plane.scaling_enabled=1
        self._cut_plane.rotation_enabled=0
        def clipper_edit_event(widget, event):
            """This callback sets the """
            pl = tvtk.Planes()
            self._cut_plane.get_planes( pl )
            xmin, xmax, ymin, ymax = xy_minimal_bounding_box_of_polygon( pl.points )
            self.actions[ "action_add_voronoi_centers" ].set_bounds(xmin, xmax,ymin,ymax)
        self._cut_plane.add_observer("EndInteractionEvent", clipper_edit_event)
        
        def callback_end(widget, event):
            """This callback sets the """
            if self._bw.prop3d:
                self._bw.prop3d.position = self._bw.center
                self.update_vtk_from_voronoi( render_scene=True, voronoi_changed=True )                   
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
                x = self.add_voronoi_center(pos=(d.coordinate[ 0 ], d.coordinate[ 1 ], 0.) )
                # crash!
                #self.select_voronoi_center( x )
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

        # adding an membrane end - key 'm'
        def membrane_callback(widget, event):
            """Alternative right mouse click callback"""
            if widget.GetKeyCode() == 'm':
                pos = widget.GetEventPosition()
                d = self.scene_model.picker.pick_point(pos[ 0 ], pos[ 1 ])
                self.actions["actions_add_membrane"].set_point( d.coordinate )
                #self.event_w = widget
        self.scene_model.interactor.add_observer("KeyPressEvent", membrane_callback)

        # adding an membrane end - key 'm'
        self.default_cell_type = "outside"
        def custom_callback(widget, event):
            """Changing cell type to self.default_cell_type"""
            if widget.GetKeyCode() == 'n':
                rmc2_callback( widget, event )
                self._selected_voronoi_center.cell_type = self.default_cell_type
        self.scene_model.interactor.add_observer("KeyPressEvent", custom_callback)

        # comment it if you would like "normal" 3d interactor instead of the one
        # described in __doc__
        self.scene_model.interactor.interactor_style = \
            tvtk.InteractorStyleImage()
        
        self.scene_model.parallel_projection=True
        
        self._voronoi_vtk_ds = None
        
        self.scene_model.anti_aliasing_frames = 0

    def update_vtk_from_voronoi( self, render_scene=True, voronoi_changed = True):
        if len( self._voronoi_center_list ) > 4:
            if voronoi_changed:
                (i,o) = voronoi_centers_to_edges( self.voronoi_centers() )
                a = self.actions[ "action_add_voronoi_centers" ]
                c1 = a.voronoi_centers_limit_left_bottom_position 
                c2 = a.voronoi_centers_limit_right_top_position
                self._voronoi_wt = read_qhull2walled_tissue(i, o, remove_infinite_cells=True, constraints=(c1, c2) ) 
            super(CompartmentEditorWindow, self).update_vtk_from_voronoi( render_scene=render_scene, voronoi_changed=voronoi_changed )
            
            
def mesh_editing():
    return CompartmentEditorWindow()

def general_editing():
    return CompartmentEditorWindow( voronoi_factory=general_voronoi_factory, \
        cell_properties=general_cell_properties)    


if __name__ == '__main__':
    # Create and open an application window.
    #window = mesh_editing()
    window = general_editing()
    window.edit_traits()
    window.do()
    GUI().start_event_loop()

        
