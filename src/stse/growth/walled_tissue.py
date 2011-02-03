#!/usr/bin/env python
"""Module providing dynamics for WT2.

They are 4 types of functions defined so far:
#tgs - tissue growth strategy
#scs - select cells strategy
#dcd - divide cell strategy
#chd - check & divide cell

:todo:
    Move rutine functions.

:bug:
    None known.
    
:organization:
    WPUT

"""
# Module documentation variables:
__authors__="""Pawel Kopocinski,
Edyta Masnik,
Szymon Stoma
"""
__contact__=""
__license__="Cecill-C"
__date__="Tue Feb  1 19:40:48 CET 2011"
__version__="0.1"
__docformat__= "restructuredtext en"


from openalea.stse.structures.algo.walled_tissue import calculate_cell_surface,\
    calculate_cell_surfaceS, calculate_cell_perimiter


# Growth strategy functions
def tgs_linear_growth (wt2d, center, steps, growth_factor):
	"""Increases the size of cell in defined as paramater number of steps and growth_factor.
	"""
	for steps_counter in range(steps):
		for i in wt2d.wvs():
			wt2d.wv_pos( i, wt2d.wv_pos( i ) - (center -  wt2d.wv_pos( i ) ) * growth_factor )


# Cell selection functions
#earlier cds_size
def scs_surface (wt2d, size):
	"""Returns list of cells which should divide acording to surface rule"""
	to_divide = []
	for c in wt2d.cells():
		if calculate_cell_surface( wt2d, c ) > size:
			to_divide.append( c ) 
	return to_divide
	
	
	
def scs_perimiter_rule(wt2d, perimiter):
	"""Returns list of cells which should divide acording to perimiter rule"""
	to_divide = []
	for c in wt2d.cells():
		if calculate_cell_perimiter( wt2d, c ) > perimiter: 
			to_divide.append( c )
	return to_divide 
	


def scs_prop_greater (wt2d, prop, value):
	"""Returns list of cells which property is higher than value"""
	to_divide = []
	for c in wt2d.cells():
		if wt2d._cell2properties[c][prop] > value:
			to_divide.append( c )
	return to_divide
	

# Check and divide functions
#earlier divide_by_surface
def chd_surface(wt2d, max_surface, divide_strategy):
	"""Dividing cells which has higher surface than max_surface"""
	cells_to_divide = scs_surface(wt2d, max_surface)
	if cells_to_divide:
		cell_to_divide_index = wt2d.cells().index(cells_to_divide[0])
		wt2d.divide_cell( wt2d.cells()[ cell_to_divide_index ], divide_strategy )
		

def chd_perimiter(wt2d, max_perimiter, divide_strategy):
	"""Dividing cells which has longer perimiter than max_perimiter"""
	cells_to_divide = scs_perimiter_rule(wt2d, max_perimiter)
	if cells_to_divide:
		cell_to_divide_index = wt2d.cells().index(cells_to_divide[0])
		wt2d.divide_cell( wt2d.cells()[ cell_to_divide_index ], divide_strategy )
		

# Divide cell strategy functions
#earlier dscs_shortest_wall
def dcs_shortest_wall( wt2d, cell ):
	"""Divide Single Cell Strategy: divides taking the shortest possible wall. TODO explain.
	"""
	shape = wt2d.cell2wvs( cell )
	test_if_division_is_possible( wt2d, shape )
	dshape = shape+shape
	ls = len(shape)
	vmin = float( "infinity" )
	for i in range( ls ): 
		s1t = wt2d.wv_pos( dshape[ i ] )
		t1t = wt2d.wv_pos( dshape[ i+1 ] )
		s2t = wt2d.wv_pos( dshape[ i+ls/2 ] )
		t2t = wt2d.wv_pos( dshape[ i+1+ls/2 ] )
		p1t = t1t + (s1t-t1t)/2.
		p2t = t2t + (s2t-t2t)/2.
		if pgl.norm( p1t-p2t ) < vmin:
		#if visual.mag( p1t-p2t ) < vmin:
			vmin = pgl.norm( p1t-p2t ) 
			#vmin = visual.mag( p1t-p2t ) 
			p1 = p1t
			p2 = p2t
			s1 = dshape[ i ]
			t1 = dshape[ i+1 ]
			s2 = dshape[ i+int(ls/2) ]
			t2 = dshape[ i+1+int(ls/2) ]
	return ( (s1, t1, p1), (s2, t2, p2) )
	
	
	
#earlier dscs_first_wall
def dcs_first_wall( wt2d, cell ):
    """Divide Single Cell Strategy: divides taking the first possible wall. TODO explain.
    """
    shape = wt2d.cell2wvs( cell )
    i = len( shape )
    test_if_division_is_possible( wt2d, shape ) 
    s1 = shape[0]
    t1 = shape[1]
    s2 = shape[ i/2 ]
    t2 = shape[ i/2+1 ]
    p1 = wt2d.wv_pos( t1 ) + ( wt2d.wv_pos( s1 ) - wt2d.wv_pos( t1 ) )/2.
    p2 = wt2d.wv_pos( t2 ) + ( wt2d.wv_pos( s2 ) - wt2d.wv_pos( t2 ) )/2.
    return ( (s1, t1, p1), (s2, t2, p2) )
	
	

#earlier dscs_shortest_wall_with_geometric_shrinking
def dcs_shortest_wall_with_geometric_shrinking( wt2d, cell ):
    """Divide Single Cell Strategy: divides taking the shortest possible wall and aditionaly shinks new wall. 
    """
    ( (s1, t1, p1), (s2, t2, p2) ) = dcs_shortest_wall( wt2d, cell )
    d = (p1 - p2) * 0.1
    return ( (s1, t1, p1-d), (s2, t2, p2+d) )
		



def test_if_division_is_possible( wt2d, shape ):
	"""Returns True if cell can be divided. Currently the cell can't be divided if it has less than 3 walls. 
	"""
	i = len( shape )
	if i < 3: 
		# TODO drop exception
		print "Skipping division of degenerated cell:", cell
		return False
	return True


#TODO these functions should be used from the place where they are defined in
# stse; you can import them using eg:
# from openalea.stse... import calculate_cell_surface

# Calculating functions
#def calculate_cell_surface( wt2d, cell=None, refresh=False ):
#	"""Calculates cell c surface. Surface is created finding the baricenter,
#	and adding the surfaces of triangles which are build up with edge (of the cell)
#	and its edges to center. With caching.
#	"""
#
#	shape = wt2d.cell2wvs( cell )
#	wv2pos = wt2d._wv2pos
#	return calculate_cell_surfaceS( shape, wv2pos )
	

#def calculate_cell_surfaceS( shape, wv2pos ):
#   s = 0
#    b = pgl.Vector3() 
#    #b = visual.vector() 
#    ls = len( shape )
#    for i in shape:
#        b += wv2pos[ i ]
#    b = b/ls
#    for i in range( ls ):
#        vi_vip = wv2pos[ shape[ (i+1)%ls ] ] - wv2pos[ shape[i] ] 
#        vi_b = b - wv2pos[ shape[i] ]
#        s += pgl.norm( pgl.cross( vi_vip, vi_b )/2 )
#        #s += visual.mag( visual.cross( vi_vip, vi_b )/2 )
#    #print "surf:", s
#    return s
    
    

#def calculate_cell_perimeter(wt2d, c):
#	"""Calculates the perimiter of cell cell_id.
#	"""
#	p = 0
#	shape = wt2d.cell2wvs( c )
#	for i in range( len( shape )-1 ):
#		p += pgl.norm( wt2d.wv_pos( shape[i] ) - wt2d.wv_pos( shape[i+1] ) )
#	return p
	
	
	
	
	
# Cell properties functions

def cell_property( wt2d, cell=None, property=None, value=None ):
        """Returns/sets property for cell
        """
        if value:
        	wt2d._cell2properties[ cell  ][ property ] = value
        elif cell == None:
        	return wt2d._cell2properties
        elif property == None:
        	return wt2d._cell2properties[ cell ]
        else:
        	return wt2d._cell2properties[ cell ][ property ]
