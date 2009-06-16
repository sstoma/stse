#!/usr/bin/env python
"""Defines configuration for quad2 tissue.

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
__date__="Tue Jun 16 12:44:32 CEST 2009"
__version__="0.1"
__docformat__= "restructuredtext en"

import math

# making sure that the configuration is new
import openalea.stsf.io.walled_tissue.dat_config
m = reload( openalea.stsf.io.walled_tissue.dat_config )
locals().update(m.__dict__)

rotation = math.pi/2.
translation = True