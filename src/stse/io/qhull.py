#!/usr/bin/env python

__doc__="""Contains io operations related to qhull library usefull for stsf package.
"""

def voronoi_center_widget_list_to_rbo_file(voronoi_center_widget_list, file_name):
    """Brief synopsis

    A longer explanation.
            
    :param arg1: the first value
    :returns: 
    :rtype: 
    """
    f = file(file_name, "w")
    # dimension
    f.write(str(3)+" GENERATED FROM SPHERE ACTORS V.0.1 \n")
    #nbr of points
    f.write(str(len(voronoi_center_widget_list))+" \n")
    #points: in each line
    for i in voronoi_center_widget_list:
        f.write(str(i.position[0])+" "+str(i.position[1])+" "+str(i.position[2])+" \n")
    f.close()