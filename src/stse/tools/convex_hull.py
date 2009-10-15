"""Rutines to compute convex hull. Usage hull( [(x0, y0),(x1, y1),..,(xn, yn)] )



:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    Humboldt Univesity

:authors:
    Szymon Stoma
"""


from __future__ import generators
from math import ceil
from copy import copy
    
def orientation(p,q,r):
    '''Return positive if p-q-r are clockwise, neg if ccw, zero if colinear.'''
    return (q[1]-p[1])*(r[0]-p[0]) - (q[0]-p[0])*(r[1]-p[1])

def hulls(Points):
    '''Graham scan to find upper and lower convex hulls of a set of 2d points.'''
    U = []
    L = []
    Points.sort()
    for p in Points:
        while len(U) > 1 and orientation(U[-2],U[-1],p) <= 0: U.pop()
        while len(L) > 1 and orientation(L[-2],L[-1],p) >= 0: L.pop()
        U.append(p)
        L.append(p)
    del L[0]
    del L[-1]
    L.reverse()
    return U+L

def rotatingCalipers(Points):
    '''Given a list of 2d points, finds all ways of sandwiching the points
between two parallel lines that touch one point each, and yields the sequence
of pairs of points touched by each pair of lines.'''
    U,L = hulls(Points)
    i = 0
    j = len(L) - 1
    while i < len(U) - 1 or j > 0:
        yield U[i],L[j]
        
        # if all the way through one side of hull, advance the other side
        if i == len(U) - 1: j -= 1
        elif j == 0: i += 1
        
        # still points left on both lists, compare slopes of next hull edges
        # being careful to avoid divide-by-zero in slope calculation
        elif (U[i+1][1]-U[i][1])*(L[j][0]-L[j-1][0]) > \
                (L[j][1]-L[j-1][1])*(U[i+1][0]-U[i][0]):
            i += 1
        else: j -= 1

def diameter(Points):
    '''Given a list of 2d points, returns the pair that's farthest apart.'''
    diam,pair = max([((p[0]-q[0])**2 + (p[1]-q[1])**2, (p,q))
                     for p,q in rotatingCalipers(Points)])
    return pair


def point_inside_polygon(point,poly):
    """Determine if a point is inside a given polygon or not
    Polygon is a list of (x,y) pairs.
    """

    n = len(poly)
    inside =False
    x = point[0]
    y = point[1]
    p1x,p1y,p1z = poly[0]
    for i in range(n+1):
        p2x,p2y,p2z = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def int_points_in_polygon( polygon=None ):
    """Function returns a list of integer coordinated
    points which are laying inside of the inputed
    polygon.
    
    <Long description of the function functionality.>
    
    :parameters:
        polygon : `[(Float,Float)]`
            Polygon defined as a list of floats.
    :rtype: `[(Int, Int)]`
    :return: List of integer coordinated
    points which are laying inside of the inputed
    polygon.
    """
    assert len(polygon) > 2
    pts_inside = []
    xmin,ymin,xmax,ymax = xy_minimal_bounding_box_of_polygon( polygon )
    pts = int_points_inside_rectangle(xmin,ymin,xmax,ymax)
    for pts_x in pts:
        if pts_x:
            pts_x_rev = copy(pts_x)
            pts_x_rev.reverse()
            nbr = len(pts_x)
            i = 0
            while i < nbr and not point_inside_polygon( pts_x[ i ], polygon ):
                i += 1
            j = 0
            while j < nbr and not point_inside_polygon( pts_x_rev[ j ], polygon ):
                j += 1
            j = nbr - j 
            # no was find
            if i <= j:
                while i < j:
                    pts_inside.append( pts_x[i] )
                    i += 1
                
    
            #for i in pts_x:
            #    # TODO optimize by check from the begining and and
            #    if point_inside_polygon( i, polygon ):
            #        pts_inside.append( i )
        
    return pts_inside


def xy_minimal_bounding_box_of_polygon( polygon=None ):
    """Function returns a xy oriented coords of
    minimum bounding box containing polygon.
    
    :parameters:
        polygon : `[(Float,Float)]`
            Polygon defined as a list of floats.
    :rtype: `(Int, Int, Int, Int)`
    :return: xmin, xmax, ymin, ymax of the
    bounding polygon.
    """
    xmin, xmax, ymin, ymax = polygon[ 0 ][ 0 ], \
        polygon[ 0 ][ 0 ], polygon[ 0 ][ 1 ], polygon[ 0 ][ 1 ]
    for i in polygon:
        if i[0] < xmin: xmin = i[0]
        if i[0] > xmax: xmax = i[0]
        if i[1] < ymin: ymin = i[1]
        if i[1] > ymax: ymax = i[1]
    return xmin, xmax, ymin, ymax
 
        
def int_points_inside_rectangle( xmin, xmax, ymin, ymax ):
    """Function returns a list of lists containing
    integer coord points which lay inside .
    
    :parameters:
        xmin : Float
            Left x coord of polygon (left corner is lower then right one)
        ymin : Float
            Left y coord of polygon (left corner is lower then right one)
        xmax : Float
            Right x coord of polygon (left corner is lower then right one)
        ymax : Float
            Right y coord of polygon (left corner is lower then right one)
    :rtype: `[[(Int,Int),..,(Int,Int)],..,[(Int,Int),..,(Int,Int)]]`
    :return: List of lists containing int coord points, list are ordered increasingly by
    x, and internal lists by y
    """
    r = []
    x = int(ceil( xmin ))
    runned_once = False
    while x < xmax:
        runned_once = True
        t = []
        y = int(ceil( ymin ))
        while y < ymax:
            t.append( (x,y) )
            y = y+1
        r.append( t )
        x = x+1
    if runned_once: return r
    else: return [[]]