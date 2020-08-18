# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 18:36:32 2018

@author: Boulbrachene
"""

from shapely.geometry import Point
from matplotlib import pyplot as plt

def Int_Alpha_Value_Generator(Phy_domain,Int_GP,Alpha_List):
    
    
    Leaves_Per_Cell=len(Int_GP[0])
    print(Leaves_Per_Cell)
    for i in range (0,Leaves_Per_Cell):
        temp=[]
         
        for k in range (0,4):
            x=Int_GP[0][i][2][k]
            y=Int_GP[0][i][3][k]
            GP=Point(x,y)
#                 plt.plot([x],[y], 'go')
               
#                 GP_Two=Point(GP_List[i][1][j][1][1],GP_List[i][1][j][2][1])
#                 GP_Three=Point(GP_List[i][1][j][1][2],GP_List[i][1][j][2][2])
#                 GP_Three=Point(GP_List[i][1][j][1][3],GP_List[i][1][j][2][3])
                 
            if Phy_domain.contains(GP) :  #Check for GPs Inside and give alpha=1
                temp.append(1)
                    
                plt.plot([x],[y], 'go')
            else:  #Otherwise the GP has to be outiside and alpha=0
                temp.append(0)
                plt.plot([x],[y], 'ro')
                plt.plot(x,y,color='red')
        Alpha_List.append(temp)