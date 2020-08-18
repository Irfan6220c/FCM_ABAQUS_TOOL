# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 21:18:52 2018

@author: Srikkanth
"""


from stl import mesh
#from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt
from matplotlib import patches
from shapely.geometry import Polygon

def Read_from_Stl(stl_filename,mesh_filename):

#Creating object by reading the stl file    
    My_geometry = mesh.Mesh.from_file(stl_filename)
#    mesh_file = 'Mest_Parameters.txt'

#Number of divsions for mesh generations   
    number_of_divisions = 10

#List of triangles from stl file
    Triangle_data = My_geometry.vectors
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
    sheet_size = 2.0*length * height    

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
    fo.close()
    
    return Triangle_data
    