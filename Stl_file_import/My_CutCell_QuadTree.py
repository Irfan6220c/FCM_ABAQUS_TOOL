# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:02:24 2018

@author: Boulbrachene
"""

#%%

from shapely.geometry import box
from matplotlib import pyplot as plt
import numpy as num

Leaves=[]
temp=[]
Label = []

#def writeLabelToFile(lbl):
#    foo = open('Label_list.txt','a')
#    num.savetxt(foo,lbl)

class QuadTree():
    
    #Nodes and Leaves Counter
    myNoOfNodes = 0
    myNoOfLeaves = 0
    Integ_Input= []
    #Convention is
    #myChildren[0] = NW  myChildren[1] = NE
    #myChildren[2] = SW  myChildren[3] = SE
    
    def Integration_Input(self):
        
        if self.myfather != None:
            for i in range (0,len(self.myfather.label)):
                self.label.append(self.myfather.label[i])
            self.label.append(self.ID)
            #print (self.label)
            #Integ_Input.append(self.label)
      

    def __init__(self,CutCellNum,Phy_domain, xmin, ymin, xmax, ymax, father, level, stringCode,ID):
        self.ElementNum=CutCellNum
        self.Domain=Phy_domain
        self.myXmin = xmin
        self.myYmin = ymin
        self.myXmax = xmax
        self.myYmax = ymax
        self.myfather = father
        self.myLevel = level
        self.myStringCode = stringCode
        self.myChildren = None
        self.myCell = box(xmin, ymin, xmax, ymax)
        self.ID = ID
        self.label = []
        QuadTree.myNoOfNodes+=1
    	
        
    def divideMe(self):
        
        self.middleX = 0.5 * (self.myXmax + self.myXmin)
        self.middleY = 0.5 * (self.myYmax + self.myYmin)
        self.myChildren = [QuadTree(self.ElementNum, self.Domain,self.myXmin, self.myYmin, self.middleX, self.middleY, self, self.myLevel + 1, "0",1),
                           QuadTree(self.ElementNum, self.Domain,self.middleX, self.myYmin, self.myXmax, self.middleY, self, self.myLevel + 1, "0",2),
                           QuadTree(self.ElementNum, self.Domain,self.middleX, self.middleY, self.myXmax, self.myYmax, self, self.myLevel + 1, "0",3),
                           QuadTree(self.ElementNum, self.Domain,self.myXmin, self.middleY, self.middleX, self.myYmax, self, self.myLevel + 1, "0",4)]               
        
        for i in range (0,4):
            self.myChildren[i].Integration_Input()
    
    def amIcut(self):
        # 0 = totally outside
        # 1 = totally inside
        # 2 = cut 
                
        if self.Domain.contains(self.myCell):
            #print('Cell countains geometry')
            self.myStringCode = '1'
            
            return False
        
        elif self.myCell.intersects(self.Domain):
            #print('Out Boundary is cut')
            self.myStringCode = '2'
            return True
        
        else:
            #print('It is totally outside')
            self.myStringCode = '0'
            return False


    def generateQuadtree(self, maxLevel):
        
        if (self.myLevel < maxLevel and self.amIcut()):
            self.divideMe()
            for children in self.myChildren:
                children.generateQuadtree(maxLevel)
#                if children.myStringCode !='2':
#                    print (children.label)
#                    temp_lbl = children.label
#                    writeLabelToFile(temp_lbl)
        
        
#        foo = open('Label_list.txt','w')
#        num.savetxt(foo,Integ_Input)           #print (Integ_Input)
                 
    def writeTreeToConsole(self):
        print('Node at level', self.myLevel, ': [', self.myXmin, ', ', self.myXmax, '] x [', self.myYmin, ', ', self.myYmax, ']\n')
        if (self.myChildren != None):
            i=0
            for children in self.myChildren:
                indentation = (2 * (self.myLevel + 1)) * ('  ')
                print(indentation + "Sub node " + str(i) + ': ')
                i+=1
                children.writeTreeToConsole()
                
    def Get_myNoOfLeaves(self):
        if (self.myChildren!= None):
                for children in self.myChildren:
                    children.Return_Leaves_list()
        else:
            QuadTree.myNoOfLeaves+=1
        return QuadTree.myNoOfLeaves
    
    def writeLeavesToConsole(self):    
        
            if (self.myChildren!= None):
                for children in self.myChildren:
                    children.writeLeavesToConsole()
            else:
                QuadTree.myNoOfLeaves+=1
                print("this leaf number ",QuadTree.myNoOfLeaves," belongs to Cut Element number", self.ElementNum)
                print("the bounds are (", self.myXmin ,",", self.myYmin, ") and (", self.myXmax, ",", self.myYmax,")" )
                print("Total number of Leaves of Element Number ", self.ElementNum, "are ", QuadTree.myNoOfLeaves )
                
        
    def Return_Leaves_list(self):
        
        if(self.myfather==None):
                del Leaves[:]
                
        if (self.myChildren!= None):
            for children in self.myChildren:
                children.Return_Leaves_list()
        else:
            QuadTree.myNoOfLeaves+=1
            temp=[(self.myXmin,self.myYmin),(self.myXmax,self.myYmax)]
            if temp not in Leaves:
            #temp = self.label
                Leaves.append(temp)
                            
        return Leaves 
        
    def Return_Label_list(self, Label):
     
        if(self.myfather==None):
                del Label[:]
        
        if (self.myChildren != None):
             for children in self.myChildren:
                 children.Return_Label_list(Label)
                 if children.myStringCode !='2':
                     temp = children.label
                     Label.append(temp)
        #return Label   
        
        
    def plotTreeToConsole(self):
        x,y = self.myCell.exterior.xy
        plt.plot(x,y, color='blue')
        if (self.myChildren != None):
            for children in self.myChildren:
                children.plotTreeToConsole()
                
    def plotElementToConsole(self, maxLevel):

        if (self.myChildren != None):
            for children in self.myChildren:
                children.plotElementToConsole(maxLevel)        

        # Totally outside
        if (self.myStringCode =='4' ):
            x,y = self.myCell.exterior.xy
            plt.plot(x,y, color='red')

        # Total inside
        if (self.myChildren == None and self.myStringCode == '3'):
            x,y = self.myCell.exterior.xy
            plt.plot(x,y, color='blue')

        # Cut
        elif (self.myLevel == maxLevel-1 and self.myStringCode == '2'):
            x,y = self.myCell.exterior.xy
            plt.plot(x,y, color='green')        
        
	
    
#%%   
    #output functions
    def writePointsToVtk(self,fileName):
        
        with open(fileName, 'a') as the_file:
                
            the_file.write(str(self.myXmin)+ "\t"+ str(self.myYmin)+ "\t"+ "0"+ "\n")
            the_file.write(str(self.myXmax)+ "\t"+ str(self.myYmin)+ "\t"+ "0"+ "\n")
            the_file.write(str(self.myXmax)+ "\t"+ str(self.myYmax)+ "\t"+ "0"+ "\n")
            the_file.write(str(self.myXmin)+ "\t"+ str(self.myYmax)+ "\t"+ "0"+ "\n")
        
        if (self.myChildren != None):
            for children in self.myChildren: 
                children.writePointsToVtk(fileName)

    def writeNodeCodesToVtk(self, fileName):
        
        with open(fileName, 'a') as the_file:
            the_file.write(str(self.myStringCode)+"\n")
            if (self.myChildren != None):
                for children in self.myChildren:
                    children.writeNodeCodesToVtk(fileName)

    def writeTreeToVtk(self, fileName):

        with open(fileName, 'w') as the_file:
            the_file.write("")
                           
        with open(fileName, 'a') as the_file:
            the_file.write("# vtk DataFile Version 4.2\n")
            the_file.write("Test Data\n")
            the_file.write("ASCII\n")
            the_file.write("DATASET UNSTRUCTURED_GRID\n")
            the_file.write("POINTS "+ str(4 * QuadTree.myNoOfNodes)+ " "+ "double \n")            
            
        self.writePointsToVtk(fileName);
    
        with open(fileName, 'a') as the_file: 
            
            #output the cells
            the_file.write("CELLS "+ str(QuadTree.myNoOfNodes)+ " "+ str(5 * QuadTree.myNoOfNodes)+"\n")
            for i in range(0, QuadTree.myNoOfNodes * 4, 4):
                the_file.write("4\t"+ str(i)+ "\t"+ str((i + 1))+ "\t"+ str((i + 2))+ "\t"+ str((i + 3))+ "\n")
        
            #output cell types
            the_file.write("CELL_TYPES "+ str(QuadTree.myNoOfNodes)+ "\n")
            for i in range(0,QuadTree.myNoOfNodes):
                the_file.write("9\n")
            #the_file.write("CELL_DATA "+ str(QuadTree.myNoOfNodes)+ "\n")
            #the_file.write("SCALARS Node_Number double\n")
            #the_file.write("LOOKUP_TABLE default\n")
        #self.writeNodeCodesToVtk(fileName)

