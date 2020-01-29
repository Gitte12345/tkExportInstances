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



def cCheckAndMakeDir(path, *args):
	buffer1 = []
	buffer2 = []
	buffer1 = path.split(':')
	newPath = buffer1[0] + ":"
	if len(buffer1) > 0:
		buffer2 = buffer1[1].split('/')
		for dir in range(1, len(buffer2)):
			newPath = newPath + "/" + buffer2[dir]
			if os.path.isdir(newPath) == 0:
				os.mkdir(newPath)


def tkExportInstances(*args):
	del parentsList[:]
	counter = 0
	mainInstGrp = 'inst_LC_grp'
	cmds.select('INSTANCES')
	tk.selectLevel('INSTANCES', 1, 1)
	instances = cmds.ls(sl=1, l=1)
	if not cmds.objExists(mainInstGrp):
		mainInstGrp = cmds.group(em=1, n=mainInstGrp)

	for inst in instances:
		# print inst
		tk.selectLevel(inst, 1, 1)
		curSel = cmds.ls(sl=1, l=1)

		for sel in curSel:
			children 	= cmds.listRelatives(sel, f=1, c=1)
			parents 	= cmds.listRelatives(sel, f=1, ap=1)

			if len(parents) > 1:
				for daddy in parents:
					if daddy not in parentsList:
						# print 'daddy:'
						# print daddy
						parentsList.append(daddy)					


	print 'parentsList:'	
	for par in parentsList:
		print par

	for daddy in parentsList:
		# print 'daddy:'
		# print daddy
		isRef = cmds.referenceQuery(daddy, isNodeReferenced=1)
		if isRef == 1: 
			referencePath = cmds.referenceQuery(daddy, filename=1)

			children 	= cmds.listRelatives(daddy, f=1, c=1)
			parents 	= cmds.listRelatives(daddy, f=1, ap=1)
			for par in parents:
				if ':' in par:
					print 'YES'
					print par
					origRefName = par

			
			if referencePath not in referenceList:
				referenceList.append(referencePath)

		if daddy in instances:
			print counter
			loc = cmds.spaceLocator()
			cmds.addAttr(loc[0], ln='fileReference', dt='string')
			cmds.setAttr(str(loc[0]) + '.fileReference', referencePath, type='string')	
			cmds.addAttr(loc[0], ln='origRefName', dt='string')
			cmds.setAttr(str(loc[0]) + '.origRefName', origRefName.split('|')[-1], type='string')	

			translate = cmds.getAttr(daddy + '.translate')
			rotate = cmds.getAttr(daddy + '.rotate')
			scale = cmds.getAttr(daddy + '.scale')
			cmds.setAttr(loc[0] + '.translate', 
				translate[0][0], translate[0][1], translate[0][2])
			cmds.setAttr(loc[0] + '.rotate', 
				rotate[0][0], rotate[0][1], rotate[0][2])
			cmds.setAttr(loc[0] + '.scale', 
				scale[0][0], scale[0][1], scale[0][2])

			loc = cmds.parent(loc, mainInstGrp)
			counter += 1

	version = tk.getProjectData().pxoVersion
	ws = cmds.workspace(fn=1)
	path = ws + '/_export_instances/' + version + '/'
	exportFilename = path + mainInstGrp + '.ma'

	print exportFilename
	cCheckAndMakeDir(path)
	tk.removeUnknownPlugs()
	cmds.select(mainInstGrp, r=1)
	cmds.file(exportFilename, es=1, force=1, typ='mayaAscii', pr=1)
	# cmds.delete(mainInstGrp)
	print '------------------------------------'
	print 'all instances successfully exported!'
	print '------------------------------------'


def cImportInstanceFromMA(*args):
	# check all references
	del referenceList[:]

	allRefs = cmds.ls(type='reference')
	for ref in allRefs:
		filename = cmds.referenceQuery(ref, filename=1)
		referenceList.append(filename)

	translate = [0, 0, 0]
	rotate = [0, 0, 0]
	scale = [0, 0, 0]

	ws = cmds.workspace(fn=1)
	ws = ws + '/_export_instances/'
	directory = cmds.fileDialog2(dir=ws, fm=3)
	files = os.listdir(directory[0])
	for file in files:
		if file.endswith('LC_grp.ma'):
			absFile = directory[0] + '/' + file
			pureName = file.split('.')[0]

			# if cmds.objExists(pureName + '_grp') == 0:
			# 	mainGrp = cmds.group(empty=1, n=pureName + '_grp')

			cmds.file(absFile, i=1, typ='mayaAscii', 
				iv=1, mergeNamespacesOnClash=0, namespace=pureName)
			
			grp = pureName + ':' + pureName

			tk.selectLevel(grp, 1, 0)
			locs = cmds.ls(sl=1)
			for loc in locs:
				fileReference = cmds.getAttr(loc + '.fileReference')
				print fileReference
				if fileReference not in referenceList and fileReference is not "empty":
					referenceList.append(fileReference)
					cmds.file(fileReference, r=1, iv=1, 
						type="mayaBinary", options="v=0;", mergeNamespacesOnClash=0, namespace=pureName)

				translate 	= cmds.getAttr(loc + '.translate')
				rotate 		= cmds.getAttr(loc + '.rotate')
				scale 		= cmds.getAttr(loc + '.scale')
				geoName 	= cmds.getAttr(loc + '.origRefName')
				print 'origRefName:'
				print origRefName
				match 		= cmds.ls('*:' + origRefName)
				print 'match:'
				print match
				instance 	= cmds.instance(match[0])
				cmds.parent(instance[0], w=1)

				cmds.setAttr(instance[0] + '.translate', 
					translate[0][0], translate[0][1], translate[0][2])
				cmds.setAttr(instance[0] + '.rotate', 
					rotate[0][0], rotate[0][1], rotate[0][2])
				cmds.setAttr(instance[0] + '.scale', 
					scale[0][0], scale[0][1], scale[0][2])

				cmds.parent(instance[0], mainGrp)

			cmds.delete(grp)


def tkInstanceExportImport():
	# global myFileList
	colSilverLight 	= [0.39, 0.46, 0.50];
	colSilverDark 		= [0.08, 0.09, 0.10];
	colSilverMid 		= [0.23, 0.28, 0.30];
	ver = '0.2'
	windowStartHeight = 50
	windowStartWidth = 200
	bh1 = 18
	if (cmds.window('win_tkInstanceExportImport', exists=1)):
		cmds.deleteUI('win_tkInstanceExportImport')
	myWindow = cmds.window('win_tkInstanceExportImport', t=('win_tkInstanceExportImport ' + ver), s=1)
	cmds.columnLayout(adj=1, bgc=(colSilverMid[0], colSilverMid[1], colSilverMid[2]))
	cmds.frameLayout('flMashExport', l='Publish', bgc=(colSilverMid[0], colSilverMid[1], colSilverMid[2]), cll=1, cl=0, cc='cShrinkWin("win_tkInstanceExportImport")')
	# cmds.frameLayout('flMashExport', l='Publish', bgc=(colSilverMid[0], colSilverMid[1], colSilverMid[2]), 
		# cll=1, cl=0, cc=partial(tk.cShrinkWin, 'win_tkInstanceExportImport', 200, 300))

	cmds.button(l='Publish Instances', c=tkExportInstances)
	cmds.button(l='Import Instances', c=cImportInstanceFromMA)

	cmds.showWindow(myWindow)
	cmds.window('win_tkInstanceExportImport', e=1, w=300)

tkInstanceExportImport()
cmds.window('win_tkInstanceExportImport', e=1, w=300)


