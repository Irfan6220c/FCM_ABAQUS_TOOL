# -*- coding: utf-8 -*-
"""
Created on Wed May  9 16:28:17 2018

@author: Srikkanth
"""

from sys import path
path.append('C:\Users\Srikkanth\Anaconda3\envs\py27\Lib\site-packages')
    
from abaqus import *
import numpy as num
from part import *
from material import *
from section import *
from assembly import *
from step import *
from load import *
from mesh import *
from job import *
from sketch import *
from Abaqus_functions import *
from Utility_functions_ABAQUS import *

def main():
  
###############################################################################
    
    #Parameters to be entered
    
    Elastic_modulus = 200000        #(N/mm^2)
    Poisson_Ratio = 0.3
    Thickness = 1.0                 #Thickness of the plane stress element (mm)
    Epsilon = 0.0000000001          # Set this value to define stiffness for outside elements
    
##############################################################################3
    
    
    mesh_filename = 'Mesh_Parameters.txt'
    mesh_size = 0.0
    Rectangle = num.zeros((2,2))
    sheet_size = 0.0
    num_triangles = 0.0
    
    f=open(mesh_filename,'r')
    mesh_size = float(f.readline())
    Rectangle = num.zeros((2,2))
    Rectangle[0][0] = float(f.readline())
    Rectangle[0][1] = float(f.readline())
    Rectangle[1][0] = float(f.readline())
    Rectangle[1][1] = float(f.readline())
    sheet_size = float(f.readline())
    num_triangles = int(f.readline())
    
    f.close()
    
##############################################################################
    
    #Part creation
    Create_Part(sheet_size, Rectangle)
   
###############################################################################
    
    #Mesh generation
    Generate_Mesh(mesh_size, Rectangle)    
       
##############################################################################
    
    #Computing the number of nodes and elements
    
    element_data  = mdb.models['Model-1'].parts['Part-1'].elements
    node_data  = mdb.models['Model-1'].parts['Part-1'].nodes
    
    Num_of_Elem = len(element_data)
    Num_of_Nodes = len (node_data)
    
###############################################################################
    
    #Writing the element and node data to the text files    
    
    file_name_elem = 'Element_data_1D_array.txt'
    file_name_node = 'Node_data_1D_array.txt'
    Write_Ele_Node_Data_To_File (file_name_elem, file_name_node, Num_of_Elem, Num_of_Nodes, element_data, node_data )
    
###############################################################################
    
    # Create a list of element and nodes
      
    Element_list = create_element_list(file_name_elem,Num_of_Elem)
    Node_list = create_node_list(file_name_node,Num_of_Nodes)
    
###############################################################################
    
    # Create a list of cut elements
    file_name = 'Cut_elements.txt'
    element_list_cut = Get_Element_list(file_name)
        
    # Create a list of outside elements
    file_name = 'Outside_elements.txt'
    element_list_outside = Get_Element_list(file_name)
    
    # Create a list of inside elements
    file_name = 'Inside_Elements.txt'
    element_list_inside = Get_Element_list(file_name)
  
##############################################################################
    
    #Generate orphan mesh
    
    #Creating an alias for the Abaqus part object
    p = mdb.models['Model-1'].parts['Part-1']
    #Creating an alias for the Abaqus model object
    M = mdb.models['Model-1']
    #Creating an alias for the Abaqus ophan part object
    P = Generate_Orphan_Mesh (p)
     
    #deleting the orginal part an retaining only the orphan mesh object
    del p
    
###############################################################################
   
    ##Create_element sets 
    
    #Creating an alias for the Abaqus element array oject
    e = P.elements
    
    #Creating element set for cut elements
    Set_name = 'Cut'
    Create_Element_Sets (e,element_list_cut,P,Set_name)
    
    #Creating element set for inside elements   
    Set_name = 'Inside'
    Create_Element_Sets (e,element_list_inside,P,Set_name)
    
    #Creating element set for inside elements   
    Set_name = 'Outside'
    Create_Element_Sets (e,element_list_outside,P,Set_name)
    
###############################################################################
    
    ### Create Material   
    Create_Material (M, Elastic_modulus, Epsilon, Poisson_Ratio)
        
###############################################################################
    
    # Creating sections
    Create_Solid_Section (M,Thickness)
    
###############################################################################
    
    #Assigning sections    
    Assign_Sections (P,M)   
    
###############################################################################
    
    #Creating assembly  
    M.rootAssembly.Instance(name = 'Orphan_Mesh_Assembly', part = P)
    
###############################################################################
    
    #Creating Step  
    M.StaticStep(name = 'Static_load_case', previous = M.steps['Initial'].name)
    
###############################################################################
#%%
    """
    The following section is valid only for a plate with hole.

    The loading conditons, Nodes for applying conditons for other problems are different
    Comment the following section and use the GUI to apply load and BCs
    """
   
    #Creating Node sets for Dirichlet and Nuemann BC
    Create_Node_Sets_For_Load_BC (P,M,Rectangle)
    
###############################################################################
    
    #Creating Dirichlet BC
    
    #Fixing y displacement for all the nodes on the bottom edge
    M.DisplacementBC(name='Y_disp_fixed', createStepName = M.steps['Static_load_case'].name, region=M.rootAssembly.sets['BC_X_dirichlet'], u2=0.0)
    
    #Fixing x displacement for all the nodes on the left edge
    M.DisplacementBC(name='X_disp_fixed', createStepName = M.steps['Static_load_case'].name, region=M.rootAssembly.sets['BC_Y_dirichlet'], u1=0.0)
    
###############################################################################
    
    #Creating Dirichlet BC
    #Surface traction applied on the top surface
    M.SurfaceTraction(name = 'Surface_traction', createStepName = M.steps['Static_load_case'].name, region = M.rootAssembly.surfaces['Loading_edge'], magnitude = 100.0, directionVector = ((0.0,0.0,0.0),(0.0,1.0,0.0),), traction = GENERAL) 
    
###############################################################################
    
    #Creating Job   
    Job = mdb.Job(name='Test_run', model = M)
    #Creating the input file
    Job.writeInput()
    
###############################################################################
#%%

main()

#%%