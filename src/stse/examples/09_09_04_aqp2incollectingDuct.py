#!/usr/bin/env python
"""Model of aqp in collecting duct.

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
__date__="<Timestamp>"
__version__="0.1"
__docformat__= "restructuredtext en"





from openalea.stse.gui.compartment_viewer import general_viewing
from openalea.stse.gui.compartment_editor import general_editing
from openalea.stse.io.walled_tissue.native_representation import \
    write_walled_tissue, read_walled_tissue
from openalea.stse.structures.algo.walled_tissue_physiology import \
    PhysiologicalModelAction
from enthought.pyface.api import GUI



class AQPPhysiologicalModelAction( PhysiologicalModelAction ):
    """Diffusion of a substance A in a WalledTissue.
    """
    pass

if __name__ == '__main__':
    window = general_viewing()
    window.edit_traits()
    window.do()
    GUI().start_event_loop()
    window.actions["file_load_walled_tissue"].load("/local/home/sstoma/src/stse/trunk/data/09-11-03-aqpCellCulture/initial/")
    da = AQPPhysiologicalModelAction(wt=window._voronoi_wt, window=window)
    da.capture_period = 1.
    