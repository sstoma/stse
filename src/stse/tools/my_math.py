#!/usr/bin/env python


from numpy import sqrt, power
from scipy.integrate import quadrature

def curve_length( f=None, x0=0., x1=1., tolerance=0.01  ):
    """Return the lenght of a curve f (for which we know the derivate f_prim),
    from x0 to x1.
    
    <Long description of the function functionality.>
    
    :parameters:
        f_prim : function
            Curve funtion.
    :rtype: float
    :return: The length of a curve
    """
    assert x0 <= x1
    if x0 == x1: return 0.    
    return quadrature(lambda x: sqrt(1+power(f(x), 2)), x0, x1, tol=tolerance)[0]

def new_argrument_for_given_curve_length( f=None, x0=0., length=0., tolerance=0.01 ):
    """Returns new argument x1 such as the function f curve length between x0 and x1 is
    equal length.
    
    <Long description of the function functionality.>
    
    :parameters:
        f : function
            function
        x0 : float
            point of a function
        length : float
            desired length
    :rtype: float
    :return: As in function description
    """
    ratio=2.
    if x0 == 0: x0=0.001
    x1=x0+ratio*x0
    while curve_length(f=f,x0=x0, x1=x1) < length:
        x1 += x1*ratio
    
    return bisection(lambda x: length-curve_length(f=f,x0=x0,x1=x), x0=x0, x1=x1, tolerance=tolerance)
    
    
def bisection( f=None, x0=0., x1=1., tolerance=0.1 ):
    """Bisection algorithm
    
    <Long description of the function functionality.>
    
    :parameters:
        f : function
            Function which root we would like to find
        x0: float
            left boundary
        x1: float
            right boundary
        tolerance : float
            tolerance
    :rtype: float
    :return: root of f with epsilon tolerance.
    """
    assert x0 < x1
    assert f(x0)*f(x1) <= 0
    while abs(x1-x0) > 2*tolerance:
        midpoint = (x1+x0)/2.
        if f(x0)*f(midpoint) > 0: x0 = midpoint
        else: x1=midpoint
    return (x0+x1)/2.
