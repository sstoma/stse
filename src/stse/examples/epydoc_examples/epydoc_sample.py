"""The module `epydoc_sample` provides the examplary use
of ``epydoc`` directives.

Here we gather almost all important comment directives which
could be used in ``epydoc`` restructured text. In the submodule
`epydoc_template` we provide the customizable template
which we could use while developing for *vplatns*.

Please do not use this file as a template. Use epydoc_template instead.
Here we could present some useful syntax and threat it as examplary file.

Detailed description presenting the properties of ``module``. In short:

    * property1:
        - subproperty1,
        - subproperty2.
    * property2.

Specials (should appear in bold):
    * property1,
    * property2.
    
:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    INRIA

:see:
    http://google.com/

:note:
    A basic note.    
"""
__authors__="""    Szymon Stoma
"""
__contact__="mis.kolargol@inria.fr"
__license__="Cecil-C"
__date__="pia mar 30 09:18:16 CEST 2007"
__version__="0.1"
__docformat__= "restructuredtext en"


global_variable1 = 1
"""Describes global_variable1. (comment got through introspection)
"""

#: Describes global_variable2. (comment got through parsing)
global_variable2 = 1


class A:
    """The examplary `A` class.
    
    This class is nothing but a stub.
    """
    pass


def fun( param1=[], param2=[]):
    """The `fun` checks the equality of its parameters converted to boolean.
    
    The `fun` must be run with *caution* for one parameter, hence:
    
        .. python::
            fun( 1 )
            >>> True
            
    :parameters:
        param1 : `bool` convertable
            Stafdsjlk ldkfjladskjfklajflkjasdl l lkdslk
            flksdjflksjdal ksldkflkas flkasjdklfslakfj laksjlk lfdsaflksajlkfsalkfj aslkdfjlkasjfldksa  arg1.
        param2 : `bool` convertable
            arg2. fdsaf df asfddasfaslkj lkjskld lkjdfkl salkkajdklf lkasf kk kljsd fkaklk lasfdlklkf lkaskl
            fjlkadslkfsa lfsakljlks asd kfaslkjklkjkldf   fdskfj sfk fsk dfkdf dkk.
     
    :raise Exception1:
        dummy exception thrown when one of the arguments is not-boolean convertable.
    
    :raise Exception2:
        dummy exception thrown when one of the arguments is not-boolean convertable.

    :rtype: `bool`
    
    :return: True iff the params are equal. 

    :precondition: sth about the precond..
    
    :postcondition: sth about the postcond..
    
    :invariant: sth about the invariant..
            
"""
    try:    
        return bool( param1 ) == bool( param2 )
    except:    
        raise Exception("One of the arguments is not-boolean convertable.")