#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 17:07:07 2018

@author: JadyWu
"""

import numpy as np
from matplotlib import path
#from matplotlib import polygon
p = path.Path([(0,0), (0, 1), (1, 1), (1, 0)])  # square with legs length 1 and bottom left corner at the origin
points = np.array([0.3, 0.3, 1, 1.5, 0.0, 0.0]).reshape(3, -1)
print (points)
print (p.contains_points(points))