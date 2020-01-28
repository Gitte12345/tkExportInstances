import maya.cmds as cmds
from functools import partial  
import thomas as tk

global instancerList
global referenceList
global referencePath
instancerList = []
referenceList = []

def tkFindInstances(*args):
	cmds.select('INSTANCES')
	tk.selectLevel('INSTANCES', 2, 0)
	curSel = cmds.ls(sl=1, l=1)

	mainLocGrp = cmds.group(em=1, n='mainLocGrp')

	for sel in curSel:
		children 	= cmds.listRelatives(sel, f=1, c=1)
		parents 	= cmds.listRelatives(sel, f=1, ap=1)

		if len(parents) > 1:
			for daddy in parents:
				isRef = cmds.referenceQuery(daddy, isNodeReferenced=1)
				if isRef == 1: 
					referencePath = cmds.referenceQuery(daddy, filename=1)
					if referencePath not in referenceList:
						referenceList.append(referencePath)
				
			for daddy in parents:
				loc = cmds.spaceLocator()
				cmds.addAttr(loc[0], ln='path', dt='string')
				# cmds.addAttr(loc + '.path', e=1)

				cmds.setAttr(str(loc[0]) + '.path', referencePath, type='string')
				cmds.parent(loc, mainLocGrp)













tkFindInstances()