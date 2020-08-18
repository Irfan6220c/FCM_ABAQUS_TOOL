# STL to Polygon with Shpaely
"""
Created on Tue Jun 26 17:29:33 2018

@author: JadyWu
"""
#%%

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from shapely.geometry import Polygon
#from shapely.geometry import MultiPolygon

# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Load the STL files and add the vectors to the plot
your_mesh = mesh.Mesh.from_file('geometries/potato_with_hole.stl')

axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

# Auto scale to the mesh size
scale = your_mesh.points.flatten(-1)
axes.auto_scale_xyz(scale, scale, scale)

# Show the plot to the screen
pyplot.show()

#%%

size=your_mesh.vectors.size
t=[]
for i in range(0, size//3//3):
    t.append(Polygon(your_mesh.vectors[i]))

#for each in t:
#     print(each,"\n")

a=Polygon()
for i in range(0, size//3//3):
    a=a.union(t[i])
    
#print(a)

#LineStrings
outBoundary=a.boundary[0]
inBoundary=a.boundary[1]

#CoordinateSequence
outBoundaryCoordsSeq=a.boundary[0].coords
outBoundaryCoords = list (a.boundary[0].coords)

inBoundaryCoordsSeq=a.boundary[1].coords
inBoundaryCoords = list (a.boundary[1].coords)

#pyplot.plot(list (a.boundary[0].coords))
