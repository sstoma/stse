#!/usr/bin/env python
"""Contains routines used to exchange data with VTK.

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

from enthought.tvtk.api import tvtk
from enthought.traits.trait_errors import TraitError
from numpy import array, infty
import math

from openalea.stse.structures.algo.walled_tissue import cell_centers
from openalea.stse.tools.convex_hull import point_inside_polygon
from copy import copy

def walled_tissue2vtkPolyData( wt=None ):
    """Converts WalledTissue to vtkPolyData.
    
    <Long description of the function functionality.>
    
    :parameters:
        wt : `walled_tissue`
            Walled tissue to be converted.
    :rtype: `vtkPolyData`
    :return: Converted tissue.
    """
    
    # setting wvs
    wvs = tvtk.Points()
    wv_id_wt2vtk = {}
    wv_id_vtk2wt = {}
    for i in wt.wvs():
        # TODO rethink mapping points to ids
        wvs.insert_point(i, tuple( wt.wv_pos( i ) ) ) 
        id = i
        wv_id_vtk2wt[ id ] = i
        wv_id_wt2vtk[ i ] = id
        
    cell_id_wt2vtk = {}
    cell_id_vtk2wt = {}
    cells = tvtk.CellArray()
    for i in wt.cells():
        cs = wt.cell2wvs( i )
        id = cells.insert_next_cell( len( cs ) )
        for j in cs:
            cells.insert_cell_point( j )
        cell_id_wt2vtk[ i ] = id
        cell_id_vtk2wt[ id ] = i
    

    tissue = tvtk.PolyData(points=wvs, polys=cells)
    return {
        "tissue": tissue,
        "cell_id_vtk2wt": cell_id_vtk2wt,
        "cell_id_wt2vtk": cell_id_wt2vtk,
        "wv_id_vtk2wt": wv_id_vtk2wt,
        "wv_id_wt2vtk": wv_id_wt2vtk,
    }


def synchronize_id_of_wt_and_voronoi( wt, point_list ):
    """Updates the properties of walled_tissue based on
    voronoi points. 
    
    The algorithm works in the following way:
    1. for each cell in wt calculates its centroid.
    2. for each centroid we assign the nearest point from points.
    3. for each pair we test if the assigned point is inside of the
    polygon corresponding to the centroid. If yes, we synchronize id.
    
    :parameters:
        wt : WalledTissue
            Tissue to synchronize
        point_list : [VoronoiCenterVisRep]
    """
    def closest_point(point, centroids):
        """ Point is VoronoiCenterVisRep
        centorids contains {cid:Vector3}
        returns cid of cell corresponding to closest point
        """
        min = infty
        id = -1
        print "start", point_list
        for i in centroids:
            dist = math.pow(centroids[ i ][0] - point.position[0],2) + math.pow(centroids[ i ][1] - point.position[1],2)           
            if dist < min:
                min = dist
                id = i
        return id
    def closest_point2(centroid, points):
        """ centroid is Vector3
        points contains [VoronoiCenterVisRep]
        returns ind of point closest to the centroid 
        """
        min = infty
        id = -1
        for i in range( len (points) ):
            dist = math.pow(points[i].position[0] - centroid[0],2) + math.pow(points[i].position[1] - centroid[1],2)           
            if dist < min:
                min = dist
                id = i
        return id
    def polygon( i ):
        cs = wt.cell2wvs( i )
        l = []
        for i in cs:
            l.append( wt.wv_pos(i) )
        return l
    # preparation
    cc = cell_centers( wt )
    point_list_tmp = list( point_list ) 
    cc2cell = {}
    for i in cc:
        cc2cell[ cc[ i ] ] = i
        
    # step 1
    centroid2nearest_point = {}
    nearest_point2centroid = {}
    for i in cc:
        cp = closest_point2(cc[ i ], point_list_tmp)
        centroid2nearest_point[ cc[ i ] ] = point_list_tmp[ cp ]
        nearest_point2centroid[ point_list_tmp[ cp ] ] = cc[ i ]
        point_list_tmp.remove( point_list_tmp[ cp ] )
    
    # step 2
    point_inside = {}
    for i in centroid2nearest_point:
        if point_inside_polygon( centroid2nearest_point[ i ].position, polygon(cc2cell[ i ] ) ):
            point_inside[ centroid2nearest_point[i] ] = True
        else:
            point_inside[ centroid2nearest_point[i] ] = False
    
    # step 3
    for i in point_inside:
        if point_inside[ i ]:
            cid = cc2cell[ nearest_point2centroid[ i ] ]
            i.cell_id = cid
        else:
            print " !: possible problem, closest point outside cell"

def copy_cell_properties_from_wt_to_voronoi( wt, voronoi, properties ):
    """Copies cell properties from WalledTissue to voronoi structure.
    
    :parameters:
        wt : `WalledTissue`
            Source of properties.
        voronoi : []
            Target of properties.
        properties : {}
            Properties to be synchronize.
    """
    for i in properties:
        try:
            for j in voronoi:
                if j.cell_id != -1:
                    j.__setattr__( i, wt.cell_property(j.cell_id, i) )
        except TraitError:
            print " !: problem while synchronising wt->voronoi:", i
            
            
def copy_cell_properties_from_voronoi_to_wt( wt, voronoi, properties, \
    init_properties=True ):
    """Copies cell properties from  voronoi to WalledTissue structure.
    
    :parameters:
        wt : `WalledTissue`
            Source of properties.
        voronoi : []
            Target of properties.
        properties : {}
            Properties to be synchronized.
    """
    for i in properties:
        if init_properties:
            wt.init_cell_property(i, properties[ i ])
        try:
            for j in voronoi:
                if j.cell_id != -1:
                    wt.cell_property(j.cell_id, i, j.__getattribute__( i ) )                
        except AttributeError:
            print " !: problem while synchronising voronoi->wt:", i