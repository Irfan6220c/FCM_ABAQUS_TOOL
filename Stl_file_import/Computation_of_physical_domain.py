# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 03:09:36 2018

@author: Srikkanth
"""

#To perform_inside_outside_test

from matplotlib import pyplot as plt
import shapely.geometry as shape

def Compute_physical_domain(Triangle_List):
    

    num_triangle =  len(Triangle_List)
#    num_elements =  len(Element_list)
#    num_nodes = len(Node_list)
    
    t=[]
#    fig1 = plt.figure()
#    ax1 = fig1.add_subplot(111,aspect='equal')
    Physical_geometry = shape.Polygon()
    for  i in range (0,num_triangle):
        V1 = Triangle_List[i][0]
        V2 = Triangle_List[i][1]
        V3 = Triangle_List[i][2]

        V1_xy = [V1[0],V1[1]]
        V2_xy = [V2[0],V2[1]]
        V3_xy = [V3[0],V3[1]]
        
        Point_list = [V1_xy,V2_xy,V3_xy]
        
       
        i_th_triangle = shape.Polygon(Point_list)
#        ax1.add_patch(i_th_triangle)
        #print(i_th_triangle)
        t.append(i_th_triangle)
        
    

    for i in range(0, num_triangle):
        Physical_geometry = Physical_geometry.union(t[i])
    
    return Physical_geometry

