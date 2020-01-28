import maya.cmds as cmds
from functools import partial  

def tkFindInstances(*args):
	instancerList = []
	curSel = cmds.ls(sl=1)
	for sel in curSel:
		children 	= cmds.listRelatives(sel, fp=1, c=1)
		parents 	= cmds.listRelatives(sel, fp=1, ap=1)
		if len(parents) > 1:
			instancerList.append(sel) 

	return instacerList
