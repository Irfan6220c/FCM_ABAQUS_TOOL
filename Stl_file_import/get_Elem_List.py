# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 10:59:47 2018

@author: Srikkanth
"""
"""
This functions returns a list of element labels of cut/inside/outside

Input : Text file name containing the element labels:
Output : List of element labels
"""
#%%
import numpy as num

#%%

def Get_Element_list (file_name) :
    
    foo = open(file_name,'r')
    element_list = num.loadtxt(foo)
    foo.close
    
    return element_list

#%%