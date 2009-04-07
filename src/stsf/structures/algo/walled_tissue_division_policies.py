#!/usr/bin/env python
"""The module containing different pre/post division policies.

here the different post/pre division_policies are kept.

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

from openalea.mersim.tissue.algo.walled_tissue import cell_center, calculate_cell_surface, pin_level

# Old code, not suitable right now. kept in case..
#def  pre_1():
#    """TODO do it!
#    """
#    # saving mt
#    shape = self.cell2wvs( cell = cell )
#    s1 = shape[0]
#    t1 = shape[1]
#    s1pos = self.wv_pos( wv=s1 )
#    t1pos = self.wv_pos( wv=t1 )
#    middle_of_wall = t1pos + ( s1pos - t1pos )/2.
#    center_of_cell = self.cell_center( cell = cell )
#    #axis = (middle_of_wall - center_of_cell).rotate( angle = self.cell_property( cell=cell, property="mtb_orientation_angle"),
#    #                                                axis=visual.cross(s1pos-center_of_cell, t1pos-center_of_cell) ) 
#    #TODO translate to pgl
#    axis = (middle_of_wall - center_of_cell).rotate( angle = self.cell_property( cell=cell, property="mtb_orientation_angle"),
#                                                    axis=visual.cross(s1pos-center_of_cell, t1pos-center_of_cell) ) 
#    #
#    
#    #saving surface
#    surf = self.calculate_cell_surface( cell = cell )
#    cell_center = self.cell_center( cell = cell )
#
#    #saving pin:
#    pin_c2n={}
#    pin_n2c={}
#    for i in self.cell_neighbors( cell = cell ):
#        pin_c2n[ i ] = self.pin( (cell, i) )
#        pin_n2c[ i ] = self.pin( (i, cell) )
#    
#    #saving properties
#    saved_prop = {}
#    for cp in self._cell2properties[ cell ].keys():
#            saved_prop[ cp ] = self.cell_property( cell, cp)
#
#
#def post_1():
#    """TODO do it!
#    """
#    ( ( ( v1d, p1 ), (v2d, p2) ), ( ( v1d, s1 ), ( v1d, t1 ),( v2d, s2 ),( v2d, t2 ),( v1d, v2d ) ), dict )  =  r
#    for i in ( dict[ "added_cell1"], dict[ "added_cell2" ] ):
#        for cp in saved_prop.keys():
#                self.cell_property( i, cp, saved_prop[ cp ] )
#    if saved_prop["PrC"]>0:
#        # criterium of distance to the right path
#        ##added_cell_1_center = self.cell_center( dict[ "added_cell1"] )
#        ##added_cell_2_center = self.cell_center( dict[ "added_cell2"] )
#        ##cell_init_pos = self.tissue_property( "primordiums" )[ saved_prop["PrC"] ][ "ini_pos" ]
#        ##center = self.tissue_center()
#        ##correct_path_direction = cell_init_pos - center
#        ##a1 = visual.diff_angle( added_cell_1_center - center,correct_path_direction)  
#        ##a2 = visual.diff_angle( added_cell_2_center - center,correct_path_direction)
#        ##if a1 < a2:
#        #if self.cell_center( cell=dict[ "added_cell1" ] ).z < self.cell_center( cell=dict[ "added_cell2" ] ).z :
#        cs = self.cell2wvs( cell=dict[ "added_cell1" ] )
#        prm=False
#        for i in cs:
#            if self.wv_property(wv=i, property="PrC") == saved_prop["PrC"]:
#                prm=True
#        if prm:
#            self.cell_property( cell=dict["added_cell1"], property="PrC", value= saved_prop["PrC"])
#            self.cell_property( cell=dict["added_cell2"], property="PrC", value=0 )
#        else:
#            self.cell_property( cell=dict["added_cell2"], property="PrC", value= saved_prop["PrC"] )
#            self.cell_property( cell=dict["added_cell1"], property="PrC", value=0 )
#
#    # pumps
#    added_cells = [dict["added_cell1"], dict["added_cell2"]]
#    #print pin_c2n, added_cells
#    for c in added_cells:
#        for i in self.cell_neighbors( c ):
#            if i not in added_cells:
#                #print c, i
#                if pin_c2n[ i ] >pin_c2n[ i ]:
#                    self.pin( (c,i), pin_c2n[ i ] )
#                    self.pin( (i,c), pin_n2c[ i ] )
#                else:
#                    self.pin( (c,i), pin_c2n[ i ] )
#                    self.pin( (i,c), pin_n2c[ i ] )
#            else:
#                pass
#                # leave default value
#                
#    ## automatic IC identity
#    if saved_prop["IC"]:
#        #self.cell_property( cell=dict["added_cell2"], property="IC", value="False" )
#
#        if self.cell_center( cell=dict[ "added_cell1" ] ).z < self.cell_center( cell=dict[ "added_cell2" ] ).z :
#            self.cell_property( cell=dict["added_cell1"], property="IC", value=False )
#            self.cell_property( cell=dict["added_cell2"], property="IC", value=True )
#        else:
#            self.cell_property( cell=dict["added_cell2"], property="IC", value=False )
#            self.cell_property( cell=dict["added_cell1"], property="IC", value=True )
#
#    
#    #for aux concentration:
#    #self.cell_property( cell=dict["added_cell1"], property="auxin_level", value = saved_prop["auxin_level"]*self.calculate_cell_surface(cell=dict["added_cell1"], refresh=True)/surf ) 
#    #self.cell_property( cell=dict["added_cell2"], property="auxin_level", value = saved_prop["auxin_level"]*self.calculate_cell_surface(cell=dict["added_cell2"], refresh=True)/surf )
#    
#    # setting new orientation to new cells:
#    #for i in ( dict[ "added_cell1"], dict[ "added_cell2" ] ):
#    #    axisn = visual.norm( axis )
#    #    curent_axisn = visual.norm( self._get_mt_direction( i ) )
#    #    steps =  180
#    #    mindist = 1000000000000
#    #    minteta = 0
#    #    for z in range( steps ):
#    #        teta=float(z)/steps*2*math.pi
#    #        dist = visual.mag(visual.rotate( curent_axisn, teta, visual.cross( axisn, curent_axisn) ) - axisn)
#    #        if dist < mindist:
#    #            minteta = teta
#    #    self.cell_property( i, "mtb_orientation_angle", minteta)
#


def  pre_2( wtt, cell=None ):
    """Action taken before division
    """
    res = {}
    ## saving mt
    #res["shape"] = wtt.cell2wvs( cell = cell )
    #res["center_of_cell"] = cell_center( wtt, cell = cell )

    ##saving surface
    #surf = calculate_cell_surface( wtt, cell = cell )

    #saving pin:
    pin_c2n={}
    pin_n2c={}
    for i in wtt.cell_neighbors( cell = cell ):
        pin_c2n[ i ] = pin_level( wtt, cell_edge=(cell, i) )
        pin_n2c[ i ] = pin_level( wtt, cell_edge=(i, cell) )
    #saving properties
    saved_prop = {}
    for cp in wtt._cell2properties[ cell ].keys():
            saved_prop[ cp ] = wtt.cell_property( cell, cp)
    
    res["pin_c2n"]=pin_c2n
    res["pin_n2c"]=pin_n2c
    res["saved_prop"]=saved_prop
    return res

def post_2( wtt, pre_res={} ):
    """Actions taken after the division!
    """
    ( ( ( v1d, p1 ), (v2d, p2) ), ( ( v1d, s1 ), ( v1d, t1 ),( v2d, s2 ),( v2d, t2 ),( v1d, v2d ) ), (dict) )  = pre_res["div_desc"]
    saved_prop = pre_res["saved_prop"]
    pin_c2n=pre_res["pin_c2n"]
    pin_n2c=pre_res["pin_n2c"]
    dict=dict[0]
    
    for i in ( dict[ "added_cell1"], dict[ "added_cell2" ] ):
        for cp in saved_prop.keys():
                wtt.cell_property( i, cp, saved_prop[ cp ] )
    
    if saved_prop["PrC"]>0:
        wtt.cell_property( cell=dict["added_cell1"], property="PrC", value= saved_prop["PrC"])
        wtt.cell_property( cell=dict["added_cell2"], property="PrC", value=0 )



    # pumps
    added_cells = [dict["added_cell2"], dict["added_cell1"]]
    for c in added_cells:
        for i in wtt.cell_neighbors( c ):
            if i not in added_cells:
                pin_level( wtt, cell_edge=(c,i), value=pin_c2n[ i ] )
                pin_level( wtt, cell_edge=(i,c), value=pin_n2c[ i ] )

                
    ## automatic IC identity
    if saved_prop["IC"]:
            wtt.cell_property( cell=dict["added_cell1"], property="IC", value=False )
            wtt.cell_property( cell=dict["added_cell2"], property="IC", value=True )



def  pre_3( wtt, cell=None ):
    """Action taken before division.
    
    This actsions are tuned for auxin flux simulation taking an account of cell geometry
    (the number of particles is distributed depanding on the cell surfaces).
    """
    res = {}
    ## saving mt
    #res["shape"] = wtt.cell2wvs( cell = cell )
    #res["center_of_cell"] = cell_center( wtt, cell = cell )

    ##saving surface
    surf = calculate_cell_surface( wtt, cell = cell )

    #saving pin:
    pin_c2n={}
    pin_n2c={}
    for i in wtt.cell_neighbors( cell = cell ):
        pin_c2n[ i ] = pin_level( wtt, cell_edge=(cell, i) )
        pin_n2c[ i ] = pin_level( wtt, cell_edge=(i, cell) )
    #saving properties
    saved_prop = {}
    for cp in wtt._cell2properties[ cell ].keys():
            saved_prop[ cp ] = wtt.cell_property( cell, cp)
    
    res["pin_c2n"]=pin_c2n
    res["pin_n2c"]=pin_n2c
    res["saved_prop"]=saved_prop
    res["cell_surface"]=surf
    return res

def post_3( wtt, pre_res={} ):
    """Actions taken after the division!

    This actsions are tuned for auxin flux simulation taking an account of cell geometry
    (the number of particles is distributed depanding on the cell surfaces).
    """
    ( ( ( v1d, p1 ), (v2d, p2) ), ( ( v1d, s1 ), ( v1d, t1 ),( v2d, s2 ),( v2d, t2 ),( v1d, v2d ) ), (dict) )  = pre_res["div_desc"]
    saved_prop = pre_res["saved_prop"]
    pin_c2n=pre_res["pin_c2n"]
    pin_n2c=pre_res["pin_n2c"]
    dict=dict[0]
    surf = pre_res[ "cell_surface" ]
    
    for i in ( dict[ "added_cell1"], dict[ "added_cell2" ] ):
        for cp in saved_prop.keys():
                wtt.cell_property( i, cp, saved_prop[ cp ] )
    
    if saved_prop["PrC"]>0:
        wtt.cell_property( cell=dict["added_cell1"], property="PrC", value= saved_prop["PrC"])
        wtt.cell_property( cell=dict["added_cell2"], property="PrC", value=0 )

    # pumps
    added_cells = [dict["added_cell2"], dict["added_cell1"]]
    for c in added_cells:
        for i in wtt.cell_neighbors( c ):
            if i not in added_cells:
                pin_level( wtt, cell_edge=(c,i), value=pin_c2n[ i ] )
                pin_level( wtt, cell_edge=(i,c), value=pin_n2c[ i ] )

                
    ## automatic IC identity
    if saved_prop["IC"]:
            wtt.cell_property( cell=dict["added_cell1"], property="IC", value=False )
            wtt.cell_property( cell=dict["added_cell2"], property="IC", value=True )

    #aux
    for c in added_cells:
        s = calculate_cell_surface( wtt, cell = c, refresh=True )
        wtt.cell_property( cell=c, property="auxin_level", value= wtt.cell_property( cell=c, property="auxin_level" )*s/surf )
        
        
        
def  pre_4( wtt, cell=None ):
    """Action taken before division.
    
    This actsions are tuned for auxin flux simulation taking an account of cell geometry
    (the number of particles is distributed depanding on the cell surfaces).
    
    The values stored for PIN and IAA are concentrations.
    """
    res = {}

    #surf = calculate_cell_surface( wtt, cell = cell )

    #saving pin:
    pin_c2n={}
    pin_n2c={}
    for i in wtt.cell_neighbors( cell = cell ):
        pin_c2n[ i ] = pin_level( wtt, cell_edge=(cell, i) )
        pin_n2c[ i ] = pin_level( wtt, cell_edge=(i, cell) )
    #saving properties
    saved_prop = {}
    for cp in wtt._cell2properties[ cell ].keys():
            saved_prop[ cp ] = wtt.cell_property( cell, cp)
    
    res["pin_c2n"]=pin_c2n
    res["pin_n2c"]=pin_n2c
    res["saved_prop"]=saved_prop
    #res["cell_surface"]=surf
    return res

def post_4( wtt, pre_res={} ):
    """Actions taken after the division!

    This actsions are tuned for auxin flux simulation taking an account of cell geometry
    (the number of particles is distributed depanding on the cell surfaces).

    The values stored for PIN and IAA are concentrations.
    """
    ( ( ( v1d, p1 ), (v2d, p2) ), ( ( v1d, s1 ), ( v1d, t1 ),( v2d, s2 ),( v2d, t2 ),( v1d, v2d ) ), (dict) )  = pre_res["div_desc"]
    saved_prop = pre_res["saved_prop"]
    pin_c2n=pre_res["pin_c2n"]
    pin_n2c=pre_res["pin_n2c"]
    dict=dict[0]
    #surf = pre_res[ "cell_surface" ]
    
    for i in ( dict[ "added_cell1"], dict[ "added_cell2" ] ):
        for cp in saved_prop.keys():
                wtt.cell_property( i, cp, saved_prop[ cp ] )
    
    if saved_prop["PrC"]>0:
        wtt.cell_property( cell=dict["added_cell1"], property="PrC", value= saved_prop["PrC"])
        wtt.cell_property( cell=dict["added_cell2"], property="PrC", value=0 )

    # pumps
    added_cells = [dict["added_cell2"], dict["added_cell1"]]
    for c in added_cells:
        for i in wtt.cell_neighbors( c ):
            if i not in added_cells:
                pin_level( wtt, cell_edge=(c,i), value=pin_c2n[ i ] )
                pin_level( wtt, cell_edge=(i,c), value=pin_n2c[ i ] )

    if saved_prop.has_key("PrC_stub"):
        if saved_prop["PrC_stub"]>0:
            wtt.cell_property( cell=dict["added_cell1"], property="PrC_stub", value= saved_prop["PrC"])
            wtt.cell_property( cell=dict["added_cell2"], property="PrC_stub", value=0 )
            
    ## automatic IC identity
    #if saved_prop["IC"]:
    #        wtt.cell_property( cell=dict["added_cell1"], property="IC", value=False )
    #        wtt.cell_property( cell=dict["added_cell2"], property="IC", value=True )

    #aux
    #for c in added_cells:
    #    s = calculate_cell_surface( wtt, cell = c, refresh=True )
    #    wtt.cell_property( cell=c, property="auxin_level", value= wtt.cell_property( cell=c, property="auxin_level" )*s/surf )
    
    
    
def  pre_5( wtt, cell=None ):
    """Action taken before division.
    
    This actsions are tuned for empty cells and full inreritance.
    
    """
    res = {}

    saved_prop = {}
    for cp in wtt._cell2properties[ cell ].keys():
            saved_prop[ cp ] = wtt.cell_property( cell, cp)
    
    res["saved_prop"]=saved_prop
    return res

def post_5( wtt, pre_res={} ):
    """Actions taken after the division!

    This actsions are tuned for empty cells and full inreritance.

    """
    ( ( ( v1d, p1 ), (v2d, p2) ), ( ( v1d, s1 ), ( v1d, t1 ),( v2d, s2 ),( v2d, t2 ),( v1d, v2d ) ), (dict) )  = pre_res["div_desc"]
    saved_prop = pre_res["saved_prop"]
    dict=dict[0]
    
    for i in ( dict[ "added_cell1"], dict[ "added_cell2" ] ):
        for cp in saved_prop.keys():
                wtt.cell_property( i, cp, saved_prop[ cp ] )
    
