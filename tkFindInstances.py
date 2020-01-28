import maya.cmds as cmds
from functools import partial  
import thomas as tk

global instancerList
global referenceList
global parentsList
global referencePath
instancerList = []
referenceList = []
parentsList = []

def tkFindInstances(*args):
	counter = 0
	cmds.select('INSTANCES')
	tk.selectLevel('INSTANCES', 1, 1)
	instances = cmds.ls(sl=1, l=1)
	mainLocGrp = cmds.group(em=1, n='mainLocGrp')

	for inst in instances:
		# print inst
		tk.selectLevel(inst, 1, 1)
		curSel = cmds.ls(sl=1, l=1)

		for sel in curSel:
			# children 	= cmds.listRelatives(sel, f=1, c=1)
			parents 	= cmds.listRelatives(sel, f=1, ap=1)

			if len(parents) > 1:
				for daddy in parents:
					if daddy not in parentsList:
						print 'daddy:'
						print daddy
						parentsList.append(daddy)

		
	for daddy in parentsList:
		isRef = cmds.referenceQuery(daddy, isNodeReferenced=1)
		if isRef == 1: 
			referencePath = cmds.referenceQuery(daddy, filename=1)
			if referencePath not in referenceList:
				referenceList.append(referencePath)

		if daddy in instances:
			print counter
			loc = cmds.spaceLocator()
			cmds.addAttr(loc[0], ln='path', dt='string')
			cmds.setAttr(str(loc[0]) + '.path', referencePath, type='string')	
			cmds.addAttr(loc[0], ln='name', dt='string')
			cmds.setAttr(str(loc[0]) + '.name', daddy, type='string')	

			translate = cmds.getAttr(daddy + '.translate')
			rotate = cmds.getAttr(daddy + '.rotate')
			scale = cmds.getAttr(daddy + '.scale')
			cmds.setAttr(loc[0] + '.translate', translate[0][0], translate[0][1], translate[0][2])
			cmds.setAttr(loc[0] + '.rotate', rotate[0][0], rotate[0][1], rotate[0][2])
			cmds.setAttr(loc[0] + '.scale', scale[0][0], scale[0][1], scale[0][2])

			loc = cmds.parent(loc, mainLocGrp)
			counter += 1

			# add filename and version to grp

			# export grp to publish folder 




tkFindInstances()