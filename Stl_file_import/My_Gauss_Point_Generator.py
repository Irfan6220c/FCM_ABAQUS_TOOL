# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 16:22:14 2018

@author: Boulbrachene
"""
import math 
GP=[] 
temp=[]
def Gauss_Point_Generator(Num_of_CutCells,Leaves_list):
   
    #This function returns Gauss Points coordinates of each Leaf
    for i in range (0,1):
        del temp[:]
        Leaves_Per_Cell=len(Leaves_list[i][1])
        for j in range (0,Leaves_Per_Cell):
                Xmin= Leaves_list[i][1][j][0][0]
                Xmax= Leaves_list[i][1][j][1][0]
                Ymin= Leaves_list[i][1][j][0][1]
                Ymax= Leaves_list[i][1][j][1][1]
                deltaX=Xmax-Xmin
                deltaY=Ymax-Ymin
                
                xCordone=Xmin + (deltaX/2)*(1-1/math.sqrt(3))
                xCordtwo=Xmax - (deltaX/2)*(1-1/math.sqrt(3))
                xCordthree=xCordtwo
                xCordfour=xCordone
                
                yCordone=Ymin + (deltaY/2)*(1-1/math.sqrt(3))
                yCordtwo=yCordone
                yCordthree=Ymax - (deltaY/2)*(1-1/math.sqrt(3))
                yCordfour=yCordthree
                
                xCords=(xCordone,xCordtwo,xCordthree,xCordfour)
                yCords=(yCordone,yCordtwo,yCordthree,yCordfour)
                temp.append([j+1,xCords,yCords])
                
                
        GP.append([Leaves_list[i][0],temp[:]])
        
    
    return GP
            