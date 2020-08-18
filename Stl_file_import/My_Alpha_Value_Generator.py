# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 18:52:51 2018

@author: Boulbrachene
"""
from shapely.geometry import Point
from matplotlib import pyplot as plt

def Alpha_Value_Generator(Phy_domain,Num_of_CutCells,Leaves_list,GP_List):
   
     Mod_GP_List=[]
     for i in range(0,1):
         plt.figure()
         Leaves_Per_Cell=len(Leaves_list[i][1])
         for j in range (0,Leaves_Per_Cell):
             GP_List[i][1][j].insert(1,[])
             for k in range (0,4):
                 x=GP_List[i][1][j][2][k]
                 y=GP_List[i][1][j][3][k]
                 GP=Point(x,y)
                 plt.plot([x],[y], 'go')
               
#                 GP_Two=Point(GP_List[i][1][j][1][1],GP_List[i][1][j][2][1])
#                 GP_Three=Point(GP_List[i][1][j][1][2],GP_List[i][1][j][2][2])
#                 GP_Three=Point(GP_List[i][1][j][1][3],GP_List[i][1][j][2][3])
                 Mod_GP_List=GP_List
                 if Phy_domain.contains(GP) :  #Check for GPs Inside and give alpha=1
                    
                    Mod_GP_List[i][1][j][1].append(1)
                    plt.plot([x],[y], 'o', color = 'black')
                 else:  #Otherwise the GP has to be outiside and alpha=0
                    Mod_GP_List[i][1][j][1].append(0)
                    plt.plot([x],[y], 'ro')
#                    plt.plot(x,y,color='red')

     return Mod_GP_List
    