#!/usr/bin/env python
"""Processing the config of tissue representation.

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

from os.path import join
from IPython.external.path import path
from openalea.stse.structures.walled_tissue import WalledTissue
from openalea.stse.structures.walled_tissue_const import WalledTissueConst
from openalea.stse.structures.algo.walled_tissue import create
from openalea.stse.io.walled_tissue.dat_representation import read_dat2walled_tissue, read_link_file
from openalea.plantgl.math import Vector3
import openalea.plantgl.all as pgl
import openalea.plantgl.ext.all as pd
import math
import copy


class Config:
    """ Load a python configuration file. """
    def __init__(self, filename):
        """Loads tissue configuration file and copies all variables as
        methods and datafields of Config class.
        
        :parameters:
            filename : string
                Path to file containing config.
        """    
        print " #: reading..", filename
        execfile(filename, self.__dict__)


def read_dat_tissue_directory( config ):
    """Reads tissue data into walled_tissue structure. 
    
    <Long description of the function functionality.>
    
    :parameters:
        config : string
            Filename of file containing config. If None config is taken from
            current directory from config.py
    :raise Exception: <Description of situation raising `Exception`>
    """
    
    if config: c = Config( config )
    else: c = Config( "config.py")
    
    #print "cells to remove:", c.remove_cell_list
    #print "cell_properties:", c.cell_properties
    
    # we define the set of settings for a tissue
    wtc = WalledTissueConst( name = c.description,
                      tissue_properties = c.const.tissue_properties,
                      wv_properties = c.const.wv_properties,
                      wv_edge_properties = c.const.wv_edge_properties,
                      cell_properties = c.const.cell_properties,
                      cell_edge_properties = c.const.cell_edge_properties )
    
    
    
    links = read_link_file( link_fn = join( path( c.file_folder), path( c.link_file ) ) )
    if links:    
        # we declare the set of properties for every cell edge
        # it corresponds to the protein PIN level
        wtc.cell_edge_properties.update( { copy.copy(c.link) : 0. } )

    #wt = WalledTissue(const = wtc)
    
    # we initialize the tissue using the data read from
    # .dat file Specification can be found in the stsf
    # documentation
    t = read_dat2walled_tissue( filename = join( path( c.file_folder ), path( c.dat_file ) ), tissue_properties = wtc, screen_coordinates = True)

    if links:
        print " # adding links"
        for (i,j) in links:
            try:
                t.directed_cell_edge_property((int(i), int(j)), c.link, 1. )
            except Exception:
                print " ! link not added:", i,j    
    
    # scalling
    # moving to have the center of the meristem in the (0,0,0)
    # rotating
    avg=Vector3()
    for i in t.wvs():
        t.wv_pos(i, t.wv_pos(i)*c.scale_factor)
        avg+=t.wv_pos(i)
    
    if c.translation:
        avg = avg/float(len(t.wvs()))
        for i in t.wvs():
            t.wv_pos(i, t.wv_pos(i)-avg)
    
    if c.rotation:
        m = pgl.Matrix3().axisRotation((0,0,1),c.rotation)
        for i in t.wvs():
            t.wv_pos(i, m*t.wv_pos(i))
     
    for i in c.remove_cell_list:
        t.remove_cell(i)
                 
    # setting cell properties
    for i in c.cell_properties.keys():
        if i in c.const.cell_properties.keys():
            for j in c.cell_properties[ i  ].keys():
                t.cell_property(j, i, c.cell_properties[ i  ][ j ] )
    
    # setting cell_edge properties
    for i in c.cell_edge_properties.keys():
        if i in c.const.cell_edge_properties.keys():
            for j in c.cell_edge_properties[ i  ].keys():
                t.cell_edge_property(j, i, c.cell_edge_properties[ i  ][ j ] )            
    
    # setting wv properties
    for i in c.wv_properties.keys():
        if i in c.const.wv_properties.keys():
            for j in c.wv_properties[ i  ].keys():
                t.wv_property(j, i, c.wv_properties[ i  ][ j ] )
                
    # setting wv_edge properties
    for i in c.wv_edge_properties.keys():
        if i in c.const.wv_edge_properties.keys():
            for j in c.wv_edge_properties[ i  ].keys():
                t.wv_edge_property(j, i, c.wv_edge_properties[ i  ][ j ] )
                
    for i in c.post_procedures:
        i( t )
    return t
