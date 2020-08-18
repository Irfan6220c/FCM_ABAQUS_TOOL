# Polygon_Cell_Test with shpaely
"""
Created on Tue Jun 26 17:29:33 2018

@author: JadyWu
"""
#%%

#from geometry import implicitFunction
from Dummy import Phy_domain
from shapely.geometry import box
from matplotlib import pyplot as plt

class QuadTree():
    
    #counting how many nodes exist in the tree
    myNoOfNodes = 0

    #the convention is
    #myChildren[0] = NW  myChildren[1] = NE
    #myChildren[2] = SW  myChildren[3] = SE
    

    def __init__(self, xmin, ymin, xmax, ymax, father, level, stringCode):
        self.myXmin = xmin
        self.myYmin = ymin
        self.myXmax = xmax
        self.myYmax = ymax
        self.myfather = father
        self.myLevel = level
        self.myStringCode = stringCode
        self.myChildren = None
        self.myCell = box(xmin, ymin, xmax, ymax)
        QuadTree.myNoOfNodes+=1
    	
#    def __del__(self):
#        QuadTree.myNoOfNodes -= 1
        
    def divideMe(self):
        
        self.middleX = 0.5 * (self.myXmax + self.myXmin)
        self.middleY = 0.5 * (self.myYmax + self.myYmin)
        self.myChildren = [QuadTree(self.myXmin, self.middleY, self.middleX, self.myYmax, self, self.myLevel + 1, "0"),
                           QuadTree(self.middleX, self.middleY, self.myXmax, self.myYmax, self, self.myLevel + 1, "0"),
                           QuadTree(self.myXmin, self.myYmin, self.middleX, self.middleY, self, self.myLevel + 1, "0"),
                           QuadTree(self.middleX, self.myYmin, self.myXmax, self.middleY, self, self.myLevel + 1, "0")]
        
#    def amIcut(self, noPoints):
#        isInside = implicitFunction(self.myXmin, self.myYmin)
#        n = (noPoints - 1)
#
#        for i in range(0, noPoints):
#            for j in range(0,noPoints):
#                x = (self.myXmax - self.myXmin) * i / n + self.myXmin
#                y = (self.myYmax - self.myYmin) * j / n + self.myYmin
#                if (implicitFunction(x,y) != isInside): 
#                    return True;
#            
#        return False;
    
    def amIcut(self):
       
        # 0 = totally inside
        # 1 = totally outside
        # 2 = cut
       
        
        if Phy_domain.contains(self.myCell):
            #print('Cell countains geometry')
            self.myStringCode = '0'
            return False
        
        elif self.myCell.intersects(Phy_domain):
            #print('Out Boundary is cut')
            self.myStringCode = '2'
            return True
        
        else:
            #print('It is totally outside')
            self.myStringCode = '1'
            return False

    def generateQuadtree(self, maxLevel):
        numberOfPoints = 5;
        
        if (self.myLevel < maxLevel and self.amIcut(self)):
            self.divideMe()
           
            for children in self.myChildren:
                children.generateQuadtree(maxLevel)


    def writeTreeToConsole(self):
        print('Node at level', self.myLevel, ': [', self.myXmin, ', ', self.myXmax, '] x [', self.myYmin, ', ', self.myYmax, ']\n')
        if (self.myChildren != None):
            i=0
            for children in self.myChildren:
                indentation = (2 * (self.myLevel + 1)) * ('  ')
                print(indentation + "Sub node " + str(i) + ': ')
                i+=1
                children.writeTreeToConsole()
    
    def plotTreeToConsole(self):
        x,y = self.myCell.exterior.xy
        plt.plot(x,y, color='black')
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
        