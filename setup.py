
import sys
import os

from setuptools import setup, find_packages
from os.path import join as pj

build_prefix = "build-scons"


# Header

# Setup script

# Package name
name = 'stse'
namespace = 'openalea'
pkg_name= namespace + '.' + name

# Package version policy
version= '1.0.0' 

# Description
description= 'Space-time simulation environment' 
long_description= '''
Spatio-temporal simulation environment (STSE) is set of open-source tools used to
perform spatio-temporal simulations in discret structures. The framework
contains modules to represent, analyse, and model spatial distributions of
species in static and dynamic (e.g. growing) structures. '''

# Author
author= 'Szymon Stoma'
author_email= ''
url= 'http://stoma.name/stse/'
license= 'Cecill-C' 



# Main setup
setup(
    # Meta data
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    keywords = '',

    
    # Define what to execute with scons
    #scons_scripts=['SConstruct'],
    #scons_parameters=["build","build_prefix="+build_prefix],

    # Packages
    namespace_packages = [namespace],
    create_namespaces = True,
    py_modules = [],
    packages =  [ 'openalea.stse.' + x for x in find_packages('src/stse/') ],
    package_dir = { 'openalea.stse':  pj('src','stse'), "":"src" },
    packages.append( 'openalea.stse' )
    print "# Installing packages: ", packages

    
    include_package_data = True,
    package_data = {'' : ['*.pyd', '*.so'],},

    zip_safe= False,

    #lib_dirs = {'lib' : pj(build_prefix, 'lib'), },
    #inc_dirs = { 'include' : pj(build_prefix, 'include') },
    #share_dirs = { 'tutorial' : pj('examples','tutorial')},
    
    #postinstall_scripts = [],

    # Scripts
    entry_points = { 'gui_scripts': [
	    'stse_compartment_editor = openalea.stse.gui.compartment_editor:start_gui',
	    'stse_compartment_viewer= openalea.stse.gui.compartment_viewer:start_gui',
	    ]},


    # Dependencies
    setup_requires = ['openalea.deploy'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
    install_requires = [],


    )


