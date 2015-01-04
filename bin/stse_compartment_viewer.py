#!/usr/bin/env python
"""Application allowing for 2D tissue digitalization.

:bug:
    None known.
    
:organization:
    INRIA/Humboltd University Berlin

"""
# Module documentation variables:
__authors__="""Szymon Stoma    
"""
__contact__="<Your contact>"
__license__="Cecill-C"
__date__="<Timestamp>"
__version__="0.1"
__docformat__= "restructuredtext en"


# ---------------------------------------------------------------- IMPORTS

# Enthought library imports.
from pyface.api import GUI
#STSE imports
from openalea.stse.gui.compartment_viewer import general_viewing



if __name__ == '__main__':
    # Create and open an application window.
    window = general_viewing()
    window.edit_traits()
    window.do()
    GUI().start_event_loop()
