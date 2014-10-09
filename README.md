iOS Dependency Generator (swift)
========================

Script to generate models  and dependencies for Yeti's take on [VIPER](http://www.objc.io/issue-13/viper.html) architecture


## Installation
Clone this project into a working directory.
`git clone https://github.com/yeti/ios-dependency-generator.git`

## Dependencies
The script requires the [Jinja2](http://jinja.pocoo.org/docs/dev/intro/) templating engine to create files. Jinja2 can be installed through either `easy_install` or `pip`
```
easy_install Jinja2
pip install Jinja2
```

## Basic Usage
Run the following command
```
sudo python dependency_generator.py ./file.json /path/to/desired/directory
```
where:
1. ./file.json is the path to a json file with attributes outline below
2. /path/to/desired/directory is the directory in which the generated files will be saved

### JSON File
The JSON file should outline the modules to be created in the script. For each module, you must supply a module name and the list of views in that module. The JSON file should 
consist of a list of dictionaries. Each dictionary contains a "ModuleName" and an Array of Views. For example:
```
[
{"ModuleName" : "Home", "Views" : ["List","Friends"]},
{"ModuleName" : "Map", "Views" : ["Visited"]}
]

```
## Output
For each module, the script will output:
- 1 Presenter
- 1 Interactor
- 1 Wireframe
- 1 Datamanger
- 1 Storyboard
- X View controllers
Where X is the number of views associated with that module.
The script will also generate an AppDependencies file that binds these files to each other.
Along with this, the script will create a RootWireFrame in the 'Common' directory.
When these files are created, simply drag and drop them into your current Xcode project.


