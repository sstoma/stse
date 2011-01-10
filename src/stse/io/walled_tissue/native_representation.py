#!/usr/bin/env python
"""Routines to store/load WalledTissue in native format.

Based on the concept from celltissue. 



:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    INRIA/Humboldt University

"""
# Module documentation variables:
__authors__="""Szymon Stoma    
"""
__contact__="<Your contact>"
__license__="Cecill-C"
__date__="Thu Aug  6 11:45:35 CEST 2009"
__version__="0.1"
__docformat__= "restructuredtext en"



# ----------------------------------------------------- Properties related

"""
a set of definitions of what might be a tissue property
to store tissue and values associated with tissue entities
are defined by their scale. Ususally, cell have scale 0, walls scale 1,...
"""

class IOAbstractProperty (dict) :
	"""
	abstract class for all shared properties
	"""
	def __init__ (self,*args,**keywds) :
		dict.__init__(self,*args,**keywds)
		self.description=""

class IOTissueProperty (dict) :
	"""
	Class to store a tissue property
	association of a wisp id at a given scale and a value
	Note: wisp id  *must* be ``int``.
	"""
	def __init__ (self,scale,*args,**keywds) :
		dict.__init__(self,*args,**keywds)
		self.scale=scale
		self.description=""

class IOTissue (object) :
	"""
	representation of a tissue as a list of properties :
		- scale i : IOTissueProperty({wisp at scale i-1:list of wisps at scale i})
	"""
	def __init__ (self) :
		self.field={}
		self.scale_relations=[]
		self.geometry=IOTissueProperty(0)
		self.geometry.description="describe geometry of wisps at a given scale of a tissue"



# ----------------------------------------------------- AbstractTissue related

"""
interface for reading and saving tissue
use the concepts of IOProperty defined in io_property
"""

class TissueReader( object ):
	"""<Short description of the class functionality.>
	
	<Long description of the class functionality.>
	"""
	def read (self, name=None) :
		"""
		read and return a property named name
		if name is None, return the tissue
		"""
		raise NotImplementedError


class TissueWriter( object ):
	"""<Short description of the class functionality.>
	
	<Long description of the class functionality.>
	"""
	
	def write (self, obj, objname=None) :
		"""
		write an object into the tissuefile
		with the given objname
		"""
		raise NotImplementedError
	
	def close (self) :
		"""
		close the flux and do not allow
		further accesses
		"""
		raise NotImplementedError

class TissueFile (TissueWriter, TissueReader) :
	"""
	the base class for reading and writing tissue,
	tissue properties or anything
	"""
	pass

# ----------------------------------------------------- AbstactTissue related

"""
provide some basic functions to pickle and unpickle properties
that represent a tissue and attached data
"""
import pickle
import os
from os import path

def open_tissue (tissuename,mode='r') :
	return TissuePickle(tissuename,mode)

class TissuePickleReader( TissueReader ):
	"""<Short description of the class functionality.>
	
	<Long description of the class functionality.>
	"""

	def __init__ (self, tissuename, mode="r") :
		"""
		try to create a tissuefile
		for reading 'r' or writing 'w'
		"""
		if mode=='r' :
			if not path.exists(tissuename) :
				raise IOError("not existing path %s" % tissuename)
			if not path.isdir(tissuename) :
				raise IOError("not a tissue directory %s" % tissuename)
		self._dirname=tissuename
		self._mode=mode


	def read_tissue (self, scale=None) :
		f=open(path.join(self._dirname,"_tissue.tis"),'rbU')
		tfields,max_scale=pickle.load(f)
		f.close()
		tissue=IOTissue()
		tissue.field=tfields
		if scale is None :
			scale=max_scale
		for i in xrange(scale) :
			f=open(path.join(self._dirname,"_wisp%.2d.tis" % i),'rbU')
			tissue.scale_relations.append(pickle.load(f))
			f.close()
		f=open(path.join(self._dirname,"_geometry.tis"),'rbU')
		tissue.geometry=pickle.load(f)
		f.close()
		return tissue
	
	def read_property (self, property_name) :
		f=open(path.join(self._dirname,"%s.tip" % property_name),'rbU')
		#print path.join(self._dirname,"%s.tip" % property_name)
		prop=pickle.load(f)
		f.close()
		return prop

	def read_tissue_properties( self ):
		"""Reads tissue properties.
		
		We load the tissue properties from file with predefined name:
		``tissue_properties.tip``. The properties are stored in the dict.
		The key of the dict describes the name of the property, the value
		describes the content of the property. Content must be pickable. 
		
		:rtype: ``dict(string->pickable)``
		:return: Tissue properties.
		"""
		f=open(path.join(self._dirname,"tissue_properties.tip"),'rbU')
		prop=pickle.load(f)
		f.close()
		return prop
		
	def read_description (self, description_name) :
		f=open(path.join(self._dirname,"%s.txt" % description_name),'r')
		description=f.read()
		f.close()
		return description
	
	def read_external_file (self, filename) :
		return path.join(self._dirname,filename)
	
	def read (self, name=None) :
		if self._mode!='r' :
			raise IOError("file not open in the right mode %s" % self._mode)
		if name is None :
			return self.read_tissue()
		else :
			if path.exists(path.join(self._dirname,name)) :
				return self.read_external_file(name)
			elif path.exists(path.join(self._dirname,"%s.tip" % name)) :
				return self.read_property(name)
			elif path.exists(path.join(self._dirname,"%s.txt" % name)) :
				return self.read_description(self,name)
			else :
				raise IOError("unable to read %s" % name)


class TissuePickleWriter( TissueWriter ):
	"""<Short description of the class functionality.>
	
	<Long description of the class functionality.>
	"""

	def __init__ (self, tissuename, mode="r") :
		"""
		try to create a tissuefile
		writing 'w'
		"""
		if mode=='w' :
			if path.exists(tissuename) and path.isdir(tissuename) :
				#directory already exists, do nothing
				pass
			else :
				os.mkdir(tissuename)
		self._dirname=tissuename
		self._mode=mode
	
	def write (self, tissue) :
		f=open(path.join(self._dirname,"_tissue.tis"),'wb')
		t=(tissue.field,len(tissue.scale_relations))
		pickle.dump(t,f)
		f.close()
		for ind,scale_rel in enumerate(tissue.scale_relations) :
			f=open(path.join(self._dirname,"_wisp%.2d.tis" % ind),'wb')
			pickle.dump(scale_rel,f)
			f.close()
		f=open(path.join(self._dirname,"_geometry.tis"),'wb')
		pickle.dump(tissue.geometry,f)
		f.close()
	
	def write_property (self, prop, property_name) :
		f=open(path.join(self._dirname,"%s.tip" % property_name),'wb')
		pickle.dump(prop,f)
		f.close()
	
	def write_description (self, description, description_name) :
		f=open(path.join(self._dirname,"%s.txt" % description_name),'w')
		f.write(description)
		f.close()
	
	def write_external_file (self, filename, name) :
		fext=open(filename,'rb')
		f=open(path.join(self._dirname,name),'wb')
		f.write(fext.read())
		f.close()
		fext.close()
	
	def write_tissue_properties( self, tissue_prop={} ):
		"""Writes tissue properties.
		
		The properties are stored in the dict. The key of the dict describes the name
		of the property, the value describes the content of the property. Content must
		be pickable. We store the tissue properties in file with predefined name:
		``tissue_properties.tip``.
		
		:parameters:
		    tissue_prop : ``dict(string->pickable)``
			Tissue properties.
		"""
		f=open(path.join(self._dirname,"tissue_properties.tip" ),'wb')
		pickle.dump(tissue_prop,f)
		f.close()
		
	def close (self) :
		"""
		do nothing
		"""
		pass

class TissuePickle (TissuePickleReader, TissuePickleWriter ) :
	"""
	implement TissueFile using pickling of objects into a directory
	"""
	def __init__ (self, tissuename, mode="r") :
		"""
		try to create a tissuefile
		for reading 'r' or writing 'w'
		"""
		if mode=="r":
			TissuePickleReader.__init__( self, tissuename=tissuename, mode=mode)
		elif mode=="w":
			TissuePickleWriter.__init__( self, tissuename=tissuename, mode=mode)
		else:
			raise NotImplementedError

    
# ----------------------------------------------------- WalledTissue related

from openalea.stse.structures.abstract_geometry import Point
from openalea.stse.structures.walled_tissue import WalledTissue
from openalea.stse.structures.algo.walled_tissue import create, investigate_cell
from openalea.stse.structures.algo.walled_tissue_topology import initial_find_the_inside_of_tissue
from openalea.stse.tools.misc import IntIdGenerator, get_ordered_vertices_from_unordered_shape
from openalea.stse.structures.walled_tissue_const import WalledTissueConst

import openalea.plantgl.all as pgl

def write_walled_tissue( tissue=None, name=None, desc="default description" ):
        wtp = WalledTissuePickleWriter( name, mode="w",
                               tissue=WalledTissue2IOTissue(tissue, id=IntIdGenerator( tissue.wv_edges() )),
                               tissue_properties=WalledTissue2IOTissueProperties( tissue  ),
                               cell_properties=WalledTissue2IOCellPropertyList( tissue  ),
                               wv_properties=WalledTissue2IOEdgePropertyList( tissue ),
                               wv_edge_properties=WalledTissue2IOWallPropertyList( tissue, id=IntIdGenerator( tissue.wv_edges() ) ),
                               const = WalledTissue2ConstProperties( tissue ),
                               description=desc )
        wtp.write_all()
        return wtp

def read_walled_tissue( file_name=None, const=None ):
        wtpr = WalledTissuePickleReader( file_name, mode="r")
        
        ## preparing IOTissue
        
        # reading tissue
        wtpr.read_tissue()
        
        # reading const if availibed and unspecified
        if const==None:
                try:
                        wtpr.read_property( "_const" )
                except TypeError:
                        print " #: Using default WalledTissueConst [read_walled_tissue]"
                        wtpr.const=WalledTissueConst()
        
        
        # reading all wips properties
        for i in wtpr.const.cell_properties.keys()+wtpr.const.wv_edge_properties.keys() \
            +wtpr.const.wv_properties.keys()+wtpr.const.cell_edge_properties.keys():
                #print "reading: ", i
                wtpr.read_property( i )
        # reading tissue properties
        wtpr.read_property("tissue_properties")
        
        
        ## preparing WalledTissue based on IOTissue
        
        wt=IOTissue2WalledTissue( wtpr.tissue, wtpr.wv_properties[ "_positions" ], const=wtpr.const )
        
        for j in wt.const.cell_properties.keys():
            for i in wt.cells():
                        wt.cell_property( cell=i, property=j, value=wtpr.cell_properties[ j ][ i ] )

        
        for j in wt.const.cell_edge_properties.keys():
                for i in wt.cell_edges():
                        wt.cell_edge_property( cell_edge=i, property=j, value=wtpr.cell_edge_properties[ j ][ i ] )

        for j in wt.const.wv_properties.keys():
                for i in wt.wvs():
                        wt.wv_property( wv=i, property=j, value=wtpr.wv_properties[ j ][ i ] )

        for j in wt.const.wv_edge_properties.keys():
                for i in wtpr.tissue.scale_relations[1]:
                    wt.wv_edge_property( wv_edge=tuple(wtpr.tissue.scale_relations[1][i]), property=j, value=wtpr.wv_edge_properties[ j ][ i ] )
        
        #print wt.const.tissue_properties, wtpr.tissue_properties
        for i in wt.const.tissue_properties.keys():
                wt.tissue_property( i, wtpr.tissue_properties[ i ] )
	#print " # wt.const.cell_properties:", wt.const.cell_properties
	#print " # wt._cell2properties[0]:", wt._cell2properties[0]
	#print " # wt._tissue_properties:", wt._tissue_properties
	#print " # wt.const.tissue_properties:", wt.const.tissue_properties
	return wt

class WalledTissuePickleWriter ( TissuePickleWriter ):
	def __init__ (self, tissuename, mode="w",
                    tissue=IOTissue(),
                    const=IOTissueProperty(-2),
                    tissue_properties=IOTissueProperty(-1),
		    cell_properties=IOTissueProperty(0),
                    wv_edge_properties=IOTissueProperty(1),
                    wv_properties=IOTissueProperty(2),
                    cell_edge_properties=IOTissueProperty(3),
		    description='',
                ):
		"""
		try to create a tissuefile
		for writing 'w'
		"""
		TissuePickleWriter.__init__( self, tissuename, mode )
		self.tissue = tissue
		self.tissue_properties = tissue_properties
		self.cell_properties = cell_properties
                self.cell_edge_properties = cell_edge_properties
		self.wv_properties = wv_properties
		self.wv_edge_properties = wv_edge_properties
		self.description = description
                self.const = const
			
	def write_tissue(self ) :
		TissuePickleWriter.write_tissue( self, tissue=self.tissue )
		TissuePickleWriter.write_property( self, self.wv_properties[ "_positions" ], "_positions" )
		TissuePickleWriter.write_description( self, self.description, "_desc" )
		
                
	def write_all( self ):
		TissuePickleWriter.write( self, tissue=self.tissue )
		if self.description != None:
			self.write_description( self.description, "_desc" )
		for i in self.cell_properties:
			self.write_property( self.cell_properties[ i ] , i )
		for i in self.wv_properties:
			self.write_property( self.wv_properties[ i ], i )
		for i in self.wv_edge_properties:
			self.write_property( self.wv_edge_properties[ i ], i )
                try:
                        self.write_property( self.tissue_properties, "tissue_properties")
                except TypeError:
                        print " ! Tissue properties not written: "
                self.write_property( self.const , "_const" )
                
                
class WalledTissuePickleReader ( TissuePickleReader ):
	def __init__ (self, tissuename, mode="w", tissue=IOTissue(), tissue_properties={},
		      cell_properties={}, wv_properties={},
		      wv_edge_properties={}, description=None,  ) :
		"""
		try to create a tissuefile
		for writing 'w'
		"""
		TissuePickleReader.__init__( self, tissuename, mode )
		self.tissue = tissue
		self.tissue_properties = tissue_properties
		self.cell_properties = cell_properties
		self.wv_properties = wv_properties
		self.wv_edge_properties = wv_edge_properties
		self.description = description
                self.const = None
		
			
	def read_property (self, property_name) :
		p = TissuePickleReader.read_property( self, property_name )
		if p.scale==-1:
                        self.tissue_properties = p
                elif p.scale==1:
			self.wv_edge_properties[ property_name ] = p
		elif p.scale==2:
			self.wv_properties[ property_name ] = p
		elif p.scale==0:
			self.cell_properties[ property_name ] = p
                elif p.scale==-2:
                        self.const =  p["const"] 
		else:
			raise IOError("Read unknown property..")
	
	def read_description (self, description_name="_desc") :
		try:
                        self.description = TissuePickleReader.read_description( self, description_name )
                except Exception(): self.description="" 
			
	def read (self, name=None) :
		if self._mode!='r' :
			raise IOError("file not open in the right mode %s" % self._mode)
		if name is None :
			self.tissue = self.read_tissue()
		else :
			if path.exists(path.join(self._dirname,name)) :
				return self.read_external_file(name)
			elif path.exists(path.join(self._dirname,"%s.tip" % name)) :
				self.read_property( property_name=name)
			elif path.exists(path.join(self._dirname,"%s.txt" % name)) :
				self.description = self.read_description(self,name)
			else :
				raise IOError("unable to read %s" % name)
	
	def read_tissue( self ):
                self.read_description()
		self.tissue=TissuePickleReader.read_tissue( self )
		self.wv_properties[ "_positions" ] = TissuePickleReader.read_property( self, "_positions" )
                self.const = TissuePickleReader.read_property( self, "_const" )
     

                
                
def IOTissue2WalledTissue( it = None, pos={}, const=None):
	"""<Short description of the function functionality.>
	
	<Long description of the function functionality.>
	
	:parameters:
	    it : `IOTissue`
		Tissue to be converted.
	:rtype: `WalledTissue`
	:return: Converted tissue
	:raise Exception: <Description of situation raising `Exception`>
	"""
        if const==None:
                const = TissueConst()
        cell_walls=None
        wall_edges=None
        for i in it.scale_relations:
                if i.scale == 0:
                        cell_walls = i
                elif i.scale == 1:
                        wall_edges = i
	if len( it.scale_relations ) != 3 or not (cell_walls and wall_edges):
                raise Exception("Tissue incompatible")
        #print it.scale_relations
        #transformation of pid into eid
        pid_to_eid={}
        for eid,geom in it.geometry.iteritems() :
                pid,=geom
                pid_to_eid[pid]=eid
        for pid,vec in pos.items() :
                pos[pid_to_eid[pid]]=vec
        #vcreation of shapes
        cell2wv_list = {} #cell to ordered list of wv
	for c in cell_walls.keys():
		cellshape=[]
		for w in cell_walls[ c ]:
			cellshape.append( wall_edges[ w ] )
		cell2wv_list[ c ] = get_ordered_vertices_from_unordered_shape( cellshape )
	
	wt = WalledTissue(const=const) #TODO const
        for i in pos:
                if len( pos[ i ] ) == 1:
                        pos[ i ] = pgl.Vector3(pos[ i ][ 0 ], 0., 0.)
                if len( pos[ i ] ) == 2:
                        pos[ i ] = pgl.Vector3(pos[ i ][ 0 ], pos[ i ][ 1 ], 0.)
                if len( pos[ i ] ) == 3:
                        pos[ i ] = pgl.Vector3(pos[ i ][ 0 ], pos[ i ][ 1 ], pos[ i ][ 2 ])
                else:
                        raise Exception("Problem in position retrival..")
	create( wt, wv2pos=pos, cell2wv_list=cell2wv_list)
	#initial_find_the_inside_of_tissue( wt )
        return wt

def WalledTissue2IOTissue( wt = None, id=IntIdGenerator() ):
	"""<Short description of the function functionality.>
	
	<Long description of the function functionality.>
	
	:parameters:
	    wt : `WalledTissue`
		Tissue to be converted.
	    id : `IntIdGenerator`
		Generator used to transform wv_edge_id to id.
	:rtype: `IOTissue`
	:return: Conversion result (cropped).
	"""
	r = IOTissue()

        cell_walls = IOTissueProperty(0)
        wall_edges = IOTissueProperty(1)
        edge_empty = IOTissueProperty(2)
        geometry = IOTissueProperty(2)
	for i in wt.cells():
		cell_walls[ i ] = map( lambda x : id.id( wt.wv_edge_id(x)) , wt.cell2wvs_edges( i ) )
        #print "cw", cell_walls, id._object2id
        #raw_input()
	for i in wt.wv_edges():
		wall_edges[ id.id( i ) ] = [ i[ 0 ], i[ 1 ] ]
        #print wall_edges
	for i in wt.wvs():
		edge_empty[ i ] = []
	for i in wt.wvs():
		geometry[ i ] = Point( i )
        r.scale_relations.append(cell_walls)
        r.scale_relations.append(wall_edges)
        r.scale_relations.append(edge_empty)
        r.geometry=geometry
        return r


def WalledTissue2IOWallPropertyList( wt=None, id=None ):
	"""<Short description of the function functionality.>
	
	<Long description of the function functionality.>
	
	:parameters:
	    arg1 : `T`
		<Description of `arg1` meaning>
	:rtype: `T`
	:return: <Description of ``return_object`` meaning>
	:raise Exception: <Description of situation raising `Exception`>
	"""
	l ={}
	for i in wt.const.wv_edge_properties.keys(): 
		r = IOTissueProperty(1)
		r.description = i
		for j in wt.wv_edges():
			r[ id.id( j ) ] = wt.wv_edge_property( wv_edge=j, property=i )
		l[ i ] = r
	return l 


def WalledTissue2IOCellPropertyList( wt=None ):
	"""<Short description of the function functionality.>
	
	Note: we assume that 
	
	:parameters:
	    arg1 : `T`
		<Description of `arg1` meaning>
	:rtype: `T`
	:return: <Description of ``return_object`` meaning>
	:raise Exception: <Description of situation raising `Exception`>
	"""
	l = {}
	for i in wt.const.cell_properties.keys(): 
		r = IOTissueProperty(0)
		r.description = i
		for j in wt.cells():
			r[ j  ] = wt.cell_property( cell=j, property=i )
		l[ i ] = r 
	return l


def WalledTissue2IOEdgePropertyList( wt=None ):
	"""<Short description of the function functionality.>
	
	<Long description of the function functionality.>
	
	:parameters:
	    arg1 : `T`
		<Description of `arg1` meaning>
	:rtype: `T`
	:return: <Description of ``return_object`` meaning>
	:raise Exception: <Description of situation raising `Exception`>
	"""
	l = {}
	for i in wt.const.wv_properties.keys(): 
		r = IOTissueProperty(2)
		r.description = i
		for j in wt.wvs():
			r[ j  ] = wt.wv_property( wv=j, property=i )
		l[ i ] = r
	r = IOTissueProperty( 2 )
	r.description = "_positions"
	for j in wt.wvs():
		p = wt.wv_pos( j )
		r[ j  ] = (p.x, p.y, p.z)
	l[ r.description ] = r 
	return l

def WalledTissue2IOTissueProperties( wt=None ):
	"""<Short description of the function functionality.>
	
	<Long description of the function functionality.>
	
	:parameters:
	    arg1 : `T`
		<Description of `arg1` meaning>
	:rtype: `T`
	:return: <Description of ``return_object`` meaning>
	:raise Exception: <Description of situation raising `Exception`>
	"""
	r = IOTissueProperty(-1)
        r.description =  "Tissue properties"
        for i in wt.const.tissue_properties.keys(): 
		if wt.has_tissue_property( property=i ):
			r[ i  ] = wt.tissue_property( property=i )
	return r

def WalledTissue2ConstProperties( wt=None ):
	"""<Short description of the function functionality.>
	
	<Long description of the function functionality.>
	
	:parameters:
	    arg1 : `T`
		<Description of `arg1` meaning>
	:rtype: `T`
	:return: <Description of ``return_object`` meaning>
	:raise Exception: <Description of situation raising `Exception`>
	"""
	r = IOTissueProperty(-2)
        r.description =  "Tissue const object"
        r[ "const"  ] = wt.const
	return r
