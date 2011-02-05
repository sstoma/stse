# !/usr/bin/env python

"""Application allowing for 2D tissue digitalization.
:todo:
    To be revied by somebody skillfull in VTK/TraitsUI/tvtk.
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

from numpy import array, zeros

from enthought.pyface.api import FileDialog, DirectoryDialog, GUI, OK, ImageResource
from enthought.pyface.action.api import Action, MenuBarManager, MenuManager, ToolBarManager

from enthought.traits.api import Instance, HasTraits, Range, on_trait_change, Color, HTML, \
    Enum, Tuple, Int, Bool, Array, Float, Any, Str, Button
from enthought.traits.ui.api import View, Item, VGroup, Tabbed, HSplit, InstanceEditor, HGroup

from enthought.tvtk.pyface.scene_editor import SceneEditor
from enthought.tvtk.api import tvtk

from enthought.mayavi.tools.mlab_scene_model import MlabSceneModel
from enthought.mayavi.core.ui.mayavi_scene import MayaviScene
from enthought.mayavi import mlab
from enthought.mayavi.sources.vtk_data_source import VTKDataSource
from enthought.mayavi.modules.image_actor import ImageActor

from vtk.util import colors

from openalea.stse.io.walled_tissue.native_representation import write_walled_tissue, read_walled_tissue

from openalea.stse.structures.walled_tissue import WalledTissue
from openalea.stse.structures.algo.walled_tissue import calculate_cell_surface
    
from openalea.stse.tools.convex_hull import int_points_in_polygon, xy_minimal_bounding_box_of_polygon

from openalea.stse.gui.voronoi_aplications import VoronoiCenterVisRep, VoronoiCenterVisRepGeneral, \
    MyScene, MyAction, general_cell_properties, default_voronoi_factory, general_voronoi_factory, \
    CompartmentWindow
    
from openalea.stse.tools.emergency import kill_close_points


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
        dlg = FileDialog(action = 'save as',
                wildcard = '*', title = "Save WalledTissue")
        
        if dlg.open() == OK:
            self.__save(dlg.path)
    
    # Private method called by perform button.
    def __save(self, file_name):
        """Save WalledTissue."""
        a = self._application
        t = a._voronoi_wt
        
        # Kill double voronoi.
        kill_close_points(a._voronoi_center_list, 0.1)
        
        # Update properties from voronoi centers to WalledTissue2d.
        a.update_properties_from_vc_to_wt2d(a._voronoi_wt, a._voronoi_center_list, a.cell_properties)

        ovc = []
        for i in a._voronoi_center_list:
            if i.cell_id != -1:
                t.cell_property(i.cell_id, "voronoi_center", i.position)
            else:
                ovc.append(i.position)
                
        t.tissue_property("outside_voronoi_centers", ovc)
        
        saved_tissue = write_walled_tissue(tissue = a._voronoi_wt, name = file_name, desc = "Test tissue")


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
            self.__load(dlg.path)
    
    # Private method called by perform button.
    def __load(self, path):
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


# ------------------------
# menubar: "Actions"


# "Add voronoi centers."
class ActionsAddVoronoiCenters(MyAction):
    """Add voronoi centers."""
    
    # Create form fields.
    method = Enum("Grid", "Random")
    voronoi_centers_limit_left_bottom_position = Tuple(0., 0.)
    voronoi_centers_limit_right_top_position = Tuple(100., 100.)
    voronoi_centers_add_number = Int(100)

    # Prepare default view.
    def default_traits_view(self):
        """Description of default view."""
        view = View(
            VGroup(
                Item(
                    "method",
                ),
                Item(
                   "voronoi_centers_limit_left_bottom_position",
                   label = "Left bottom",
                ),
                Item(
                   "voronoi_centers_limit_right_top_position",
                   label = "Right top",
                ),
                Item(
                    # Number of voronoi centers to add.
                   "voronoi_centers_add_number",
                   label = "# centers",
                ),
                Item(
                    "perform_btn",
                    show_label = False,
                ),
                show_border = True, label = 'Add Voronoi centers',
            ),
        )
        
        return view

    # Perform button.
    def perform_calc(self):
        """Add voronoi centers."""
        if self.method == "Grid":
            a = self._application
            p = []
            
            (xmin, ymin) = self.voronoi_centers_limit_left_bottom_position
            (xmax, ymax) = self.voronoi_centers_limit_right_top_position
            
            x_range = xmax - xmin
            y_range = ymax - ymin
            area = x_range * y_range
            small_area = area / float(self.voronoi_centers_add_number)
            delta = math.sqrt(small_area)

            x_nbr = int(x_range / delta)
            y_nbr = int(y_range / delta)
            
            for i in range(x_nbr):
                for j in range(y_nbr):
                    p.append(((j % 2) * delta / 2. + xmin + (delta / 2.) + i * delta, (ymin + (delta / 2.) + j * delta), 0.))
                    
            a.add_voronoi_centers(pos_list = p, render_scene = False)    
            a.scene_model.render()
        elif self.method == "Random":
            a = self._application
            p = []
            
            (xmin, ymin) = self.voronoi_centers_limit_left_bottom_position
            (xmax, ymax) = self.voronoi_centers_limit_right_top_position
            
            x_range = xmax-xmin
            y_range = ymax-ymin
            
            for i in range(self.voronoi_centers_add_number):
                p.append((xmin + x_range * random.random(), ymin + y_range * random.random(), 0.))
                
            a.add_voronoi_centers(pos_list = p, render_scene = False)    
            a.scene_model.render()
     
    # Set centers position.
    def set_bounds(self, xmin, xmax, ymin, ymax):
        """Set bounds."""
        self.voronoi_centers_limit_left_bottom_position = (xmin, ymin)
        self.voronoi_centers_limit_right_top_position = (xmax, ymax)


# "Update voronoi edges."
class ActionsUpdateVoronoiEdges(MyAction):
    """Produces and displays the voronoi edges."""
    
    # Create form fields.
    inside_type = Str('No configuration options')
    
    # Prepare default view.
    def default_traits_view(self):
        """Description of default view."""
        view = View(
            VGroup(
                Item(
                    "inside_type",
                    show_label = False, 
                    style = "readonly",
                ),
                Item(
                    "perform_btn",
                    show_label = False,
                ),
                show_border = False, label = '',
            ),
        )
        
        return view
        
    # Perform button.
    def perform_calc(self):
        """ Performs the action. """
        a = self._application
        
        # Update properties from WalledTissue2d to polygonal mesh.
        a.update_properties_from_wt2d_to_pm(render_scene = True)
    

# "Add membrane."
class ActionsAddMembrane(MyAction):
    """Add membrane."""
    
    # Create form fields.
    p1 = Array(Float, (2,1))
    p2 = Array(Float, (2,1))
    number_of_points = Int(10)
    thickness = Float(10.)
    click_counter = Int(0)
    inside_type = Str('B')
    outside_type = Str('A')

    # Prepare default view.
    def default_traits_view(self):
        """Description of default view."""
        view = View(
            VGroup(
                Item(
                    "p1",
                    label = "Start point",
                    style = "readonly",
                ),
                Item(
                    "p2",
                    label = "End point",
                    style = "readonly",
                ),
                Item(
                    "number_of_points",
                    label = "# points",
                ),
                Item(
                    # Number of voronoi centers to add.
                    "thickness",
                    label = "membrane thickness",
                ),
                Item(
                    # Number of voronoi centers to add.
                    "inside_type",
                    label = "inside cell type",
                ),
                Item(
                    # Number of voronoi centers to add.
                    "outside_type",
                    label = "outside cell type",
                ),
                Item(
                    "perform_btn",
                    show_label = False,               
                ),
                show_border = True, label = 'Add membrane',
            ),
        )
        
        return view

    # Perform button.
    def perform_calc(self):
        """Add membrane."""
        a = self._application
        op = []
        ip = []
        
        dir_x = self.p2[0] - self.p1[0]
        dir_y = self.p2[1] - self.p1[1]
        norm_per = math.sqrt(dir_x * dir_x + dir_y * dir_y)
        
        per_x = -dir_y / norm_per * self.thickness / 2.
        per_y = dir_x / norm_per * self.thickness / 2.
        
        n = float(self.number_of_points)
        for i in range(self.number_of_points):
            for j in [-1, 1]:
                op.append((float(self.p1[0] + i * dir_x / n + j * per_x), float(self.p1[1] + i * dir_y / n + j * per_y), 0.))
            ip.append((float(self.p1[0] + i * dir_x / n), float(self.p1[1] + i * dir_y / n), 0.))
            
        a.add_voronoi_centers(pos_list = ip, render_scene = False, cell_type = self.inside_type)    
        a.add_voronoi_centers(pos_list = op, render_scene = False, cell_type = self.outside_type) 
        
        a.scene_model.render()
        
    # Set point.
    def set_point(self, point):
        """Set point."""
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


# "Removes voronoi placed too close to each other."
class ActionsCleanVoronoi(MyAction):
    """Removes voronoi placed too close to each other."""
    
    # Create form fields.
    distance = Float(0.1)
    
    # Prepare default view.
    def default_traits_view(self):
        """Description of default view."""
        view = View(
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
    
    # Perform button.
    def perform_calc(self):
        """Kills voronoi centers too close to each other."""
        a = self._application
        
        kill_close_points(a._voronoi_center_list, self.distance)


# "Calculates expressions."
class ActionsCalculateAverageExpression(MyAction):
    """Calculates expressions."""
    
    # Create form fields.
    expression_name = Str("custom_cell_property1")
    red_channel = Bool(True)
    green_channel = Bool(True)
    blue_channel = Bool(True)
    use_surface = Bool(False)

    # Init.    
    def __init__(self, **kwargs):
        """Init."""
        super(ActionsCalculateAverageExpression, self).__init__(**kwargs)

    # Prepare default view.
    def default_traits_view(self):
        """Description of default view."""
        view = View(
            VGroup(
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
                    "use_surface"
                ),
                Item(
                    "perform_btn",
                    show_label = False,               
                ),
                show_border = True, label = 'Calculate expressions',
            ),
        )
        
        return view

    # Perform button.
    def perform_calc(self):
        """Calculate average expression level based on the image.""" 
        a = self._application
        t = a._voronoi_wt
        
        # Checking if there is one cell or more.
        if len(t.cells()) == 0:
            print "!: Add more voronoi centers to have non empty mesh."
            return
        
        if not a.cell_properties.has_key(self.expression_name):
            print "!: Specify an existing cell property name in Corresponding property."
            return
        
        t.init_cell_property(self.expression_name, a.cell_properties[self.expression_name])
        
        try:
            #TODO: Add searching for nb. of proc.
            limit = 8
            
            import pprocess
            results = pprocess.pmap(self.__calculate_expression_in_cell, t.cells(), limit = limit)
            
            for i in results:
                t.cell_property(i[0], i[1], i[2])
                
        except Exception:
            print "#: Waning: not using multiple cores. Verify python-pprocess installation..."
            
            for i in t.cells():
                j = self.__calculate_expression_in_cell(i)
                t.cell_property(j[0], j[1], j[2])
        
        # Update properties from WalledTissue2d to voronoi centers structure.
        a.update_properties_from_wt2d_to_vc(a._voronoi_wt, a._voronoi_center_list, [self.expression_name])
        
    # Private method called by perform button.
    def __calculate_expression_in_cell(self, cell):
        """Caluculates average expression in given cell."""
        a = self._application
        t = a._voronoi_wt
        cs = t.cell2wvs(cell)
        cs_pos = map(t.wv_pos, cs)
        pl = int_points_in_polygon(cs_pos)
        exp = 0.
        
        for j in pl:
            ind = a._bg_image.actor.input.find_point(j[0], j[1], 0)
            d = a._bg_image.actor.input.point_data.scalars[ind]
            
            try:
                if self.green_channel:
                    exp += d[0]
                if self.red_channel:
                    exp += d[1]
                if self.blue_channel:
                    exp += d[2]
            except TypeError:
                exp += d
        
        if self.use_surface:        
            surf = calculate_cell_surface(t, cell)
            
            return cell, self.expression_name, exp / surf
        else: return cell, self.expression_name, exp / len(pl)


# "Define cell types."
class ActionsDefineCellTypes(MyAction):
    """Define cell types."""
    
    # Create form fields.
    cell_type = Str("B")
    filename = Str("")
    load_filename = Button(label = 'Select file')
   
    # Init.
    def __init__(self, **kwargs):
        """Init"""
        super(ActionsDefineCellTypes, self).__init__(**kwargs)
   
    # Prepare default view.
    def default_traits_view( self ):
        """Description of default view."""
        view = View(
            VGroup(
                Item(
                    "cell_type",
                    label = "Cell type",
                ),
                Item(
                    "perform_btn",
                    show_label = False,               
                ),
                show_border = True, label = 'Define cell types',
            ),
        )
        
        return view
   
    # Perform button.
    def perform_calc(self):
        """Calculate average expression level based on the image.""" 
        a = self._application
        t = a._voronoi_wt
        
        # Checking if there is one cell or more.
        if len(t.cells()) == 0:
            print "!: Add more voronoi centers to have non empty mesh"
            return

        # Update properties from WalledTissue2d to voronoi centers structure.
        a.update_properties_from_wt2d_to_vc(a._voronoi_wt, a._voronoi_center_list, None)
        
        self.vc2cell_type = {}
        
        for i in a._voronoi_center_list:
            self.vc2cell_type[i.cell_id] = i.cell_type
        
        try:
            #TODO: Add searching for nb. of proc.
            limit = 8
            
            import pprocess
            results = pprocess.pmap(self.__define_cell_type, t.cells(), limit = limit)
            
            for i in results:
                t.cell_property(i[0], i[1], i[2])
        except Exception:
            print "#: Warning: not using multiple cores. Verify python-pprocess installation..."
            
            for i in t.cells():
                j = self.__define_cell_type(i)
                t.cell_property(j[0], j[1], j[2])
        
        # Update properties from WalledTissue2d to voronoi centers structure.
        a.update_properties_from_wt2d_to_vc(a._voronoi_wt, a._voronoi_center_list, ['cell_type'])

    # Private method called by perform button.
    def __define_cell_type(self, cell):
        """Define cell type."""
        a = self._application
        t = a._voronoi_wt
        img = a._bg_image
        cs = t.cell2wvs(cell)
        cs_pos = map(t.wv_pos, cs)
        pl = int_points_in_polygon(cs_pos)
        exp = 0.
        
        for j in pl:
            ind = img.actor.input.find_point(j[0], j[1], 0)
            d = img.actor.input.point_data.scalars[ind]
            
            try:
                exp += d[0] + d[1] + d[2]
            except TypeError: 
                exp += d 
                
            if exp > 0: break
                
        if exp > 0:    
            t.cell_property(cell, "cell_type", self.cell_type)
            
            return cell, "cell_type", self.cell_type
        else:
            t.cell_property(cell, "cell_type",  self.vc2cell_type[cell])
            
            return cell, "cell_type", self.vc2cell_type[cell]
        
    # Runs default action.
    def _load_filename_fired(self):
        """Runs default action."""
        a = self._application
        dlg = FileDialog(action = 'open',
                wildcard = '*', title = "Load binary image")
        
        if dlg.open() == OK:
            self.filename = dlg.path


# ------------------------
# menubar: "View"


# "Cut plane ON/OFF."
class ViewSwitchCutPlane(MyAction):
    """Cut plane ON/OFF."""
    
    # Perform button.
    def perform(self):
        """Switch."""
        a = self._application
        a._cut_plane.enabled = not a._cut_plane.enabled
        

# ----------------------------------APPLICATION------


# Compartment window.
class CompartmentEditorWindow(CompartmentWindow):
    """Compartment window"""
    
    # Register menu actions.
    def register_actions(self):
        """Defining menubar positions."""
        # ---Defining menubar: "File".
        
        # "Load background."
        self.actions["file_load_background_image"] = FileLoadBackgroundImage(
            parent = self,
            name = "Load background",
            action = "self.perform",
            toolip = "Load background image.",
        )
        
        # "Save WalledTissue." 
        self.actions["file_save_walled_tissue"] = FileSaveWalledTissue(
            parent = self,
            name = "Save WalledTissue",
            action = "self.perform",
            toolip = "Saves WalledTissue.",
        )
        
        # "Load WalledTissue."
        self.actions["file_load_walled_tissue"] = FileLoadWalledTissue(
            parent = self,
            name = "Load WalledTissue",
            action = "self.perform",
            toolip = "Loads WalledTissue.", 
        )
        
        
        # ---Defining menubar: "Actions".
        
        # "Add voronoi centers."
        self.actions["actions_add_voronoi_centers"] = ActionsAddVoronoiCenters(
            parent = self,
            name = "Add voronoi centers",
            action = "self.perform_calc",
            toolip = "Adds  voronoi centers to the current scene.",
        )
        
        # "Update voronoi edges."
        self.actions["actions_update_voronoi_edges"] = ActionsUpdateVoronoiEdges(
            parent = self,
            name = "Update voronoi edges",
            action = "self.perform_calc",
            toolip = "Update voronoi edges.",
        )

        # "Add membrane."
        self.actions["actions_add_membrane"] = ActionsAddMembrane(
            parent = self,
            name = "Add membrane",
            action = "self.perform_calc",
            toolip = "Adds voronoi centers creating thin membrane between points.", 
        )
        
        # "Removes voronoi placed too close to each other."
        self.actions["actions_clean_voronoi"] = ActionsCleanVoronoi(
            parent = self,
            name = "Removes voronoi placed too close to each other",
            action = "self.perform_calc",
            toolip = "Removes voronoi closer than given distance to each other.", 
        )
        
        # "Calculates expressions."
        self.actions["actions_calculate_average_expression"] = ActionsCalculateAverageExpression(
            parent = self,
            name = "Calculates expressions",
            action = "self.perform_calc",
            toolip = "Calculates the avarege expression for each cell in a mesh based on the image.", 
            cell_properties = self.cell_properties,
        )
        
        # "Define cell types."
        self.actions["actions_define_cell_types"] = ActionsDefineCellTypes(
            parent = self,
            name = "Define cell types",
            action = "self.perform_calc",
            toolip = "Allows to define cell types from a file.", 
        )
        
        
        # ---Defining menubar: "View".
        
        # "Cut plane ON/OFF."
        self.actions["view_switch_cut_plane"] = ViewSwitchCutPlane(
            parent = self,
            name = "Cut plane ON/OFF",
            action = "self.perform",
            toolip = "Switches cut plane ON/OFF.", 
        )

    # Register listeners.
    def do(self):
        """Defining listeners. Sets the application after initialization."""
        self._bw = tvtk.SphereWidget(interactor = self.scene_model.interactor, place_factor = 1.3)
        
        if len(self._voronoi_center_list):
            self._bw.prop3d=self._voronoi_center_list[0]
            self.select_voronoi_center(self._voronoi_center_list[0])
            self._bw.scale = False
            self._bw.place_widget()
            
        # Setting up image clipper.
        self._cut_plane = tvtk.BoxWidget(interactor = self.scene_model.interactor)
        
        self._cut_plane.off()
        self._cut_plane.scaling_enabled = 1
        self._cut_plane.rotation_enabled = 0
        
        def clipper_edit_event(widget, event):
            """This callback sets the..."""
            pl = tvtk.Planes()
            self._cut_plane.get_planes(pl)
            xmin, xmax, ymin, ymax = xy_minimal_bounding_box_of_polygon(pl.points)
            self.actions["actions_add_voronoi_centers"].set_bounds(xmin, xmax, ymin, ymax)
            
        self._cut_plane.add_observer("EndInteractionEvent", clipper_edit_event)

        def callback_end(widget, event):
            """This callback sets the..."""
            if self._bw.prop3d:
                self._bw.prop3d.position = self._bw.center
                
                a = self.actions["actions_add_voronoi_centers"]
                
                c1 = a.voronoi_centers_limit_left_bottom_position 
                c2 = a.voronoi_centers_limit_right_top_position
                
                if len(self._voronoi_center_list) > 4:
                    # Create WalledTissue2d from voronoi centers structure.
                    self.create_wt2d_from_vc(remove_infinite_cells = True, constraints = (c1, c2)) 

                # Update properties from WalledTissue2d to polygonal mesh.
                self.update_properties_from_wt2d_to_pm(render_scene = True, voronoi_changed = True)
                
        self._bw.add_observer("EndInteractionEvent", callback_end)
        self._bw.on()
        
        # Switching the spheres using picker - key 'p'.
        def rmc2_callback(widget, event):
            """Alternative right mouse click callback."""
            if self.scene_model.picker.pointpicker.actor in self._voronoi_center_list:
                self.select_voronoi_center(self.scene_model.picker.pointpicker.actor)
                
        self.scene_model.picker.pointpicker.add_observer("PickEvent", rmc2_callback)
        self.scene_model.picker.show_gui = False
        
        # Region picking  - key 'b'.
        def pick_voronoi_region_callback(widget, event):
            """Alternative right mouse click callback."""
            if widget.GetKeyCode() == 'b':
                pos = widget.GetEventPosition()
                self.d = self.scene_model.picker.pick_cell(pos[0], pos[1])

        self.scene_model.interactor.add_observer("KeyPressEvent", pick_voronoi_region_callback)

        # Adding a sphere using key interaction - key 'z'.
        def add_actor_callback(widget, event):
            """Alternative right mouse click callback."""
            if widget.GetKeyCode() == 'z':
                pos = widget.GetEventPosition()
                d = self.scene_model.picker.pick_point(pos[0], pos[1])
                x = self.add_voronoi_center(pos = (d.coordinate[0], d.coordinate[1], 0.))

        self.scene_model.interactor.add_observer("KeyPressEvent", add_actor_callback)
        
        # Adding a sphere using key interaction - key 'x'.
        def remove_voronoi_center_callback(widget, event):
            """Removes selected voronoi center."""
            if widget.GetKeyCode() == 'x':
                if self._selected_voronoi_center:
                    self.remove_voronoi_center(self._selected_voronoi_center)
                    if self._voronoi_center_list:
                        self.select_voronoi_center(self._voronoi_center_list[0])
                        
        self.scene_model.interactor.add_observer("KeyPressEvent", remove_voronoi_center_callback)
        
        # Removing all voronoi centers - key 'c'.
        def remove_all_voronoi_centers_callback(widget, event):
            """Removes selected voronoi center."""
            if widget.GetKeyCode() == 'c':
                self.remove_all_voronoi_centers()
                
        self.scene_model.interactor.add_observer("KeyPressEvent", remove_all_voronoi_centers_callback)
        
        # Adsding an membrane end - key 'm'.
        def membrane_callback(widget, event):
            """Alternative right mouse click callback."""
            if widget.GetKeyCode() == 'm':
                pos = widget.GetEventPosition()
                d = self.scene_model.picker.pick_point(pos[0], pos[1])
                self.actions["actions_add_membrane"].set_point(d.coordinate)
                
        self.scene_model.interactor.add_observer("KeyPressEvent", membrane_callback)
        
        # Adding an membrane end - key 'm'.
        self.default_cell_type = "outside"
        
        def custom_callback(widget, event):
            """Changing cell type to self.default_cell_type."""
            if widget.GetKeyCode() == 'n':
                rmc2_callback(widget, event)
                self._selected_voronoi_center.cell_type = self.default_cell_type
                
        self.scene_model.interactor.add_observer("KeyPressEvent", custom_callback)
        
        # Comment it if you would like "normal" 3d interactor instead of the one described in __doc__.
        self.scene_model.interactor.interactor_style = tvtk.InteractorStyleImage()
        self.scene_model.parallel_projection = True
        self._voronoi_vtk_ds = None
        self.scene_model.anti_aliasing_frames = 0
        
    # Prepare default view. Main Window.
    def default_traits_view(self):
        """Description of default view."""
        self.register_actions()
        
        # Specifying the layout of the window.
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
                        show_border = True, label = 'Actions', selected = True, 
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
                        show_border = True, label = 'Visualisation', selected = False, 
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
                        show_border = True, label = 'Selected center', selected = False, 
                    ),
                    VGroup(
                        Item(
                            name = '_help',
                            show_label = False,
                        ),
                        show_border = True, label = 'Help', selected = False, 
                    ),
                ),
            ),
            # Specyfing type of the window.
            kind = 'live', title = 'Compartment Editor', resizable = True,
            width = 800, height = 600,
            menubar = MenuBarManager(
                # ---menubar: "File".
                MenuManager(
                    self.actions["file_load_background_image"],
                    self.actions["file_save_walled_tissue"],
                    self.actions["file_load_walled_tissue"],
                    name = '&File',
                ),
                # ---menubar: "Actions".
                MenuManager(
                    self.actions["actions_add_voronoi_centers"],
                    self.actions["actions_update_voronoi_edges"],
                    self.actions["actions_add_membrane"],
                    self.actions["actions_clean_voronoi"],
                    self.actions["actions_calculate_average_expression"],
                    self.actions["actions_define_cell_types"],
                    name = '&Actions',
                ),
                # ---menubar: "View".
                MenuManager(
                    self.actions["view_switch_cut_plane"],
                    name = '&View',
                ),
            ),
            # Defining toolbar content.
            toolbar = ToolBarManager(
                self.actions["file_load_background_image"],
            ),
        )
        
        return view
 
 
# Start application.
def start_gui():
    """Start application."""
    
    # Create and open an application window.
    window = CompartmentEditorWindow(voronoi_factory = general_voronoi_factory, cell_properties = general_cell_properties)  
    
    window.edit_traits()
    window.do()
    GUI().start_event_loop()
    
    return window


if __name__ == '__main__':
    window = start_gui()        
        
        