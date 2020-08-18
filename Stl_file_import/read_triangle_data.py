# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 02:41:59 2018
Reading triangle data
@author: Srikkanth
"""

import numpy as py

def read_triangle_data(File_name,tri_length):
    fo = open(File_name,'r')
    data= py.loadtxt(fo)
    Triangle_list = []
    for i in range(0,tri_length):
        V1 = data[(3*i)+0]
        V2 = data[(3*i)+1]
        V3 = data[(3*i)+2]
        dummy = [V1,V2,V3]
        Triangle_list.append(dummy)
    
        fo.close()
    return Triangle_list