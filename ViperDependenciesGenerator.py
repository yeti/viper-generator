# view Generator
import json
from collections import namedtuple
import sys
import os
import os.path
import string
import templateStrings
import errno
from sys import stdin
from jinja2 import Template
# methods

# returns a list of Module tuples from given JSON
def getModulesFromJson(json):
	modArray = []
	for mod in json:
	  val = Module(name=mod["ModuleName"],views=mod["Views"])
	  modArray.append(val)
	return modArray
#end
# capitalize a string, to be used in map
def cap(strVal):
	return strVal.capitalize()

def cwd():
	if len(sys.argv) >= 3:
		return sys.argv[2]
	else:
		return os.getcwd()

def moduleDirectory(module):
	return "{}/Modules/{}".format(cwd(),module.name)

def checkDirectory(path):
	try:
		os.mkdir(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			pass

def createDirectories(modules):
	currDir = cwd()
	checkDirectory("{}/Modules".format(currDir))
	checkDirectory("{}/Common".format(currDir))
	checkDirectory("{}/Common/Models".format(currDir))
	checkDirectory("{}/Common/DataStore".format(currDir))
	for module in modules:
		checkDirectory("{}/Modules/{}".format(currDir,module.name))
		for view in module.views:
			checkDirectory("{}/Modules/{}/ViewControllers".format(currDir,module.name))

def createViews(module):
	directory = "{}/ViewControllers".format(moduleDirectory(module))
	for view in module.views:
		fileString = "{}/{}{}ViewController.swift".format(directory, module.name.capitalize() ,view.capitalize())
		with open(fileString, 'w+') as file:
			template = Template(templateStrings.viewControllerTemplate)
			file.write(template.render(name=module.name,view=view))
	# end for
def createPresenter(module):
	directory = moduleDirectory(module)
	fileString = "{}/{}Presenter.swift".format(directory,module.name.capitalize())
	with open(fileString, 'w+') as file:
			template = Template(templateStrings.presenterTemplate)
			file.write(template.render(name=module.name,viewList=module.views)) 
# end create presenter

def createInteractor(module):
	directory = moduleDirectory(module)
	fileString = "{}/{}Interactor.swift".format(directory,module.name.capitalize())
	with open(fileString, 'w+') as file:
			template = Template(templateStrings.interactorTemplate)
			file.write(template.render(name=module.name,viewList=module.views)) 
def createWireframe(module):
	directory = moduleDirectory(module)
	fileString = "{}/{}Wireframe.swift".format(directory,module.name.capitalize())
	with open(fileString, 'w+') as file:
			template = Template(templateStrings.wireframeTemplate)
			file.write(template.render(name=module.name,viewList=module.views))
def createDataManager(module):
	directory = moduleDirectory(module)
	fileString = "{}/{}DataManager.swift".format(directory,module.name.capitalize())
	with open(fileString, 'w+') as file:
			template = Template(templateStrings.datamanagerTemplate)
			file.write(template.render(name=module.name,viewList=module.views))


def createAppDependencies(modules):
	fileString = "AppDependencies.swift"  
	with open(fileString, 'w+') as file:
			template = Template(templateStrings.dependenciesTemplate)
			file.write(template.render(modules=modules))
def createRootWireframe():
	fileString = "{}/Common/RootWireFrame.swift".format(cwd())  
	with open(fileString, 'w+') as file:
			template = Template(templateStrings.rootWireframe)
			file.write(template.render())
def createStoryboard(module):
	directory = moduleDirectory(module)
	fileString = "{}/{}.storyboard".format(directory,module.name.capitalize())
	with open(fileString, 'w+') as file:
			template = Template(templateStrings.storyboard)
			file.write(template.render(name=module.name,viewList=module.views))
def getJSON():
	jsonFilename = sys.argv[1]
	with open(jsonFilename, 'r') as file:		
		parsedJson = json.loads(file.read())
	return parsedJson


# start script


jsonInput = getJSON()
# create Named Tuple
Module = namedtuple('Module',['name', 'views'])
allModules = getModulesFromJson(jsonInput)
createDirectories(allModules)
createAppDependencies(allModules)
createRootWireframe()

### Create Modules
for module in allModules:
	createViews(module)
	createPresenter(module)
	createInteractor(module)
	createWireframe(module)
	createDataManager(module)
	createStoryboard(module)
# end 





