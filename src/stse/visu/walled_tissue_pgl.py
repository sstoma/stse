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

import copy
import  openalea.plantgl.ext.all as pd
import  openalea.plantgl.ext.color as color
import  openalea.plantgl.all as pgl
from ..structures.algo.walled_tissue import cell_center, wv_edge2cell_edge, calculate_cell_surface
from ..tools.misc import segment, cast_to_0_1_segment
from openalea.stse.visu.draw_cell_pgl import draw_cell



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

def f_cell_marking( properties, property_true_material=pgl.Material( (255, 255, 255) ), property_true_radius=0.1 ):
    """Returns a funtion returning an pgl.shape with center in the centroid of
    given cell if one of the properties evaluates to True.

    :parameters:
        wt : `WalledTissue`
            Tissue storing cell data
        cell : int
            cell id 
    :rtype: `openalea.plantgl.all.Shape`
    :return: Material used to color the cell
    """
    def f( wt, cell ):
        """<Short description of the function functionality.>
        
        :parameters:
            wt : `WalledTissue`
                Tissue storing cell data
            cell : int
                cell id 
        :rtype: `openalea.plantgl.all.Shape` or None
        :return: Shape centered in the centroid of the cell if one of the
        properties was satisfied.
        """
        for property in properties:
            if wt._cell2properties[ cell ].has_key( property ):
                #print cell, property, wt.cell_property( cell, property )
                if wt.cell_property( cell, property ):
                    return pd.ASphere(pos=cell_center(wt, cell), material=property_true_material, radius=property_true_radius).shape
        return None
    return f    

def f_properties2material( properties=None, property_material=pgl.Material((0,255,0)), normal_material=pgl.Material((0,0,0)) ):
    """Returns a function returning a material 'property_material' if one of the
    list items in 'properties' is evaluated as True for a given cell. 
    
    :parameters:
        properties : [str]
            list of properties
        property_material : pgl.Material
            material returned for cells for which one of property evaluates to
            True
        normal_material : pgl.Material
            material returned for cells for which each properties evaluate to
            False
    :rtype: `openalea.plantgl.all.Material`
    :return: Material used to color the cell
    """
    def f( wt=None, cell=None, **keys ):
        """Returns a material for a given cell.
        
        :parameters:
            wt : `WalledTissue`
                Tissue storing cell data
            cell : int
                cell id 
        :rtype: `openalea.plantgl.all.Material`
        :return: Material used to color the cell
        """
        for property in properties:
            if wt._cell2properties[ cell ].has_key( property ):
                if wt.cell_property( cell, property ):
                    return property_material
        return normal_material
    return f



weighted_property2material_green_range = color.GreenMap(outside_values=True)
weighted_property2material_green_range._position_list=[0.,0.5,1.]
def f_weighted_property2material( property=None, range=[0,1], default_color_range=weighted_property2material_green_range ):
    default_color_range.set_value_range(range)
    def f( wt=None, cell=None, **keys):
        if wt._cell2properties[cell].has_key(property):
            return pgl.Material( default_color_range.get_color( wt.cell_property(cell, property) ).i3tuple() )
        else: return pgl.Material( default_color_range.get_color( range[ 0 ] ).i3tuple() )
    return f


def f_green_material( wt=None, cell=None, **keys ):
    """Returns green material for each cell from tissue.
    
    :parameters:
        wt : WalledTissue
            Tissue containing cell informations.
        cell : int
            Id of cell for which material is selected.
    :rtype: pgl.Material
    :return: Color prepared for a given cell.
    :raise Exception: <Description of situation raising `Exception`>
    """
    return pgl.Material((0,255,0))    


def f_property2scalar(wt_property_method=None,
                      property = None,
                      default_value = 0.,
                      segment = None,
                      factor = 1.):
    """Returns a function which takes an object and
    returns a scalar value.
    
    Function is built using the wt_property_method
    which is used to get a scalar value of object. If wt_property_method does
    not have a requested object/value or if the returned value can not be
    converted into float, default_value is returned.
    
    :parameters:
        wt_property_method : function
            Function which needs to return value for 2 arguments, one will be an
            object, second is a property name.
        property : string
            Property identificator, used by wt_property_method.
        default_value : float
            Default value returned in case described in function synopis.
        segment : (float, float)
            If specified, the returned value is converted to 0,1 segment
            according to this range and multiplied by factor.
        factor : float
            The value is used to scale the returned value - first the value is
            converted to fit the 0,1 segment, and then it is multiplied by
            the factor.

    :rtype: function
    :return: Function returning a scalar value for an object argument.
    """
    def f( object,  **keys):
        try:
            v = wt_property_method( object, property )
            if not segment:
                return float( v )
            else:
                return factor * cast_to_0_1_segment( base_segment = segment,
                                           value = v)
        except LookupError, ValueError:
            return float( default_value )
    return f

    
    
def visualisation_pgl_2D_varried_membrane_thickness( wt,
                                    max_wall_absolute_thickness=0.15,
                                    abs_intercellular_space=0.,
                                    abs_membrane_space=0.,
                                    f_material=f_green_material,
                                    revers=True,
                                    wall_color=pgl.Color4(0,0,0,0),
                                    pump_color=pgl.Color4(255,0,0,0),
                                    stride=15,
                                    f_membrane_thickness=None,
                                    f_cell_marking=[],                                    
                                    **keys):
    """Provides 2D tissue visualisation. 
    
    It allows to control each membrane thickness separatly (which is regulated by
    the function working on a tuple (cell, wv_edge) and a color of each cell
    (which is controlled by a function working on a cell).
    
    :parameters:
        arg1 : `T`
            <Description of `arg1` meaning>
    :rtype: `T`
    :return: <Description of ``return_object`` meaning>
    :raise Exception: <Description of situation raising `Exception`>
    """    
     
    l=[]
    l2=[]
    for i in wt.cells():
        cell_corners=[wt.wv_pos(j) for j in wt.cell2wvs(i)]
        if not f_membrane_thickness:
            wall_relative_thickness = [0 for j in wt.cell2wvs_edges(i)]
        else:
            wall_relative_thickness = []
            for j in wt.cell2wvs_edges( i ):
                wall_relative_thickness.append( f_membrane_thickness( i, j ) )
        
        cell_color=f_material(wt=wt, cell=i)
        cell_color=pgl.Color4(cell_color.ambient.red,cell_color.ambient.green,cell_color.ambient.blue,0)
        if revers:
            cell_corners.reverse()
            wall_relative_thickness.reverse()
            wall_relative_thickness = wall_relative_thickness[1:]+[wall_relative_thickness[0]]
        #print i
        l.append( draw_cell (cell_corners, wall_relative_thickness, abs_intercellular_space, abs_intercellular_space+abs_membrane_space, cell_color, wall_color, pump_color, stride=stride, nb_ctrl_pts=3, sc=None))
        for f in f_cell_marking:
            k = f( wt, i)
            if k:
                l2.append( k )
        
    for i in l: pd.get_scene().add(pgl.Shape(i,pgl.Material( (0,0,0) )))
    for i in l2:
        pd.get_scene().add( i )


    