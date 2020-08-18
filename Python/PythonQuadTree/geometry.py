#geometry.hpp
#Created on: Jun 20, 2018
#   Author: Jady
#

#impilicit Function#
def implicitFunction(x,y):
    radius = 0.5
    if ((x-2.0) * (x-2.0) + (y-2.0) * (y-2.0)) > radius * radius:
        return False 
    else:
        return True
