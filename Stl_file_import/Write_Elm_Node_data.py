# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 09:26:30 2018

@author: Srikkanth
"""
#%%
"""
This function writes the element and node data to spearate text files in the required format 

Format for Element data      : Element label
                               SW node number
                               SE node number
                               NE node number
                               NW node number
                               
Format for Node data         : Node number
                               x - coordinate
                               y - coordinate
                               
                               
Input : file_name_elem, file_name_node, Num_of_Elem, Num_of_Nodes, element_data, node_data
Ouput : None 
"""
#%%

def Write_Ele_Node_Data_To_File (file_name_elem, file_name_node, Num_of_Elem, Num_of_Nodes, element_data, node_data):
    
    #Writing element data to file in the required format  
    
    Myfile1 = open(file_name_elem,'w')
    Myfile1.write(str(Num_of_Elem)+'\n')
    
    for i in range (0,Num_of_Elem,1):
        
        SW = int(element_data[i].connectivity[0])
        SE = int(element_data[i].connectivity[1])
        NE = int(element_data[i].connectivity[2])
        NW = int(element_data[i].connectivity[3])
        
        elem = int(element_data[i].label)
        
        Myfile1.write(str(elem)+ '\n')
        Myfile1.write(str(SW)+'\n')
        Myfile1.write(str(SE)+'\n')
        Myfile1.write(str(NE)+'\n')
        Myfile1.write(str(NW)+'\n')
        
    Myfile1.close()
    
    ###########################################################################
    
    #Writing node data to file in the required format
    
    Myfile2=open(file_name_node,'w')
    Myfile2.write(str(Num_of_Nodes)+'\n')
    
    for i in range (0,Num_of_Nodes,1):
        
        x = float(node_data[i].coordinates[0])
        y = float(node_data[i].coordinates[1])
        
        node = int(node_data[i].label)
        
        Myfile2.write(str(node)+ '\n')
        Myfile2.write(str(x)+ '\n')
        Myfile2.write(str(y)+ '\n')
    
    Myfile2.close()
#%%