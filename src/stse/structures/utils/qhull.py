#!/usr/bin/env python

__doc__="""Contains different utils responsible for qhull library usefull for stsf package.
"""
import openalea.stse.io.qhull
import os

def create_vtk_file_from_voronoi_center_widget_list( voronoi_center_widget_list, filename="voronoi.rbo", cliping_geometry="", vtk_filename="voronoi.vtk" ):
    """Brief synopsis

    A longer explanation.
            
    :param arg1: the first value
    :returns: 
    :rtype: 
    """
    openalea.stse.io.qhull.voronoi_center_widget_list_to_rbo_file(voronoi_center_widget_list, filename)
    os.popen("MakeDelaunay "+filename+" "+cliping_geometry+" > voronoi.qvo")
    os.popen("qvo2vtk.py < voronoi.qvo > "+vtk_filename)
    
