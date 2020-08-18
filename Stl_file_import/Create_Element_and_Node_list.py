# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 01:28:14 2018

@author: Srikkanth
"""

#%%
import numpy as num
#%%
def create_element_list(filename,Num_of_Elem):
    """
    This function creates a list of elements from a given text list
    
    The data structure of the element list is as follows :
        
        Element_list[i] = [index, nodal_connectivity, flag]
        where:
            index -> the label for the element
            nodal -> nodal connectivity in counter clockwise direction starting with the South_West node
            flag  -> key to identify if element is cut, inside or outside
    
    
    Input : Filename to be read from, Number of elements
    Output : List of all Elements
    """
    
    foo = open('Element_data_1D_array.txt','r')
    Element_list = []
    temp = []
    nodal_connectivity = num.zeros(4,int)
    index=0
    flag = 0                               #Key : 0 -> Totally inside, 1-> Totaly outside, 2-> Cut element
    
    #looping over all the elements
    for i in range(1,Num_of_Elem):
        index = int(foo.readline())
        for j in range(0,4):
            nodal_connectivity[j] = int(foo.readline())
            
        temp = [index,nodal_connectivity,flag]
        Element_list.append(temp)
        index=0                           # Re-initialising the variable for next loop  
        nodal_connectivity = [0,0,0,0]    # Re-initialising the variable for next loop
   
    foo.close()
    
    return Element_list

#%%

def create_node_list(filename,NumNodes):
    """
    This function creates a list of nodes from a given text list
    
    The data structure of the node list is as follows :
        
        Node_list[i] = [index, [corodinates]]
        where:
            index -> the label for the node
            [coordinates] ->  list of x and y coordinates [x,y]
    
    Input : Filename to be read from, Number of nodes
    Output : List of all Nodes
    """
    
    fo = open(filename,'r')
    Node_list = []
    temp = []
    coordinates = num.zeros(2)
    index = 0
    index = int(fo.readline())
    
    #looping over all the nodes
    for i in range(1,NumNodes):        
        for j in range(0,2):
            coordinates[j] = float(fo.readline())
            if(abs(coordinates[j])<0.000001):
                coordinates[j] =0.0
            
        temp = [index,coordinates]
        index=0                         # Re-initialising the variable for next loop 
        coordinates = [0.0,0.0]         # Re-initialising the variable for next loop 
        Node_list.append(temp)
        
    fo.close()
    
    return Node_list
#%%
