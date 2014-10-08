# view Generator
import json
from collections import namedtuple
import sys
import os
import os.path
import string
import templateStrings
import errno
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
	cwd = os.getcwd()
	checkDirectory("{}/Modules".format(cwd))
	checkDirectory("{}/Common".format(cwd))
	for module in modules:
		checkDirectory("{}/Modules/{}".format(cwd,module.name))
		for view in module.views:
			checkDirectory("{}/Modules/{}/ViewControllers".format(cwd,module.name))

def createViews(module):
	directory = "{}/ViewControllers".format(moduleDirectory(module))
	for view in module.views:
		fileString = "{}/{}ViewController.swift".format(directory, view.capitalize())
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

# using fake json now, will use file input in the future
mockJSON = json.loads('[{"ModuleName":"Home","Views" : ["Visited","AddVisit"]},{"ModuleName":"Map","Views" : ["MapHome","NewMap"]}]')
# create Named Tuple
Module = namedtuple('Module',['name', 'views'])
allModules = getModulesFromJson(mockJSON)
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
# end 





