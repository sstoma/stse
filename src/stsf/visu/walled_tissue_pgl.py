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
__authors__="""Szymon Stoma    
"""
__contact__=""
__license__="Cecill-C"
__date__="<Timestamp>"
__version__="0.1"
__docformat__= "restructuredtext en"
__revision__="$Id$"


import  openalea.plantgl.ext.all as pd
import  openalea.plantgl.ext.color as color
import  openalea.plantgl.all as pgl
from ..structures.algo.walled_tissue import cell_center, wv_edge2cell_edge, calculate_cell_surface
from ..tools.misc import segment, cast_to_0_1_segment 



green_cell_material = pgl.Material( (0,255,0) )


class SphericalCell(pd.AISphere):
    """<Short description of the class functionality.>
    
    <Long description of the class functionality.>
    """
    def __init__( self, cell=None, wt=None, c_sphere_radius_factor=1, material_f=None, material_range=(0,1), **keys ):
        """Basic constructor.
        """
        pos = cell_center( wt, cell=cell )
        radius = c_sphere_radius_factor*math.sqrt( calculate_cell_surface( wt, cell=cell ) )
        material =  material_f(wt, material_range=material_range, cell=cell )
        pd.AISphere.__init__( self, pos=pos, radius=radius, material=material, **keys )

class PolygonalCell(pd.AICenterPolygon):
    
    def __init__( self,  **keys ):
        """<Short description of the function functionality.>
        
        <Long description of the function functionality.>
        
        :parameters:
            arg1 : `T`
                <Description of `arg1` meaning>
        :rtype: `T`
        :return: <Description of ``return_object`` meaning>
        :raise Exception: <Description of situation raising `Exception`>
        """
        self._common_init(**keys)
        pd.AICenterPolygon.__init__( self, points=self.l, **keys )

            
    def _common_init( self, cell=None, wt=None, abs_border_size=0., **keys ):
        self.cell_center = cell_center( wt=wt, cell=cell )
        self.l = []
        self.abs_border_size = abs_border_size
        for i in wt.cell2wvs( cell=cell ):
            v=wt.wv_pos( wv=i )-self.cell_center
            v2=pgl.Vector3(v)
            v2.normalize()
            self.l.append( self.cell_center+v-v2*abs_border_size )
        


class WalledPolygonalCell(PolygonalCell):

    def __init__( self,  cell=None, wt=None, thickness_range=(0., 1.), max_wall_absolute_thickness=1., wall_thickness_f=None, material_range=None, material_f=green_cell_material, **keys ):
        """<Short description of the function functionality.>
        
        This cell has a standard cell color and a standard cell wall color. It requires the wall
        property which would be used to determine wall fickness. Also a range of the possible
        fickness should be given as well as *absolute* max wall thickness. The function specifying
        the wall thickness should be also specified.
        
        :parameters:
            arg1 : `T`
                <Description of `arg1` meaning>
        :rtype: `T`
        :return: <Description of ``return_object`` meaning>
        :raise Exception: <Description of situation raising `Exception`>
        """
        PolygonalCell.__init__( self, cell=cell, wt=wt, pos=pgl.Vector3(0,0,-0.01), **keys )

        self.walls = {}
            
        for i in wt.cell2wvs_edges_in_real_order( cell=cell ):
            (wv1, wv2) = i
            # searching for pin concentration in the wall
            try:
                ce = wv_edge2cell_edge( wt, wt.wv_edge_id( i ) )
                if ce[ 0 ] == cell:
                    pl = cast_to_0_1_segment( base_segment=thickness_range, value=wall_thickness_f( wt, cell_edge=ce ))
                else:
                    pl = cast_to_0_1_segment( base_segment=thickness_range, value=wall_thickness_f( wt, cell_edge=(ce[ 1 ], ce[ 0 ] ) ) )
            except TypeError:
                pl=0.
            pl = pl*max_wall_absolute_thickness
            
            l = []
            v1 = wt.wv_pos( wv=wv1 )
            v2 = wt.wv_pos( wv=wv2 )
            c = self.cell_center
            for i in [(v1, v2), (v2, v1)]:
                norm_h = pl*pgl.norm(c - i[0])*pgl.norm(i[1]-i[0])/pgl.norm( pgl.cross(c-i[0], i[1]-i[0]) )
                #print v1, v2, i[0],  pgl.norm( (c - i[0]) ), norm_h
                x = (c - i[0])
                x.normalize()
                h = i[0] + x*norm_h
                l.append( h )
            if material_f == green_cell_material:
                self.walls[ wt.wv_edge_id( i ) ] = pd.AITriangle( points=[self.cell_center, l[0], l[1]], material= pgl.Material(pgl.Color3())) 
            else:
                self.walls[ wt.wv_edge_id( i ) ] = pd.AITriangle( points=[self.cell_center, l[0], l[1]], material= material_f( wt, material_range, cell ) )


def f_property2material( property=None, property_material=pgl.Material((0,255,0)), normal_material=pgl.Material((0,0,0)) ):
    def f( wt=None, cell=None, **keys):
        if wt._cell2properties[cell].has_key(property):
            if wt.cell_property( cell, property):
                return property_material
            else: return normal_material
        else: return normal_material
    return f

weighted_property2material_green_range = color.GreenMap(outside_values=True)
weighted_property2material_green_range._position_list=[0.,0.1,1.]
def f_weighted_property2material( property=None, range=[0,1], property_material=pgl.Material((0,255,0)), normal_material=pgl.Material((0,0,0)) ):
    weighted_property2material_green_range.set_value_range(range)
    def f( wt=None, cell=None, **keys):
        if wt._cell2properties[cell].has_key(property):
            return pgl.Material( weighted_property2material_green_range.get_color( wt.cell_property(cell, property) ).i3tuple() )
        else: return normal_material
    return f


def f_green_material( wt=None, cell=None ):
    """Returns green material for every cell.
    
    <Long description of the function functionality.>
    
    :parameters:
        arg1 : `T`
            <Description of `arg1` meaning>
    :rtype: `T`
    :return: <Description of ``return_object`` meaning>
    :raise Exception: <Description of situation raising `Exception`>
    """
    return pgl.Material((0,255,0))    
    
def visualisation_pgl_2D_plain( wt, max_wall_absolute_thickness=0.15,
                                    abs_intercellular_space=0., material_f=f_green_material,
                                    revers=True,  wall_color=pgl.Color4(0,0,0,0),
                                    pump_color=pgl.Color4(255,0,0,0),
                                    stride=100,
                                    **keys):
    
    from openalea.stsf.visu.draw_cell_pgl import draw_cell
    l=[]
    for i in wt.cells():
        cell_corners=[wt.wv_pos(j) for j in wt.cell2wvs(i)]
        wall_relative_thickness= [0 for i in wt.cell2wvs_edges(i)]
        cell_color=material_f(wt=wt, cell=i)
        cell_color=pgl.Color4(cell_color.ambient.red,cell_color.ambient.green,cell_color.ambient.blue,0)
        if revers:
            cell_corners.reverse()
        l.append( draw_cell (cell_corners, wall_relative_thickness, abs_intercellular_space, abs_intercellular_space, cell_color, wall_color, pump_color, stride=stride, nb_ctrl_pts=3, sc=None))
    for i in l: pd.get_scene().add(pgl.Shape(i,pgl.Material( (0,0,0) )))
    return 0



    