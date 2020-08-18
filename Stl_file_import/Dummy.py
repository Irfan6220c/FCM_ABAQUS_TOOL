# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 18:52:36 2018

@author: Srikkanth
"""


from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt
from matplotlib import patches
from shapely.geometry import Polygon
from Writing_triangle_data_to_file import write_triangle_data
from read_triangle_data import read_triangle_data
import numpy as num
from Computation_of_physical_domain import Compute_physical_domain
from Perform_inside_outside_test import In_or_out
from My_CutCell_QuadTree import QuadTree
from My_Gauss_Point_Generator import Gauss_Point_Generator
from My_Alpha_Value_Generator import Alpha_Value_Generator
from Int_Alpha_Value_Generator import Int_Alpha_Value_Generator
from Int_Gauss_Point_Generator import Int_Gauss_Point_Generator
from getGaussCoordinates import getGaussCoordinates
from Int_Quad_Cut_Cell import Cut_Element_Integration

plt.close('all')

#Read_from_Stl(stl_filename,mesh_filename):
stl_filename = 'Plate_with_hole.stl'
mesh_filename = 'Mesh_parameters.txt'

#Creating object by reading the stl file    
My_geometry = mesh.Mesh.from_file(stl_filename)

#mesh_file = 'Mest_Parameters.txt'

#Number of divsions for mesh generations
number_of_divisions=10
#List of triangles from stl file
Triangle_data = My_geometry.vectors
#print(Triangle_data[5][1][1])
No_Triangles = len (My_geometry.vectors)
    
    
#Getting co-ordinates of minimum and maximum points to compute the bounding box
Max_cord = My_geometry.max_
Min_cord = My_geometry.min_

Xmin = Min_cord[0]
Ymin=  Min_cord[1]
Xmax = Max_cord[0]
Ymax = Max_cord[1]
      
#Parameters for the Rectangular patch
left_corner = (Xmin,Ymin)
length = Xmax - Xmin
height = Ymax-Ymin
mesh_size = min(length,height) / number_of_divisions
sheet_size = max(length,height)*1.5   

#Creating the Bounding box
fig = plt.figure()
Bounding_box = patches.Rectangle(left_corner,length,height,fill = False,linestyle = 'dashed',linewidth = 2.0,color = 'r')
ax1 = fig.add_subplot(111,aspect='equal')
ax1.add_patch(Bounding_box)
plt.ylim((Ymin -10),(Ymax+10))
plt.xlim((Xmin-10),(Xmax+10))

#Looping over all the elements and plotting them within the bounding box
for i in range (0,No_Triangles):
    V1 = Triangle_data[i][0]
    V2 = Triangle_data[i][1]
    V3 = Triangle_data[i][2]
    V1_xy = [V1[0],V1[1]]
    V2_xy = [V2[0],V2[1]]
    V3_xy = [V3[0],V3[1]]
    points = [V1_xy,V2_xy,V3_xy]  
    i_th_triangle = patches.Polygon(points)
    ax1.add_patch(i_th_triangle)

#Writing structured mesh parameters to the abacus input file   
fo = open(mesh_filename,'w')
fo.write(str(mesh_size)+'\n')
fo.write(str(Xmin)+'\n')
fo.write(str(Ymin)+'\n')
fo.write(str(Xmax)+'\n')
fo.write(str(Ymax)+'\n')
fo.write(str(sheet_size) + '\n')
fo.write(str(No_Triangles)+'\n')
fo.close()

write_triangle_data(Triangle_data)
File_name = 'Triangle_data_numpy.txt'
Triangle_List = read_triangle_data(File_name,No_Triangles)

###############################################################################
# Reading Element_list
###############################################################################
foo = open('Element_data_1D_array.txt','r')
Element_list = []   # List of lists, each list (temp) contains int, vector,int
temp = []           #List
nodal_connectivity = num.zeros(4,int)
index=0
flag = 0    
num_elem=int(foo.readline())                  #Key : 0 -> Totally outside , 1-> Totaly inside , 2-> Cut element
for i in range(0,num_elem):
    index = int(foo.readline())
    for j in range(0,4):
        nodal_connectivity[j] = int(foo.readline())
            
    temp = [index,nodal_connectivity,flag]
    Element_list.append(temp)
    index=0
    nodal_connectivity = [0,0,0,0]
    #print(Element_list[i])
foo.close()
    
###############################################################################
#Reading Nodal List
###############################################################################
  
fo = open('Node_data_1D_array.txt','r')
Node_list = []      # List of lists, each list (temp) contains int and a vector
temp = []
coordinates = num.zeros(2)  
index = 0
num_node=int(fo.readline())  
for i in range(0,num_node):
    index = int(fo.readline())
    for j in range(0,2):
        coordinates[j] = float(fo.readline())
        if(abs(coordinates[j])<0.000001):
            coordinates[j] =0.0
            
    temp = [index,coordinates]
    index=0
    coordinates = [0.0,0.0]
    Node_list.append(temp)   
fo.close()
    

###############################################################################
#Computation_of_physical_domain
###############################################################################
Phy_domain = Compute_physical_domain(Triangle_List)


###############################################################################
#Perform_inside_outside_test to Elements
###############################################################################
Upadated_Element_list = In_or_out(Element_list,Node_list,Phy_domain,left_corner,length,height,Max_cord,Min_cord)

 
###############################################################################
#Perform_QuadTree_To_Cut_Cells
###############################################################################

print("\nCut Cells QuadTree Generation Starting\n")
Num_of_CutCells= len(Upadated_Element_list[2])
Leaves_list=[]
temp=[]

Leaves_label_list =[]
Int_Leaves_list = []
Alpha_List = []
a=0
#plt.figure()
#plt.gca().set_aspect("equal")
Intg_Input_list = []
Xi_Eta_Intg_pts = []

E = 200
t = 1
Nu = 0.3
for i in range (0,Num_of_CutCells):
    
    del Int_Leaves_list[:]
    del Alpha_List[:]
    del Intg_Input_list[:]
    
    CutCellNum=Element_list[Upadated_Element_list[2][i]-1][0]
    #print (CutCellNum)
    print ("Cut Element ", CutCellNum)
    Node_SW = Element_list[Upadated_Element_list[2][i]-1][1][0]
    Node_SE = Element_list[Upadated_Element_list[2][i]-1][1][1]
    Node_NE = Element_list[Upadated_Element_list[2][i]-1][1][2]
    Node_NW = Element_list[Upadated_Element_list[2][i]-1][1][3]
        
    Xmin = Node_list[Node_SW][1][0]
    Ymin = Node_list[Node_SW][1][1]
    Xmax = Node_list[Node_NE][1][0]
    Ymax = Node_list[Node_NE][1][1]
    Coordinates = [[Xmin,Ymin],[Xmax,Ymin],[Xmax,Ymax],[Xmin,Ymax]]
    tree= QuadTree(CutCellNum,Phy_domain,Xmin, Ymin, Xmax, Ymax, None, 0, "2",0)
    maxLevel =2
    tree.generateQuadtree(maxLevel)
    #plt.figure()
    #plt.figure()
    plt.gca().set_aspect("equal")
    #plt.title("Element"+str(CutCellNum))
    tree.plotTreeToConsole()
    plt.axis('off')
    #tree.writeLeavesToConsole()
#    temp=[CutCellNum,tree.Return_Leaves_list()]
#    #a=tree.Get_myNoOfLeaves()
#    Leaves_list.append(temp)
#    #print (Leaves_list)
#    
#    #temp1=tree.Return_Label_list()
#    #a=tree.Get_myNoOfLeaves()
##    #plt.figure()
##    plt.gca().set_aspect("equal")
    tree.plotTreeToConsole()
    tree.Return_Label_list(Leaves_label_list)
#    #print ("Label list")
#    #print (Leaves_label_list)
#    
#    Leaves_label_list.append([1]) 
#    Leaves_label_list.append([2])
#    Leaves_label_list.append([3])
#    Leaves_label_list.append([4])
#    Leaves_label_list.append([3,3])
#    Leaves_label_list.append([3,4])
#    Leaves_label_list.append([4])
    
    Int_Leaves_list.append(tree.Return_Leaves_list())
    Int_Gauss_Point_Generator(Int_Leaves_list)
    Int_Alpha_Value_Generator(Phy_domain,Int_Leaves_list,Alpha_List)
#    
#    Alpha_List.append([1,1,1,1])
#    Alpha_List.append([1,1,1,1])
#    Alpha_List.append([1,1,1,1])
#    Alpha_List.append([1,1,1,1])
#    Alpha_List.append([1,1,1,1])
#    Alpha_List.append([1,1,1,1])
#    Alpha_List.append([1,1,1,1])
    
    #a=tree.Get_myNoOfLeaves()
    
    for k in range (0,len(Alpha_List)):
        dummy = []
        dummy.append(Leaves_label_list[k])
        dummy.append(Alpha_List[k])
        Intg_Input_list.append(dummy)
#        print (dummy)
    
    #CutCellNum = 1
    #print(Intg_Input_list)
    #Coordinates = [[0,0],[1,0],[1,1],[0,1]]
#    
#
    Xi_Eta_Intg_pts = getGaussCoordinates(Intg_Input_list, CutCellNum) 
#    #print(Intg_Input_list)
#    
    Elem_Integration = Cut_Element_Integration(Coordinates,E,t,Nu,Xi_Eta_Intg_pts)
    Stiffness_Matrix = Elem_Integration.calculate_elastic_stiffness_matrix()
    print(Stiffness_Matrix)
#    
    foo = open("Stifness_matrix_Element_Validation.txt",'w')
    num.savetxt(foo,Stiffness_Matrix)
    foo.close()
    
    
    for z in range(0,1):
        foo = open("Stifness_matrix_Element.txt",'a')
        num.savetxt(foo,Stiffness_Matrix)
        foo.close()
    
###############################################################################
#GaussPointGenerator
###############################################################################
#GP_List=Gauss_Point_Generator(Num_of_CutCells,Leaves_list)

###############################################################################
#GP's Alpha Value Generator
###############################################################################
#Mod_GP_List=Alpha_Value_Generator(Phy_domain,Num_of_CutCells,Leaves_list,GP_List)    
  
   
print("\nCut Cells QuadTree Generation Completed\n")


#print('Intersected Elements',Upadated_Element_list[2])
#print('Elements inside',Upadated_Element_list[1])
#print('Elements outside',Upadated_Element_list[0])

foo = open('Outside_elements.txt','w')
#num.savetxt(foo,Upadated_Element_list[2])
num.savetxt(foo,Upadated_Element_list[0])
foo.close()

foo = open('Cut_elements.txt','w')
num.savetxt(foo,Upadated_Element_list[2])
#num.savetxt(foo,Upadated_Element_list[0])
foo.close()

foo = open('Inside_Elements.txt','w')
num.savetxt(foo,Upadated_Element_list[1])
foo.close()

###############################################################################
#