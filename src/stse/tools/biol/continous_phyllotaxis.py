#!/usr/bin/env python
"""Contains the definition of objects useful for modelling continous primordia.

<Long description of the module functionality.>

:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    INRIA

"""
# Module documentation variables:
__authors__="""Szymon Stoma    
"""
__contact__=""
__license__="Cecill-C"
__date__="<Timestamp>"
__version__="0.1"
__docformat__= "restructuredtext en"
__revision__="$Id$"

from openalea.plantgl.all import Vector3, norm
from openalea.stse.tools.my_math import new_argrument_for_given_curve_length
    
    
class ContinousPrimordiaManager (object):
    """The class managing the primordia in a continues medium.
    
    The shape of the
    meristem is defined by the profile function. The class provides the growth method
    which:
    1. displace the primordia,
    2. increase the size of primordia.
    Each primordium is represented by:
    1. radius
    2. direction
    3. size
    """

    class Primordium (object):
        """The class agregating the primordium data.
        
        Direction is used to move the primordium "on the right curve".
        The next displacement of the primordium depands on the amount of displacemnt
        already taken (this is due to the growth axiom of material).
        """
        def __init__( self, radius, direction, size, displacement ):
            self.radius = radius
            self.size = size
            self.direction = direction
            self.displacement = displacement
            
        def pos( self, f_profile, origin ):
            """Returns the 3d coord position of a primordium.
            
            <Long description of the function functionality.>
            
            :rtype: Vector3
            :return: Position calculated using radius, direction, profile function and displacement.
            """
            v = origin+self.direction*self.radius
            v.z = f_profile(self.radius)
            return v
            
        
            
    def __init__( self, f_profile=None, f_primordium_growth=None, c_remove_radius=5., c_origin=Vector3(), c_growth_speed=0.1,
                 c_primordium_initial_size=1., c_initial_primordium_displacement=1. ):
        """The basic init.
        
        <Long description of the function functionality.>
        
        :parameters:
            f_profile : function
                Function describing the profile. Should define profile of a meristem
                as a 1d function returning the altitude for a given radius.
            f_primordium_growth : function
                Function describing the growth of the size of th primordium. Should
                define the size of the primordium as a function of its altitude.
            c_remove_radius : float
                The radius value after exceeding which the primordium is removed
                from the meristem.
            c_origin: Vector3
                The center of the radial symetry of the meristem.
            c_growth_speed: float
                The growth speed coeficient.
            c_primordium_initial_size: float
                The initial size of the primordium.
            c_initial_primordium_displacement: float
                The initial amount of primordium displacement.
        """
        self.prims = {}
        self.f_profile = f_profile
        self.f_primordium_growth = f_primordium_growth
        self.c_remove_radius = c_remove_radius
        self.c_origin = c_origin
        self.c_growth_speed = c_growth_speed
        self.c_primordium_initial_size = c_primordium_initial_size
        self.c_initial_primordium_displacement = c_initial_primordium_displacement
        
    def add_primordium( self, pos, id ):
        """Adds primordium to the stucture.
        
        <Long description of the function functionality.>
        
        :parameters:
            pos : Vector3
                The position of the primordium
            id : int
                The unique id of the primordium.
        """
        direction = pos - self.c_origin
        direction.normalize()
        radius = norm(pos - self.c_origin)
        size=self.c_primordium_initial_size
        self.prims[ id ] = ContinousPrimordiaManager.Primordium(radius=radius, direction=direction,
                                                                size=size, displacement=self.c_initial_primordium_displacement)
        
    def growth( self ):
        """Perform one step of growth.
        
        <Long description of the function functionality.>
        
        """
        to_remove=[]
        for (i,p) in self.prims.iteritems():
            growth = p.displacement*self.c_growth_speed
            ndisplacement = p.displacement+growth
            nradius =  new_argrument_for_given_curve_length( self.f_profile,  p.radius, growth )
            nsize = self.f_primordium_growth( ndisplacement )
            
            p.displacement = ndisplacement
            p.radius = nradius
            p.size = nsize
    
            if p.radius > self.c_remove_radius:
                to_remove.append(i)    
            
        for i in to_remove:
            self.prims.pop( i )

if __name__ == "__main__":
    
    
    from math import cos, sin
    from openalea.plantgl.ext.all import AISphere
    from openalea.mersim.gui.tissue import create_meristem_stem
    
    def display(s, cpm):
        for i in s:
            i.visible = False
        l=[]
        for i in cpm.prims.values():
            l.append(AISphere(pos=i.pos(cpm.f_profile, cpm.c_origin),radius=i.size))
        return l
        
        
    cz=2.2
    f_profile=(lambda x:(-x*x +cz*cz)*10)
    c_remove_radius=5.
    create_meristem_stem(central_zone=cz, distance=c_remove_radius, profile_f=f_profile)
    cpm = ContinousPrimordiaManager(f_profile=f_profile, f_primordium_growth=(lambda x:2.), c_remove_radius=c_remove_radius)
    s=[]
    for i in range(10):
        x=Vector3(2.2*sin(i/10*2*3.14), 2.2*cos(i/10*2*3.14), 0)
        cpm.add_primordium(x, i)
        for j in range(5):
            cpm.growth()
            for p in cpm.prims.values():
                print p.pos(cpm.f_profile, cpm.c_origin), p.size
            print "end"
            s=display(s, cpm)
            raw_input()
