#!/usr/bin/env python
"""Abstract geometry.

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
Jerome Chopard
"""
__contact__="<Your contact>"
__license__="Cecill-C"
__date__="Thu Aug  6 12:07:07 CEST 2009"
__version__="0.1"
__docformat__= "restructuredtext en"

class AbstractShape (object) :
	"""
	a geometrical object that work on abstract points
	and not on positions
	"""
	def centroid (self, positions) :
		"""
		return the centroid of the object according
		to positions of points stored in positions
		:param positions: dict of {pid:vector}
		"""
		raise NotImplementedError
	
	def barycenter (self, positions) :
		"""
		return the barycenter of the object according
		to positions of points stored in positions
		:param positions: dict of {pid:vector}
		"""
		raise NotImplementedError
	
	def volume (self, positions) :
		"""
		return the volume (or surface in 2D or length in 1D or 0 in 0D)
		of the object according
		to positions of points stored in positions
		:param positions: dict of {pid:vector}
		"""
		raise NotImplementedError
	
	def size (self, positions) :
		"""
		return the size (1D length)
		of the object according
		to positions of points stored in positions
		:param positions: dict of {pid:vector}
		rtype : float
		"""
		raise NotImplementedError

class AbstractPolyhedra (AbstractShape) :
	"""
	a specification of previous concept for shapes
	that are defined by corners
	"""
	dim=0
	"""
	topological dimension of the polyhedra
	"""
	def corners (self) :
		"""
		iterator on all corners of the shape
		"""
		raise NotImplementedError
	
	def __iter__ (self) :
		"""
		alias for 'corners'
		"""
		raise NotImplementedError
	
	def nb_corners (self) :
		"""
		number of corners that define the polyhedral shape
		"""
		raise NotImplementedError
            
            
class Point (AbstractPolyhedra) :
	"""
	a point as 0D object in space
	hopefully not use
	"""
	dim=0
	
	def __init__ (self, pid) :
		self._pid=pid
	
	def centroid (self, positions) :
		return positions[self._pid]
	centroid.__doc__=AbstractPolyhedra.centroid.__doc__
	
	def barycenter (self, positions) :
		return positions[self._pid]
	barycenter.__doc__=AbstractPolyhedra.barycenter.__doc__
	
	def volume (self, positions) :
		return 0.
	volume.__doc__=AbstractPolyhedra.volume.__doc__
	
	def size (self, positions) :
		return 0.
	size.__doc__=AbstractPolyhedra.size.__doc__
	
	def corners (self) :
		yield self._pid
	corners.__doc__=AbstractPolyhedra.corners.__doc__
	
	def __iter__ (self) :
		yield self._pid
	__iter__.__doc__=AbstractPolyhedra.__iter__.__doc__
	
	def nb_corners (self) :
		return 1
	nb_corners.__doc__=AbstractPolyhedra.nb_corners.__doc__

