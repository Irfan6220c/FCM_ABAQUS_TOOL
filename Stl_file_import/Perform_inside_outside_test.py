# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 12:49:39 2018

@author: Srikkanth
"""

#Perform inside_outside_test and return updated_element_list


from matplotlib import pyplot as plt
import shapely.geometry as shape
from matplotlib import patches

def In_or_out(Element_list,Node_list,Phy_domain,left_corner,length,height,Max_cord,Min_cord):

###############################################################################    
    Element_list_updated = []
    fig = plt.figure()
    ax1 = fig.add_subplot(111,aspect='equal')
    Xmin = Min_cord[0]
    Ymin=  Min_cord[1]
    Xmax = Max_cord[0]
    Ymax = Max_cord[1]
    Box= patches.Rectangle(left_corner,length,height,fill = False,linewidth = 3.0,color = 'black')
    ax1.add_patch(Box)
    plt.ylim((Ymin -10),(Ymax+10))
    plt.xlim((Xmin-10),(Xmax+10))
    fig.show()
    
###############################################################################    
    
    #Domain = shape.Polygon(Phy_domain)
    len_elem = len(Element_list)
#    len_node = len(Node_list)
    intersect = []
    inside = []
    outside = []
    
    for i in range(0,len_elem):
        Node_SW = Element_list[i][1][0]  
        Node_SE = Element_list[i][1][1] 
        Node_NE = Element_list[i][1][2] 
        Node_NW = Element_list[i][1][3] 
    
        cord_Node_SW = Node_list[Node_SW][1]
        cord_Node_SE = Node_list[Node_SE][1]
        cord_Node_NE = Node_list[Node_NE][1]
        cord_Node_NW = Node_list[Node_NW][1]
    
        i_th_Element = shape.Polygon([(cord_Node_SW),(cord_Node_SE),(cord_Node_NE),(cord_Node_NW)])
        x,y = i_th_Element.exterior.xy
        
        if Phy_domain.contains(i_th_Element) :  #Check for Elements Inside First
        
            Element_list[i][2] = 1
            inside.append(Element_list[i][0])
            x,y = i_th_Element.exterior.xy
           # plt.plot(x,y,color='green', linewidth = 1.0)
            
        elif i_th_Element.intersects(Phy_domain):
        
            Element_list[i][2] = 2
            intersect.append(Element_list[i][0])
            x,y = i_th_Element.exterior.xy
            plt.plot(x,y,color='blue', linewidth = 2.0)  # Plot Intersected Elements
        
        else:
            Element_list[i][2] = 0
            outside.append(Element_list[i][0])
            x,y = i_th_Element.exterior.xy
            #plt.plot(x,y,color='Red', linewidth =1.0)
    
    Element_list_updated = [outside,inside,intersect]
    return Element_list_updated
    