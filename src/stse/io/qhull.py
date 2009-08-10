#!/usr/bin/env python
"""The utils allowing to work with QHULL file format

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
__contact__="<Your contact>"
__license__="Cecill-C"
__date__="Thu Jul 16 13:33:25 CEST 2009"
__version__="0.1"
__docformat__= "restructuredtext en"

import subprocess
import os

def twoD_positions_to_QHULL_file(pos_list, file_name):
    """Saves the positions in a file recognized by QHULL.
    File imits the syntax of RBOX generated file.
    
    <Long description of the function functionality.>
    
    :parameters:
        pos_list : `[(x,y)]`
            List containing the positions to be stored in files.
        file_name : string
            Name of the file to be saved.
    """
    f = file(file_name, "w")
    f = twoD_positions_to_QHULL_fd( pos_list, f)
    f.close()

def twoD_positions_to_QHULL_fd(pos_list, f):
    """Saves the positions in a file recognized by QHULL.
    File imits the syntax of RBOX generated file.
    
    <Long description of the function functionality.>
    
    :parameters:
        pos_list : `[(x,y)]`
            List containing the positions to be stored in files.
        file_name : string
            Name of the file to be saved.
    """
    # dimension
    f.write(str(2)+" GENERATED FROM twoD_positions_to_QHULL_file V.0.1 \n")
    #nbr of points
    f.write(str(len(pos_list))+" \n")
    #points: in each line
    for i in pos_list:
        f.write(str(i[0])+" "+str(i[1])+" \n")
    return f
    
def voronoi_centers_to_edges( pos_list ):
    """Returns a QHULL formated files of
    
    <Long description of the function functionality.>
    
    :parameters:
        arg1 : `T`
            <Description of `arg1` meaning>
    :rtype: `T`
    :return: <Description of ``return_object`` meaning>
    :raise Exception: <Description of situation raising `Exception`>
    """
    input = os.tmpfile()
    output = os.tmpfile()
    input = twoD_positions_to_QHULL_fd( pos_list, input)
    input.seek(0)
    #return o
    s = subprocess.Popen(['qvoronoi', 'o'], stdin=input, stdout=output)
    s.communicate()
    output.seek(0)
    input.seek(0)
    return (input, output)
