# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
cliCommand(
    """session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry=COORDINATE)""")
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-28.75, 21.25), point2=(2.5, -12.5))
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=TWO_D_PLANAR, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']
p.BaseShell(sketch=s)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
p = mdb.models['Model-1'].parts['Part-1']
p.seedPart(size=3.4, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['Part-1']
p.generateMesh()
mdb.meshEditOptions.setValues(enableUndo=True, maxUndoCacheElements=0.5)
p = mdb.models['Model-1'].parts['Part-1']
p.PartFromMesh(name='orphan mesh', copySets=True)
p1 = mdb.models['Model-1'].parts['orphan mesh']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
p = mdb.models['Model-1'].parts['orphan mesh']
e = p.elements
elements = e[32:35]+e[41:44]
p.Set(elements=elements, name='Set-1_alpha_0')
p = mdb.models['Model-1'].parts['orphan mesh']
e = p.elements
elements = e[0:32]+e[35:41]+e[44:90]
p.Set(elements=elements, name='Set-2_alpha_1')
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON, mesh=OFF)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=OFF)
mdb.models['Model-1'].Material(name='Material-1_alpha_0')
mdb.models['Model-1'].materials['Material-1_alpha_0'].Elastic(table=((0.2, 
    0.3), ))
mdb.models['Model-1'].Material(name='Material-2_alpha_1')
mdb.models['Model-1'].materials['Material-2_alpha_1'].Elastic(table=((
    200000000.0, 0.3), ))
mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1_alpha_0', 
    material='Material-1_alpha_0', thickness=0.1)
mdb.models['Model-1'].HomogeneousSolidSection(name='Section-2_alpha_1', 
    material='Material-2_alpha_1', thickness=0.1)
p = mdb.models['Model-1'].parts['orphan mesh']
region = p.sets['Set-1_alpha_0']
p = mdb.models['Model-1'].parts['orphan mesh']
p.SectionAssignment(region=region, sectionName='Section-1_alpha_0', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
p = mdb.models['Model-1'].parts['orphan mesh']
region = p.sets['Set-2_alpha_1']
p = mdb.models['Model-1'].parts['orphan mesh']
p.SectionAssignment(region=region, sectionName='Section-2_alpha_1', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)


