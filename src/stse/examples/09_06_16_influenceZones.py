#!/usr/bin/env python
"""Produces influence maps of real tissue data.

<Long description of the module functionality.>

:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    Humboldt University

"""
# Module documentation variables:
__authors__="""Szymon Stoma    
"""
__contact__="<Your contact>"
__license__="Cecill-C"
__date__="Fri Jun 19 16:02:57 CEST 2009"
__version__="0.1"
__docformat__= "restructuredtext en"
__svn_revision__= "13"

from openalea.stse.io.walled_tissue.dat_representation import read_dat2walled_tissue, read_link_file
import openalea.plantgl.all as pgl
import openalea.plantgl.ext.all as pd
from lib_09_06_06_influenceZones import vis, display_config 
from openalea.stse.io.walled_tissue.dat_config_processing import read_dat_tissue_directory, Config

### first tissue
def f1( path ):
    """Loading initial tissues and preparing for display configuration.
    """
    wt = read_dat_tissue_directory( path +"config.py" )
    # this contains some additional tissue information
    c = Config( path+"config.py" )


    vis( wt, c, ["CZ_IZ"] )
    display_config()
    # please configure the viewer and issue it manually
    #vis( wt, c, c.cell_iz.keys(), clear=True, save=True )
    return wt, c

path = []
path.append("/Users/stymek/src/stse/trunk/data/09-06-10-marianne-wt2/")
path.append("/Users/stymek/src/stse/trunk/data/09-05-26-marianne-quad2/")
path.append("/Users/stymek/src/stse/trunk/data/09-06-10-marianne-quad1/")

