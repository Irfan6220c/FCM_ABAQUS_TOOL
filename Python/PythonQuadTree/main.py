#main.py
"""
Created on Tue Jun 26 17:29:33 2018

@author: JadyWu
"""
#%%

from QuadTree import QuadTree
    
print("Implementation of FCM into")
print("start generating the tree")
tree = QuadTree(0.0, 0.0, 4.0, 4.0, None, 0, "0")
tree.generateQuadtree(5)
tree.writeTreeToConsole()
print("generating the tree finished\n")
print( "start writing")
tree.writeTreeToVtk("quadTree.vtk")
print("writing finished\n")	