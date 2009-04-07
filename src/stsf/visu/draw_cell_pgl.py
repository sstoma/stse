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
__authors__="""Jerome Chopard    
"""
__contact__=""
__license__="Cecill-C"
__date__="<Timestamp>"
__version__="0.1"
__docformat__= "restructuredtext en"
__revision__="$Id$"


from openalea.plantgl.math import Vector3,Vector4
from openalea.plantgl.scenegraph import FaceSet,NurbsCurve,Polyline
from openalea.plantgl.scenegraph import Sphere,Material,Shape,Translated

def intersection (A1, A2, B1, B2) :
       """
       compute intersection point between [A1,A2]
       and [B1,B2] in 2D
       assume that the intersection exists
       """
       S1=B2-B1
       S2=A1-B1
       S3=A2-A1
       d=(S3^S1)[2]
       if abs(d)/S1.__norm__()/S3.__norm__() < 0.01:
              return (A1+B2)/2
       u=(S1^S2)[2]/d
       if u > 1.:
              return (A1+B2)/2
       elif u < 0:
              S1=A2-A1
              S2=B1-A1
              S3=B2-B1
              d=(S3^S1)[2]
              u=(S1^S2)[2]/d
              if 0 < u and u < 1:
                     return B1+S3*u
              else:
                     return (A1+B2)/2
       return A1+S3*u

def draw_cell (cell_corners, wall_relative_thickness, thickness_min, thickness_max, cell_color, wall_color, pump_color, stride=40, nb_ctrl_pts=3, sc=None) :
       """
       cell corners : corners of cell (assume that the cell is closed by linking last corner with first corner)
       assume direct orientation (anti clockwise)
       wall_thickness : absolute thickness of each wall
       cell_color : color of the internal of the cell
       wall_color : color of the outer layer
       pump_color : color of the pumps on the wall
       stride : number of points for the discretization
       nb_ctrl_points : number of control point used for each wall (plus the 2 extremities)
       """
       sph=Sphere(0.1)
       mat=Material((0,0,0))
       nb=len(wall_relative_thickness)
       assert nb==len(cell_corners)
       assert nb_ctrl_pts>0
       corners=list(cell_corners)
       #compute external curve (between cells) control points
       ctrl_pts=[]
       for i in xrange(nb) :
               ctrl_pts.append(corners[i])
               ctrl_pts.append(corners[i])
               ctrl_pts.append( (corners[i]+corners[(i+1)%nb])/2. )
               ctrl_pts.append(corners[(i+1)%nb])
       ctrl_pts=[ctrl_pts[(i+2)%len(ctrl_pts)] for i in xrange(len(ctrl_pts))]
       ctrl_pts.append(ctrl_pts[0])
       if sc is not None :
               for pt in ctrl_pts[1:-1] :
                       sc.add(Shape(Translated(pt,sph),mat))
       outer_curve=NurbsCurve([Vector4(v,1) for v in ctrl_pts])
       #wall normals
       normals=[]
       for i in xrange(nb) :
               tang=corners[(i+1)%nb]-corners[i]
               n=Vector3(-tang.y,tang.x,0)
               n.normalize()
               normals.append(n)
       #compute external curve (between wall and pumps) control points
       ctrl_pts=[]
       #wall_pump_corners=[corners[i]+(normals[i]+normals[(i-1)%nb])*thickness_min for i in xrange(nb)]
       displaced_walls=[(corners[i]+normals[i]*thickness_min,corners[(i+1)%nb]+normals[i]*thickness_min) for i in xrange(nb)]
       wall_pump_corners=[]
       for i in xrange(nb) :
               A1,A2=displaced_walls[i]
               B1,B2=displaced_walls[(i-1)%nb]
               wall_pump_corners.append(intersection(A1,A2,B1,B2))
       ctrl_pts=[]
       for i in xrange(nb) :
               ctrl_pts.append(wall_pump_corners[i])
               for j in xrange(nb_ctrl_pts) :
                       pt=(wall_pump_corners[i]*(nb_ctrl_pts-j)+wall_pump_corners[(i+1)%nb]*(1+j))/(nb_ctrl_pts+1)
                       ctrl_pts.append(pt)
       ctrl_pts=[ctrl_pts[(i+(nb_ctrl_pts+1)/2)%len(ctrl_pts)] for i in xrange(len(ctrl_pts))]
       ctrl_pts.append(ctrl_pts[0])
       if sc is not None :
               for pt in ctrl_pts[1:-1] :
                       sc.add(Shape(Translated(pt,sph),mat))
       wall_pump_curve=NurbsCurve([Vector4(v,1) for v in ctrl_pts])
       #wall curve (between pumps and cell)
       ctrl_pts=[]
       def th (i) :
               return wall_relative_thickness[i]*(thickness_max-thickness_min)+thickness_min
       displaced_walls=[(corners[i]+normals[i]*th(i),corners[(i+1)%nb]+normals[i]*th(i)) for i in xrange(nb)]
       pump_cell_corners=[]
       for i in xrange(nb) :
               A1,A2=displaced_walls[i]
               B1,B2=displaced_walls[(i-1)%nb]
               pump_cell_corners.append(intersection(A1,A2,B1,B2))
       #pump_cell_corners=[corners[i]+normals[i]*th(i)+normals[(i-1)%nb]*th((i-1)%nb) for i in xrange(nb)]
       ctrl_pts=[]
       for i in xrange(nb) :
               ctrl_pts.append(pump_cell_corners[i])
               for j in xrange(nb_ctrl_pts) :
                       pt=(pump_cell_corners[i]*(nb_ctrl_pts-j)+pump_cell_corners[(i+1)%nb]*(1+j))/(nb_ctrl_pts+1)
                       ctrl_pts.append(pt)
       ctrl_pts=[ctrl_pts[(i+(nb_ctrl_pts+1)/2)%len(ctrl_pts)] for i in xrange(len(ctrl_pts))]
       ctrl_pts.append(ctrl_pts[0])
       if sc is not None :
               for pt in ctrl_pts[1:-1] :
                       sc.add(Shape(Translated(pt,sph),mat))
       pump_cell_curve=NurbsCurve([Vector4(v,1) for v in ctrl_pts])

       #fill
       coords=[i/float(stride) for i in xrange(stride)]
       #creation of point from external curve to internal one
       outer_pts=[outer_curve.getPointAt(coord) for coord in coords]
       wall_pump_pts=[wall_pump_curve.getPointAt(coord) for coord in coords]
       pump_cell_pts=[pump_cell_curve.getPointAt(coord) for coord in coords]
       center=sum(pump_cell_pts,Vector3())/stride
       pts=outer_pts+wall_pump_pts+pump_cell_pts+[center]
       center_ind=3*stride
       faces=[(center_ind,2*stride+i,2*stride+(i+1)%stride) for i in xrange(stride)]
       faces+=[(2*stride+(i+1)%stride,2*stride+i,stride+i,stride+(i+1)%stride) for i in xrange(stride)]
       faces+=[(stride+(i+1)%stride,stride+i,i,(i+1)%stride) for i in xrange(stride)]

       mesh=FaceSet(pts,faces)
       mesh.colorList=[cell_color]*stride+[pump_color]*stride+[wall_color]*stride
       mesh.colorPerVertex=False
       return mesh