import os
import path

pkg_path= path.path( '.' )
py_files= list( pkg_path.walkfiles() )

epydoc_options= """
--html
-o html
--name epydoc_test
--docformat restructuredtext
--graph all
--url http://openalea.gforge.inria.fr
"""

opt= ' '.join( epydoc_options.split() )

os.system( 'epydoc %s %s' % ( opt,' '.join( py_files ) ) )

