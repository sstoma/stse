#!/usr/bin/env python

"""GUI window allowing to edit compartments. The editing is performed using
Voronoi diagrams. 

"""
# Author: Szymon Stoma


from enthought.pyface.api import GUI
from enthought.traits.api import HasTraits, Tuple
from enthought.tvtk.tools import ivtk
#from enthought.tvtk.pyface import actors
from enthought.tvtk.api import tvtk
from vtk.util import colors
import numpy
import random

import openalea.stse.io.qhull
import openalea.stse.structures.utils.qhull

from enthought.pyface.action.api import Action, Group, MenuBarManager, MenuManager, Separator




class VoronoiCenterActorGenerator:
    
    def __init__( self, center=(0, 0, 0), radius=0.01, resolution=32 ):
        """Brief synopsis
    
        A longer explanation.
                
        :param arg1: the first value
        :returns: 
        :rtype: 
        """
        self.source = tvtk.SphereSource(center=center, radius=radius,
                                   theta_resolution=resolution,
                                   phi_resolution=resolution)
        self.mapper = tvtk.PolyDataMapper(input=self.source.output)
    
    
    def actor(self, color=colors.purple, opacity=1.0):
        """ Creates a sphere and returns the actor. """
        prop = tvtk.Property(opacity=opacity, color=color)
        actor = tvtk.Actor(mapper=self.mapper, property=prop)
        return actor

### START callbacks
class KeyPressInCEWindowCallback:
    
    def __init__( self, compartment_editor_gui ):
        """Brief synopsis
    
        A longer explanation.
                
        :param arg1: the first value
        :returns: 
        :rtype: 
        """
        self.compartment_editor_gui = compartment_editor_gui
    
    def __call__( self, widget, event):
        """Alternative right mouse click callback"""
        if widget.GetKeyCode() == '1':
            self.compartment_editor_gui.add_voronoi_center()
        if widget.GetKeyCode() == '2':
            pass #remove_sphere_actor()
    
class PickVoronoiCenterWithRMCCallback:
    
    def __init__( self, compartment_editor_gui ):
        """Brief synopsis
    
        A longer explanation.
                
        :param arg1: the first value
        :returns: 
        :rtype: 
        """
        self.compartment_editor_gui = compartment_editor_gui
    
    def __call__( self, widget, event):
        """Right mouse click callback"""
        if self.compartment_editor_gui.window.scene.picker.pointpicker.actor in self.compartment_editor_gui.voronoi_center_widget_list:
                self.compartment_editor_gui.bw.prop3d = self.compartment_editor_gui.window.scene.picker.pointpicker.actor
                self.compartment_editor_gui.bw.center = self.compartment_editor_gui.bw.prop3d.position
                self.compartment_editor_gui.bw.place_widget()
                self.compartment_editor_gui.window.scene.render()

class DragVoronoiCenterCallback:
    
    def __init__( self, compartment_editor_gui ):
        """Brief synopsis
    
        A longer explanation.
                
        :param arg1: the first value
        :returns: 
        :rtype: 
        """
        self.compartment_editor_gui = compartment_editor_gui
    
    def __call__( self, widget, event):
        """Alternative right mouse click callback"""
        self.compartment_editor_gui.bw.prop3d.position = self.compartment_editor_gui.bw.center

### END callbacks
class TestAction(Action):
    """ Exits the application. """
    def __init__(self, window):
        """ Creates a new action. """
        self._window = window
        self.name = "E&xit"

    def perform(self):
        """ Performs the action. """
        self._window.close()
        
class Compartment_Editor_GUI:
    
    def __init__( self, nbr_actors=10 ):
        ### basic display
        self.gui = GUI()
        self.window = ivtk.IVTK(size=(800,600))
        self.window.open()
        
        # adding voronoi center generator
        self.voronoi_center_actor_generator = VoronoiCenterActorGenerator()
        
        # adding 10 random actors
        self.voronoi_center_widget_list = []
        for i in range(nbr_actors):
            self.add_voronoi_center( pos=(random.random()-0.5, random.random()-0.5, 0.000001*random.random()))
             
        ### EVENTS
        # moving the voronoi centers by dragging
        self.bw = tvtk.SphereWidget(interactor=self.window.scene.interactor, place_factor=1.25)
        self.bw.prop3d=self.voronoi_center_widget_list[0]
        self.bw.scale = False
        self.bw.place_widget()
        self.bw.add_observer("EndInteractionEvent", DragVoronoiCenterCallback( self ) )
        self.bw.on()
        
        # switching the selected voronoi center using picker 'p'
        self.window.scene.picker.pointpicker.add_observer("PickEvent", PickVoronoiCenterWithRMCCallback( self ) )
        self.window.scene.picker.show_gui = False
        
        # key interactions
        # '1' adds new voronoi center
        # '2' removes selected voronoi
        self.window.scene.interactor.add_observer("KeyPressEvent", KeyPressInCEWindowCallback( self ))
        
        # creating the scene
        self.window.scene.reset_zoom()
        self.gui.start_event_loop()
        
        
        self.window.menu_bar_manager = MenuBarManager(
            MenuManager(
                TestAction(self.window),
                name = '&File',
            ),
            MenuManager(
                TestAction(self.window),
                name = '&Edit',
            ),
            MenuManager(
                TestAction(self.window),
                name = '&Edit',
            ),
        )

    def add_voronoi_center(self, pos=(0,0,0) ):
        """Brief synopsis
    
        A longer explanation.
                
        :param arg1: the first value
        :returns: 
        :rtype: 
        """
        self.voronoi_center_widget_list.append( self.voronoi_center_actor_generator.actor() )
        self.voronoi_center_widget_list[-1].position = pos
        self.window.scene.add_actor( self.voronoi_center_widget_list[-1] )


if __name__=="__main__":
    app = Compartment_Editor_GUI()

