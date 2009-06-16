#!/usr/bin/env python
"""remove_cell_strategy.py

Contains different strategies used to decrease nbr of points in the simulation. Strategies *are* using
WalledTissue DS.


:version: 2006-07-15 15:21:06CEST
:author: szymon stoma
"""

class SimulationRemoveCellStrategy:
    """Interface
    """
    #TODO change on tissue system
    def __init__( self, system=None ):
        self.system = system
        
    def cells_to_remove( self ):
        print " ! SimulationRemoveCellStrategy::cells_to_remove not defined.."

    def cells_to_fix( self ):
        print " ! SimulationRemoveCellStrategy::cells_to_fix not defined.."

    def _update_df_limits(self):
        """Updates the limits for dropped and fixed.
        """
        return
    


