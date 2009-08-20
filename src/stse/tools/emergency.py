#!/usr/bin/env python
"""<Short description of the module functionality.>

<Long description of the module functionality.>

:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    INRIA

"""
# Module documentation variables:
__authors__="""<Your name>    
"""
__contact__="<Your contact>"
__license__="Cecill-C"
__date__="<Timestamp>"
__version__="0.1"
__docformat__= "restructuredtext en"

import numpy as np
def kill_close_points(points, distance):
    """Removes points overlaping with each other. Points are concidered overlaping
    when the distance of their centers is smaller than distance. 
    """
    
    ptk = {}
    
    for i in points:
        ptk[ i ] = []
    
    for i in points:
        for j in points:
            if i != j:
                d = i.position - j.position
                dn = np.sqrt(np.dot(d,d))
                if dn < distance:
                    if i not in ptk[ j ]:
                        l = ptk[ i ]
                        l.append( j )
                        ptk[ i ] = l
    ltk = []
    for i in ptk:
        for j in ptk[i]:
            ltk.append(j)
    
    ltk = dict(map(lambda a: (a,1), ltk)).keys()
    
    for i in ltk:
        points.remove(i)
                        
                