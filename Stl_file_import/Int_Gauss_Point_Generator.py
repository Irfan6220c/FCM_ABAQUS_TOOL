# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 18:35:51 2018

@author: Boulbrachene
"""
import math 

def Int_Gauss_Point_Generator(Int_Leaves_list):
    Leaves_Per_Cell=len(Int_Leaves_list[0])
    for i in range (0,Leaves_Per_Cell):
            
        Xmin= Int_Leaves_list[0][i][0][0]
        Xmax= Int_Leaves_list[0][i][1][0]
        Ymin= Int_Leaves_list[0][i][0][1]
        Ymax= Int_Leaves_list[0][i][1][1]
        deltaX=Xmax-Xmin
        deltaY=Ymax-Ymin
        
        xCordone=Xmin + (deltaX/2)*(1-(1/math.sqrt(3)))
        xCordtwo=Xmax - (deltaX/2)*(1-(1/math.sqrt(3)))
        xCordthree=xCordtwo
        xCordfour=xCordone
        
#                xCordone=(deltaX/2)*(1/math.sqrt(3))
#                xCordtwo=(deltaX/2)*(1/math.sqrt(3))
#                xCordthree=xCordtwo
#                xCordfour=xCordone
        
        yCordone=Ymin + (deltaY/2)*(1-(1/math.sqrt(3)))
        yCordtwo=yCordone
        yCordthree=Ymax - (deltaY/2)*(1-(1/math.sqrt(3)))
        yCordfour=yCordthree
        
#                yCordone=(deltaY/2)*(1/math.sqrt(3))
#                yCordtwo=yCordone
#                yCordthree=(deltaY/2)*(1/math.sqrt(3))
#                yCordfour=yCordthree
        
        xCords=(xCordone,xCordtwo,xCordthree,xCordfour)
        yCords=(yCordone,yCordtwo,yCordthree,yCordfour)
        Int_Leaves_list[0][i].append(xCords)
        Int_Leaves_list[0][i].append(yCords)
        
    return Int_Leaves_list
            