#main.py
"""
Created on Tue Jun 26 17:29:33 2018

@author: JadyWu
"""
#%%

from matplotlib import pyplot as plt
from QuadTreeShapely import QuadTree
import shapely_STL2Polygon as myPolygonSTL

print("Implementation of QuadTree with Shapely")

#%% Generating Tree

print("start generating the tree")
tree = QuadTree(myPolygonSTL.BoundingBox[0], myPolygonSTL.BoundingBox[1], myPolygonSTL.BoundingBox[2], myPolygonSTL.BoundingBox[3], None, 0, "0")
maxLevel = 2
tree.generateQuadtree(maxLevel)
print("generating the tree finished\n")

#%% Print Boundary
figBoundary = plt.figure()
outX,outY = myPolygonSTL.myPolygon.boundary[0].xy
inX,inY = myPolygonSTL.myPolygon.boundary[1].xy
plt.plot(outX,outY,color='red')
plt.plot(inX,inY,color='red')
plt.ylim((myPolygonSTL.BoundingBox[1] - 3),(myPolygonSTL.BoundingBox[3] + 3))
plt.xlim((myPolygonSTL.BoundingBox[0] - 3),(myPolygonSTL.BoundingBox[2] + 3))

#%% Print Geometry Tree
figTree = plt.figure()
plt.plot(outX,outY,color='red')
plt.plot(inX,inY,color='red')
plt.ylim((myPolygonSTL.BoundingBox[1] - 3),(myPolygonSTL.BoundingBox[3] + 3))
plt.xlim((myPolygonSTL.BoundingBox[0] - 3),(myPolygonSTL.BoundingBox[2] + 3))
tree.plotElementToConsole(maxLevel)

figAllTree = plt.figure()
plt.ylim((myPolygonSTL.BoundingBox[1] - 3),(myPolygonSTL.BoundingBox[3] + 3))
plt.xlim((myPolygonSTL.BoundingBox[0] - 3),(myPolygonSTL.BoundingBox[2] + 3))
tree.plotTreeToConsole()

#%% Writing Tree

#print( "start writing to console")
#tree.writeTreeToConsole()

#print( "start writing to .vtk")
#tree.writeTreeToVtk("quadTree.vtk")
#print("writing finished\n")	
