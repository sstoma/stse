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



def  pre( wtt, cell=None ):
    """Action taken before division
    """
    res = {}
    #saving properties
    saved_prop = {}
    for cp in wtt._cell2properties[ cell ].keys():
            saved_prop[ cp ] = wtt.cell_property( cell, cp)
    res["saved_prop"]=saved_prop
    return res

def post( wtt, pre_res={} ):
    """Actions taken after the division!
    """
    ( ( ( v1d, p1 ), (v2d, p2) ), ( ( v1d, s1 ), ( v1d, t1 ),( v2d, s2 ),( v2d, t2 ),( v1d, v2d ) ), (dict) )  = pre_res["div_desc"]
    saved_prop = pre_res["saved_prop"]
    dict=dict[0]
    
    for i in ( dict[ "added_cell1"], dict[ "added_cell2" ] ):
        for cp in saved_prop.keys():
                wtt.cell_property( i, cp, saved_prop[ cp ] )
