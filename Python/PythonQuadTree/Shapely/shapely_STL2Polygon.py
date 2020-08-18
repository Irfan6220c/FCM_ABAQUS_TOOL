# STL to Polygon with Shpaely
"""
Created on Tue Jun 26 17:29:33 2018

@author: JadyWu
"""
#%%

from stl import mesh
from matplotlib import pyplot as plt
from matplotlib import patches
from shapely.geometry import Polygon

stl_filename = 'Plate_with_potato.stl'
#stl_filename = 'geometries/Plate_with_potato.stl'

# Create a new plot
fig = plt.figure()
ax1 = fig.add_subplot(111,aspect='equal')

#Creating object by reading the stl file    
My_geometry = mesh.Mesh.from_file(stl_filename)
Triangle_data = My_geometry.vectors
No_Triangles = len (My_geometry.vectors)

#Getting co-ordinates of minimum and maximum points to compute the bounding box
Max_cord = My_geometry.max_
Min_cord = My_geometry.min_

Xmin = Min_cord[0]
Ymin=  Min_cord[1]
Xmax = Max_cord[0]
Ymax = Max_cord[1]
      
#Parameters for the Rectangular patch
left_corner = (Xmin,Ymin)
length = Xmax - Xmin
height = Ymax-Ymin
plt.ylim((Ymin - 3),(Ymax + 3))
plt.xlim((Xmin - 3),(Xmax + 3))

#%% Bounding Box
##Creating the Bounding box
#
#Bounding_box = patches.Rectangle(left_corner,length,height,fill = False,linestyle = 'dashed',linewidth = 2.0,color = 'r')
#ax1.add_patch(Bounding_box)

#%% Plot Triangles

    #Looping over all the elements and plotting them within the bounding box
for i in range (0,No_Triangles):
    V1 = Triangle_data[i][0]
    V2 = Triangle_data[i][1]
    V3 = Triangle_data[i][2]
    V1_xy = [V1[0],V1[1]]
    V2_xy = [V2[0],V2[1]]
    V3_xy = [V3[0],V3[1]]
    points = [V1_xy,V2_xy,V3_xy]  
    i_th_triangle = patches.Polygon(points)
    ax1.add_patch(i_th_triangle)

#%% 3D
#
#from mpl_toolkits import mplot3d
#
## Create a new plot
#figure3D = plt.figure()
#axes = mplot3d.Axes3D(figure3D)
#
## Load the STL files and add the vectors to the plot
#axes.add_collection3d(mplot3d.art3d.Poly3DCollection(My_geometry.vectors))
#
## Auto scale to the mesh size
#scale = My_geometry.points.flatten(-1)
#axes.auto_scale_xyz(scale, scale, scale)

#%%

size = My_geometry.vectors.size
t = []
for i in range(0, size//3//3):
    t.append(Polygon(My_geometry.vectors[i]))

#for each in t:
#     print(each,"\n")

myPolygon = Polygon()
for i in range(0, size//3//3):
    myPolygon = myPolygon.union(t[i])
#print(myPolygon)

#LineStrings
outBoundary = myPolygon.boundary[0]
inBoundary = myPolygon.boundary[1]

#CoordinateSequence
outBoundaryCoordsSeq = myPolygon.boundary[0].coords
outBoundaryCoords = list (myPolygon.boundary[0].coords)

inBoundaryCoordsSeq = myPolygon.boundary[1].coords
inBoundaryCoords = list (myPolygon.boundary[1].coords)

#BoundingBox
BoundingBox = myPolygon.bounds
