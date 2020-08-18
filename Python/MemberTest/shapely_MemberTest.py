# Polygon_Cell_Test with shpaely
"""
Created on Tue Jun 26 17:29:33 2018

@author: JadyWu
"""
#%%

import matplotlib.pyplot as plt
from shapely.geometry import Polygon
#from shapely.geometry import MultiPolygon
#from shapely.geometry import MultiLineString
from shapely.geometry import box

#create Polygon
aPoly = Polygon([(0.25,0.25),(1,0),(0,1)])
bPoly = Polygon([(1,0),(0,1),(1.75,1.75)])

#get Boundary : LineString
boundary_aPoly=aPoly.boundary
boundary_bPoly=bPoly.boundary

#get XY Coordinates of boundary
aP_x,aP_y=aPoly.boundary.xy
bP_x,bP_y=bPoly.boundary.xy
#aP_x,aP_y=aPoly.exterior.xy
#bP_x,bP_y=bPoly.exterior.xy

plt.figure(0)
plt.plot(aP_x,aP_y,bP_x,bP_y)
plt.title("A and B")

#print members: Polygon, LineString, Point 
print("\n")
print("Triangulation is " + aPoly.geom_type + "\n")
print("Boundary is " + boundary_aPoly.geom_type +"\n")


print("Polygon of A: ")
print(aPoly)
print("Polygon of B: ")
print(bPoly)
print("\n")

print("Boundary of A: ")
print(boundary_aPoly)
boundary_aPoly_coords = list (boundary_aPoly.coords)
print("Coordinates")
print(boundary_aPoly_coords)
print("Boundary of B: ")
print(boundary_bPoly)
boundary_bPoly_coords = list (boundary_bPoly.coords)
print("Coordinates")
print(boundary_bPoly_coords)
print("\n")


#%%

#create MultiPolygon
#cPoly = MultiPolygon([aPoly,bPoly])
#bounds_cPoly = cPoly.bounds
#boundary_cPoly = cPoly.boundary

#create Cell
aCell=Polygon([(0.5,0.7),(0.9,0.7),(0.9,1.1),(0.5,1.1)])
bCell=Polygon([(0.5,1.1),(0.9,1.1),(0.9,1.5),(0.5,1.5)])
cCell=Polygon([(0.5,1.5),(0.7,1.5),(0.7,1.7),(0.5,1.7)])

aC_x,aC_y=aCell.boundary.xy
bC_x,bC_y=bCell.boundary.xy
cC_x,cC_y=cCell.boundary.xy

#create Polygon A+B
zPoly = aPoly.union(bPoly)
zP_x,zP_y=zPoly.boundary.xy

b_z=box(zPoly.bounds[0],zPoly.bounds[1],zPoly.bounds[2],zPoly.bounds[3])
boxX,boxY=b_z.boundary.xy

plt.figure(1)
plt.plot(zP_x,zP_y)
plt.title("C = A + B")

plt.figure(2)
plt.plot(zP_x,zP_y,boxX,boxY)
plt.title("C and bounding box")

plt.figure(3)
plt.plot(zP_x,zP_y,aC_x,aC_y,bC_x,bC_y,cC_x,cC_y,boxX,boxY)
plt.title("C and bounding box + Cell")

#%%

#inside-outside test: totally inside
z_a_contain=zPoly.contains(aCell)
z_a_cut = aCell.boundary.crosses(zPoly)
print("Is Orange Cell inside Polygon ?")
print(z_a_contain)
if z_a_contain != True and z_a_cut == True :
    print("It is cut !\n")
elif z_a_contain == True and z_a_cut != True :
    print("It is totally inside !\n")
else:
    print("It is totally outside !\n")

#inside-outside test: partially inside
z_b_contain=zPoly.contains(bCell)
z_b_cut=zPoly.boundary.crosses(bCell)
print("Is Green cell inside Polygon ?")
print(z_b_contain)
if z_b_contain != True and z_b_cut == True :
    print("It is cut !\n")
elif z_b_contain == True and z_b_cut != True :
    print("It is totally inside !\n")
else:
    print("It is totally outside !\n")

#inside-outside test: totally outside    
z_c_contain=zPoly.contains(cCell)
z_c_cut=zPoly.boundary.crosses(cCell)
print("Is Red Cell inside Polygon ?")
print(z_c_contain)
if z_c_contain != True and z_c_cut == True :
    print("It is cut !\n")
elif z_c_contain == True and z_c_cut != True :
    print("It is totally inside !\n")
else:
    print("It is totally outside !\n")

z_box_contain=b_z.contains(zPoly)
z_box_intersect=b_z.intersects(zPoly)
z_box_cross=b_z.crosses(zPoly)
print("Is bounding box contains/intersects/crosses the polygon ?")
print(z_box_contain, z_box_intersect, z_box_cross)