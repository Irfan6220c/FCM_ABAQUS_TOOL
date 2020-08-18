# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 02:34:24 2018
Writing the triangle deatils into output file
@author: Srikkanth
"""
import numpy as py

def write_triangle_data(Triangle_data):
    
    file_name = 'Triangle_data_numpy.txt'
    fo = open(file_name,'w')
    length = len(Triangle_data)
    
    for i in range(0,length):
        py.savetxt(fo,Triangle_data[i])
        
    fo.close()
        
 