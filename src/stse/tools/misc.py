#!/usr/bin/env python
"""Misc tools used in mersim project.

Here different code tools should be gathered. In the future it should be split depanding on the function.

:todo:
    drop: from numpy import *
    from pylab import *
    from vtk_pylab import *

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

import math
import copy
from numpy import *
from pylab import *
#from vtk_pylab import *

def permutation_lazy( str ):
    """Returns generator of permutations of the list str.
    """
    if len(str) <=1:
        yield str
    else:
        for perm in WalledTissue._all_perms( str[1:] ):
            for i in range(len(perm)+1):
                yield perm[:i] + str[0:1] + perm[i:]

def pair_fit( p1, p2):
    """Checks whether two pairs share one point.
    
    <Long description of the function functionality.>
    
    :parameters:
        p1 : ``2tuple``
            First pair.
        p2 : ``2tuple``
            Second pair.
    :rtype: `bool`
    :return: True iff pairs share a point. 
    :raise Exception: <Description of situation raising `Exception`>
    """
    return p1[0] == p2[0] or p1[0] == p2[1] or p1[1] == p2[0] or p1[1] == p2[1] 

def upe( p1, p2 ):
    """Unordered pair equal(upe) Returns true if 
    p1 = (s1, t1) and p2 = (s2, t2) and ( ( s1 = s2 and t1 = t2) or ( s1 = t2 and t1 = s2) ).
    """
    s1, t1 = p1
    s2, t2 = p2
    return ( s1 == s2 and t1 == t2) or ( s1 == t2 and t1 == s2)

def get_ordered_vertices_from_unordered_shape( edge_list ):
    r = [edge_list[ 0 ]]
    edge_list = edge_list[1:]
    while len( edge_list ):
        for i in range( len( edge_list ) ):
            if pair_fit( r[-1], edge_list[ i ]):
                r.append( edge_list[ i ] )
                edge_list.remove( edge_list[ i ] )
                break
        #if i ==  len( edge_list ):
        #    raise Exception("wrong shape prerequirements.")
    return get_ordered_vertices( r )[:-1]


def get_ordered_vertices( edge_list ):
    """By example: Gets the list of ordered edges written with **unordered** pair list and
    returns same edge list but with **ordered** pairs.
    input: [(1,2). (2,3), (3,4), (5,4), (6,5), (1,6)]
    output:[(1,2). (2,3), (3,4), (4,5), (5,6), (6,1)]
    """
    begin, end = edge_list[ 0 ]
    res = [ begin, end ]
    el = edge_list[1:]
    while len(el) != 0:
        for e in el:
            b = False
            for z in [0, 1]:
                if e[ z ] == begin:
                    res = [ e[ (z + 1) % 2 ] ] + res
                    begin = e[ (z + 1) % 2 ]
                    el.remove( e )
                    b = True
                    break
                if e[ z ] == end:
                    res = res + [ e[ (z + 1) % 2 ] ]
                    end = e[ (z + 1) % 2 ]
                    el.remove( e )
                    b = True
                    break
            if b: break
    return res


def find_edge_order( s1, t1, shape):
    """Returns the order of s1 and t1 based on the one in the list the list. If the pair 
    can not be found returns None.

    :Exception KeyError: If the edge is not found in shape.
    """
    ls = len( shape )
    for i in range( ls ):
        if shape[ i%ls ] == s1 and shape[ (i+1)%ls ] == t1:
            return s1, t1
        if shape[ i%ls ] == t1 and shape[ (i+1)%ls ] == s1:
            return t1, s1
    # like exception..
    KeyError("Edge not found in find_edge_order")

def find_edges_order( s1, t1, s2, t2, shape):
    """Returns the order of precedence of  s1, t1 and s2, t2 in the list.
    
    :Exception KeyError: If *both* pairs don't exist. It might be confusing with the situation
    when only one edge exists.
    """
    ls = len( shape )
    for i in range( ls ):
        if shape[ i%ls ] == s1 and shape[ (i+1)%ls ] == t1:
            return s1, t1, s2, t2
        if shape[ i%ls ] == s2 and shape[ (i+1)%ls ] == t2:
            return s2, t2, s1, t1
    raise KeyError("Vertices not found in find_edges_order")

def nearest_point( X, Y, (x,y) ):
    """Returns index of point which is nearest to (x,y). Checked points are: (X[i],Y[i]) 
    """
    minp=float("infinity")
    min_ind = 0
    for i in range(len( X ) ):
        z = math.sqrt( (X[i]-x)**2 + (Y[i]-y)**2 )
        if z < minp:
            minp=z
            min_ind=i
            
    #print minp, (X[min_ind],Y[min_ind]), (x,y)
    #raw_input()
    return min_ind


def create_grid_from_discret_values( X,Y,Z, sizeX=100, sizeY=100 ):
    """Creates a rectangular grid from a list of given values (x,y,z). A grid is rectangular
    and has the  coordinates (min(x),min(y)) -> (max(x),max(y)). The distance between
    nodes is equal and depands on the sizeX/Y parameter.
    
    TODO: not optimal. Slow.
    """

    xmin=min(X)
    xmax=max(X)
    ymin=min(Y)
    ymax=max(Y)
    xrange=xmax-xmin
    yrange=ymax-ymin
    
    #Zt = zeros(len(X))
    grid = zeros((sizeX,sizeY))
    
    for i in range(sizeX):
        for j in range(sizeY):
            grid[i][j] = Z[ nearest_point(X,Y, (xmin+i*xrange/sizeX,ymin+j*yrange/sizeY)) ]
    
    return (arange(xmin,xmax,xrange/sizeX),arange(ymin,ymax,yrange/sizeY),grid)

def plot_3d_height_map1( V ):
    X,Y,Z = [],[],[]
    for i in V:
        X.append(i.x)
        Y.append(i.y)
        Z.append(i.z)
    plot_3d_height_map( X, Y, Z )

def plot_3d_height_map_using_vtk( X,Y,Z ):
    X,Y=meshgrid(X,Y)
    mesh(X,Y,Z,1)
    vtkRender()
    vtkImage()
    imshow(im,None)
    show()

def plot_3d_height_map( X, Y, Z ):
    import pylab as p
    import matplotlib.axes3d as p3

    # in mplt3D change: 
    # levels, colls = self.contourf(X, Y, Z, 20)
    # to:
    # C = self.contourf(X, Y, Z, *args, **kwargs)
    # levels, colls = (C.levels, C.collections)
    
    fig=p.figure()
    ax = p3.Axes3D(fig)
    ax.contour(X,Y,Z)
    #ax.plot3D(X,Y,Z)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    #fig.add_axes(ax)
    p.show()
    
def interpolate_color( color1=None, color2=None, range=None, value=None):
    """Returns the interpolated RGB value between color1 and color2.
    assumptions:
    * color?= (r,g, b)
    * range = (x1, x2)
    * x1 < x2
    * value is in range
    """
    try:
        r,b,g = color1
        r2,b2,g2 = color2
        s0, s1 = range
        p = (value-s0) / (s1-s0) 
        dr = float( r2 - r )
        dg = float( g2 - g )
        db = float( b2 - b )
        c = (r+p*dr, b+p*db , g+p*dg)
    except ZeroDivisionError:
        return color1
    return c 


class IntIdGenerator( object ):
    """Class used to create uniq ``int`` ids for any object. 
    
    After asking for `id` of the object the object is remembered and next time
    the same id will be returned.
    """
    def __init__( self, objects=[] ):
        """Basic constructor.
        """
        self._current_id = 0
        self._object2id = {}
        for i in objects:
            self.id( i )
  
    def id( self, object ):
        """Returns the ``int`` id of the object.
        
        After asking for `id` of the object the object is remembered and next time
        the same id will be returned.
        
        :parameters:
            object : ``hashable``
                The object for which we want to obtain the id.
        :rtype: `int`
        :return: Id of an object.
        """
        if not self._object2id.has_key( object ):
            self._object2id[ object ] = copy.copy( self._current_id )
            self._current_id += 1
            return self._current_id-1
        else:
            return self._object2id[ object ]
        
        def id2objects( self ):
            s = {}
            for i in self._object2id:
                s[ self._object2id[ i ] ] = i
            return s
        
def segment( x1=None, x2=None, step=None ):
    """Returs an order set of points from segment [x1,x2] starting with x1 with step `step`.
    
    <Long description of the function functionality.>
    
    :parameters:
        x1 : `float`
            left boundary of segment
        x2 : `float`
            right boundary of segment
        step : `float`
            step
    :rtype: [`float`]
    :return: A list of values inside a segment.
    :raise Exception: TODO drop if x1 >x2
    """
    l = []
    i = x1
    while i<x2:
        l.append( i )
        i += step
    return l


def cast_to_0_1_segment( base_segment=None, value=None ):
    """Casts given value from given segment to [0,1].
    
    <Long description of the function functionality.>
    
    :parameters:
        base_segment : ``2tuple``
            Segment from which comes the given value
        value : `float`
            Value to be casted
    :rtype: `float`
    :return: Casted value from [0,1]
    :raise Exception: TODO
    """
    if base_segment[ 1 ] < base_segment[ 0 ]:# or (value < base_segment[ 0 ] or value >base_segment[ 1 ]):
        raise TypeError
    if base_segment[ 1 ] == base_segment[ 0 ]:
        return 0.5
    if value > base_segment[ 1 ]:
        return 1.
    if value < base_segment[ 0 ]:
        return 0.
    return ( value-base_segment[ 0 ] ) / (base_segment[ 1 ] - base_segment[ 0 ])
    
    
def pyfunction(func_str):
    """ creates a function from a text string """

    if func_str:
        func_str = str(func_str)
        # Extract the function name
        l= func_str.split('\n')
        for line in l:
            if 'def ' in line:
                break
        name=line.split('def ')[1]
        name=name.split('(')[0]

        # local dictionary
        d = {}
        #print str(func_str)
        exec(str(func_str),d)
        
        return d.get(name,None)
    else:
        return None