import maya.cmds as cmds
from functools import partial  
import thomas as tk

global INSTANCERLIST
INSTANCERLIST = []

def tkFindInstances(*args):
	cmds.select('INSTANCES')
	tk.selectLevel('INSTANCES', 2, 0)
	curSel = cmds.ls(sl=1, l=1)

	# print curSel

	for sel in curSel:
		children 	= cmds.listRelatives(sel, f=1, c=1)
		parents 	= cmds.listRelatives(sel, f=1, ap=1)

		if len(parents) > 1:
			for daddy in parents:
				if daddy not in INSTANCERLIST:
					INSTANCERLIST.append(daddy)

	# return INSTANCERLIST
	print 'INSTANCERLIST:'
	for inst in INSTANCERLIST:
		print inst

tkFindInstances()