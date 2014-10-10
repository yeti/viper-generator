#### dependencies
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

#### Globals
Module = namedtuple('Module',['name', 'views']) # Access attributes with dot syntax


#### Functions
def checkValidInput():
	if len(sys.argv) <= 1:
		print "JSON file not provided\n"
		exit(1) 
def printDependencies(modules):
	template = Template(templateStrings.newDependencies)
	print "\n{}\n".format(file.write(template.render(lower__modules=lower_module_names(modules) ,upper_modules=upper_module_names(modules) )))

# returns a list of Module tuples from given JSON
def getModulesFromJson(json):
	modArray = []
	for mod in json:
	  val = Module(name=mod["ModuleName"],views=mod["Views"])
	  modArray.append(val)
	return modArray
#end
def upcase_first_letter(s):
    return s[0].upper() + s[1:]
def lowercase_first_letter(s):
	return s[0].lower() + s[1:]
def uppercase_views(views):
	upper_views = []
	for view in views:
		upper_views.append(upcase_first_letter(view))
	return upper_views
def lower_module_names(modules):
	lower_mods = []
	for mod in modules:
		lower_mods.append(lowercase_first_letter(mod.name))
	return lower_mods
def upper_module_names(modules):
	upper_mods = []
	for mod in modules:
		upper_mods.append(upcase_first_letter(mod.name))
	return upper_mods
# Indicator for how many files were created
def fileCount(modules):
	baseFiles = len(modules) * 4
	appDependencies = 1
	storyboard = 1
	rootVC = 1
	viewCount = 0
	for module in modules:
		viewCount += len(module.views)
	return baseFiles + appDependencies + viewCount + rootVC + storyboard
# capitalize a string, to be used in map
def cap(strVal):
	return strVal.capitalize()

## Get the current working directory OR user provided path
def cwd():
	if len(sys.argv) >= 3:
		if sys.argv[2] == "--existing":
			return os.getcwd()
		else:
			return sys.argv[2] 
	else:
		return os.getcwd()
# get the given module's directory
def moduleDirectory(module):
	return "{}/Modules/{}".format(cwd(),module.name)
def change_permissions_recursive(path, mode):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            os.chmod(dir, mode)
        for file in files:
            os.chmod(file, mode)
#check if this directory exists, if not, create it
def checkDirectory(path):
	try:
		os.mkdir(path)
		change_permissions_recursive(path,777)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			pass
# get JSON from Command Line
def getJSON():
	jsonFilename = sys.argv[1]
	with open(jsonFilename, 'r') as file:		
		try:
			parsedJson = json.loads(file.read())
		except:
			print "Not valid JSON input"
			exit(1)
	return parsedJson
# create all required directories for project
def createDirectories(modules):
	currDir = cwd()
	checkDirectory(currDir)
	checkDirectory("{}/Modules".format(currDir))
	checkDirectory("{}/Common".format(currDir))
	checkDirectory("{}/Common/Models".format(currDir))
	checkDirectory("{}/Common/DataStore".format(currDir))
	for module in modules:
		checkDirectory("{}/Modules/{}".format(currDir,upcase_first_letter(module.name)))
		for view in module.views:
			checkDirectory("{}/Modules/{}/ViewControllers".format(currDir,upcase_first_letter(module.name)))
# create base module file 
def createModuleFile(module,fileName,template):
	directory = moduleDirectory(module)
	fileString = "{}/{}.swift".format(directory,fileName)
	with open(fileString, 'w+') as file:
			template = Template(template)
			file.write(template.render(upper_name=upcase_first_letter(module.name),lower_name=lowercase_first_letter(module.name), upper_views=uppercase_views(module.views))) 
def createGenericFile(directory,fileName,template):
	fileString = "{}/{}".format(directory,fileName)
	with open(fileString, 'w+') as file:
			template = Template(template)
			file.write(template.render())
# Create Presenter for this module
def createPresenter(module):
	createModuleFile(module,"{}Presenter".format(module.name.capitalize()),templateStrings.presenter)
# Create Interactor for this module
def createInteractor(module):
	createModuleFile(module,"{}Interactor".format(module.name.capitalize()),templateStrings.interactor) 
# Create wireframe from this module
def createWireframe(module):
	createModuleFile(module,"{}Wireframe".format(module.name.capitalize()),templateStrings.wireframe)
# Create DataManager from this Module
def createDataManager(module):
	createModuleFile(module,"{}DataManager".format(module.name.capitalize()),templateStrings.datamanager)

# Create ViewController.swift file for each of the module's views.
def createViews(module):
	directory = "{}/ViewControllers".format(moduleDirectory(module))
	for view in module.views:
		fileString = "{}/{}{}ViewController.swift".format(directory, upcase_first_letter(module.name) ,upcase_first_letter(view))
		with open(fileString, 'w+') as file:
			template = Template(templateStrings.viewControllerTemplate)
			file.write(template.render(upper_name=upcase_first_letter(module.name),upper_view=upcase_first_letter(view)))
	# end for
# Create App Dependencies File
def createAppDependencies(modules):
	fileString = "AppDependencies.swift"  
	with open(fileString, 'w+') as file:
			template = Template(templateStrings.dependenciesTemplate)
			file.write(template.render(lower_modules=lower_module_names(modules) ,upper_modules=upper_module_names(modules)))
# Generate the Root Wire frame
def createRootWireframe():
	createGenericFile("{}/Common".format(cwd()),"RootWireFrame.swift",templateStrings.rootWireframe)
# create the storyboard file
def createStoryboard(module):
	createGenericFile(moduleDirectory(module),"{}.storyboard".format(module.name.capitalize()),templateStrings.storyboard)

#### Main ####
def main():
	checkValidInput() # right now just checks number of arguments
	jsonInput = getJSON() # get json from system args -> exits if not valid JSON
	allModules = getModulesFromJson(jsonInput)
	createDirectories(allModules) # all needed directories
	if "--existing" in sys.argv:
		printDependencies(allModules)
	else:
		createAppDependencies(allModules) # dependencies file
		createRootWireframe() # root Wireframe

	### Create All Module Files
	for module in allModules:
		createViews(module)
		createPresenter(module)
		createInteractor(module)
		createWireframe(module)
		createDataManager(module)
		createStoryboard(module)
	# end 
	print("{} Files Created.".format(fileCount(allModules)))

if __name__ == "__main__":
    main()