#!/usr/bin/env python

"""Functions containing phyllotaxis utils.


:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    INRIA/HU

"""

# Module documentation variables:
__authors__="""Szymon Stoma    
"""
__contact__=""
__license__="Cecill-C"
__date__="pia mar 30 14:50:15 CEST 2007"
__version__="0.1"
__docformat__= "restructuredtext en"
__revision__="$Id$"

##BEGIN DOC REMOVE
import pylab as pl
##END DOC REMOVE



def store_primordium_position( wt, primordium=None):
    """Saves position of primordium in the tissue properties.
    
    Note: currently the gravity centre is used as one arm of the angle. This
    may lead to errors.
    """
    #for i in wt.cells():
    #    if wt.cell_property( cell=i, property="IC"):
    #        IC = i
    p = wt.tissue_property( property = "primordiums" )
    pp = wt.cell_center( cell=primordium )
    cp = wt.find_top_cell_by_2d_distance_to_center()[ "gravity_center" ]
    #wt.cell_center( cell=IC )
    if wt.cell_property(cell=primordium, property="PrC") > 1:
        i = wt.cell_property(cell=primordium, property="PrC")
        yi = wt.tissue_center() - pp
        zi = wt.tissue_center() - p[ i-1 ][ "ini_pos" ]
        dd = standarize_angle( get_angle_between_primordias( yi, zi) )
        print " #: current div. angle: ", dd
    p[ wt.cell_property(cell=primordium, property="PrC") ] = {"time": wt.time, "center_pos": cp, "ini_pos": pp}
    wt.tissue_property( property = "primordiums", value=p )

def store_primordium_position_wv( wt, primordium_wv=None, number=-1):
    """Saves position of primordium in the tissue properties.
    
    Note: currently the gravity centre is used as one arm of the angle. This
    may lead to errors.
    """
    p = wt.tissue_property( property = "primordiums" )
    pp = wt.wv_pos( wv=primordium_wv )
    cp = wt.find_top_cell_by_2d_distance_to_center()[ "gravity_center" ]
    #wt.cell_center( cell=IC )
    if number >1:
        i = number
        yi = wt.tissue_center() - pp
        zi = wt.tissue_center() - p[ i-1 ][ "ini_pos" ]
        dd = standarize_angle( get_angle_between_primordias( yi, zi) )
        print " #: current div. angle: ", dd
    p[ number ] = {"time": wt.time, "center_pos": cp, "ini_pos": pp}
    wt.tissue_property( property = "primordiums", value=p )

    
def visualise_primordium_information( wt, center=None ):
    """Makes a plot of divergance angles.
    
    Remember to give the right center.
    
    TODO: change to DDS code
    """
    print " #: using predefined center"
    p = wt.tissue_property( property="primordiums" )
    pln = len( p )
    x = range( 1, pln )
    y = []
    for i in range( 2, pln+1 ):
        if not center:
            yi = p[ i ][ "center_pos"] - p[ i ][ "ini_pos" ]
            zi = p[ i-1 ][ "center_pos"] - p[ i-1 ][ "ini_pos" ]
        else:
            yi = center - p[ i ][ "ini_pos" ]
            zi = center - p[ i-1 ][ "ini_pos" ]
            
        yi.z = 0
        zi.z = 0
        dd = standarize_angle( get_angle_between_primordias( yi, zi) )
        y.append( dd )
    pl.plot( x, y, "." )
    pl.show()
