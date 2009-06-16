#!/usr/bin/env python

"""Functions containing auxin/pin utils.


:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    INRIA/HU

"""

# Module documentation variables:
__authors__="""Szymon Stoma    
"""
__contact__=""
__license__="Cecill-C"
__date__="pia mar 30 14:50:15 CEST 2007"
__version__="0.1"
__docformat__= "restructuredtext en"
__revision__="$Id$"


import copy



def pin_level( wtt, cell_edge=None, value=None ):
    wv_edge = cell_edge2wv_edge( wtt, cell_edge=cell_edge )
    try:
        p = pin_level_wv_edge( wtt=wtt, wv_edge=wv_edge, cell_edge=cell_edge, value=value )
    except Exception:
        print " ! pin_level exception.."
        return 0.
    return p

def pin_level_wv_edge( wtt, wv_edge=None, cell_edge=None, value=None ):
    ce = wtt.cell_edge_id( cell_edge )
    s = wtt.wv_edge_property( wv_edge = wtt.wv_edge_id( wv_edge ) , property="pin_level")
    if value == None:    
        #s = wtt.wv_edge_property( wv_edge = wtt.wv_edge_id( wv_edge ) , property="pin_level")  
        if ce == cell_edge:
            return s[ 0 ]
        else:
            return s[ 1 ]
    else:
        s=copy.copy(s)
        if ce == cell_edge:
            s[ 0 ] = value
        else:
            s[ 1 ] = value
        wtt.wv_edge_property( wv_edge = wtt.wv_edge_id( wv_edge ) , property="pin_level", value=s)
        #print "pin", s, wtt.wv_edge_property( wv_edge = wtt.wv_edge_id( wv_edge ) , property="pin_level")


def auxin_level( wt, cell=None, value=None ):
    if value==None:
        return wt.cell_property( cell=cell, property="auxin_level" )
    else:
        wt.cell_property( cell=cell, property="auxin_level", value=value )


def comparePIN_1( wt1=None, wt2=None, tol1=0., tol2=0 ):
    """<Short description of the function functionality.>
    
    <Long description of the function functionality.>
    
    :parameters:
        arg1 : `T`
            <Description of `arg1` meaning>
    :rtype: `T`
    :return: <Description of ``return_object`` meaning>
    :raise Exception: <Description of situation raising `Exception`>
    """
    con=0
    incon=0
    ce1=wt1.cell_edges()
    for (s,r) in ce1:
        #print i,j, pin_level(wt1, (i,j)),pin_level(wt2, (i,j)) 
        for (i,j) in [(s,r), (r,s)]:
            #print i,j, pin_level(wt1, (i,j)),pin_level(wt2, (i,j)) 
            if pin_level(wt1, (i,j)) > tol1:
                if pin_level(wt2, (i,j)) > tol2:
                    con+=1
            if pin_level(wt1, (i,j)) < tol1:
                if pin_level(wt2, (i,j)) < tol2:
                    con+=1
            (i,j) = (j,i)    
    return float(con)/float(len(ce1))/2.


def comparePIN_2( wt1=None, wt2=None, tol1=0., tol2=0 ):
    """<Short description of the function functionality.>
    
    <Long description of the function functionality.>
    
    :parameters:
        arg1 : `T`
            <Description of `arg1` meaning>
    :rtype: `T`
    :return: <Description of ``return_object`` meaning>
    :raise Exception: <Description of situation raising `Exception`>
    """
    con=0
    acon=0
    pos_pumps=0
    neg_pumps=0

    ce1=wt1.cell_edges()

    for (s,r) in ce1:
        #print i,j, pin_level(wt1, (i,j)),pin_level(wt2, (i,j)) 
        for (i,j) in [(s,r), (r,s)]:
            if pin_level(wt1, (i,j)) > tol1:
                if pin_level(wt2, (i,j)) > tol2:
                    con+=1
                pos_pumps+=1
            if pin_level(wt1, (i,j)) < tol1:
                if pin_level(wt2, (i,j)) < tol2:
                    acon+=1
                neg_pumps+=1
    
    if pos_pumps>0: x=float(con)/float(pos_pumps)
    else: x=1.
    if neg_pumps>0:  y=float(acon)/float(neg_pumps)
    else: y=1.
    if pos_pumps+neg_pumps>0: z=float(con+acon)/float(neg_pumps+pos_pumps)
    else: z=1.
    return x,y,z