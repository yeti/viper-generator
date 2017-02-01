Mobile Dependency Generator (Swift and Java)
============================================

Script to generate models  and dependencies for Yeti's take on [VIPER](http://www.objc.io/issue-13/viper.html) architecture. For an example of how this architecture can be used. Take a look at the [demo project](https://github.com/yeti/searching-for-yeti-viper-demo).


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
python dependency_generator.py ./file.json /path/to/desired/directory --existing
```
where:

1. /file.json is the path to a json file with attributes outline below
2. /path/to/desired/directory is the directory in which the generated files will be saved (Optional)
    - Tip: For Android, the desired directory will be `path/to/project_name/app/src/main/java/com/project_identifier/`
3.  The '--existing' flag is added when adding a new module to an existing project

### JSON File
The JSON file should outline the modules to be created in the script. For each module, you must supply a module name and the list of views in that module. The JSON file should 
consist of a list of dictionaries. Each dictionary contains a "ModuleName" and an Array of Views. 
The first dictionary in the array should contain project information - the platform that you are generating code for (`ios` or `android`) and the Project Name.
For example:
```
[
    {
        "Platform": "android",
        "Project": "Example Project"
    }
    {
        "ModuleName": "Home", 
        "Views": ["List", "Friends"]
    },
    {   
        "ModuleName": "Map", 
        "Views" : ["Visited"]
    }
]

```
## Output
For each ios module, the script will output:
- 1 Presenter
- 1 Interactor
- 1 Wireframe
- 1 Storyboard
- X View controllers

Where 'X' is the number of views associated with that module.
The script will also generate an AppDependencies file that binds these files to each other.
Along with this, the script will create a RootWireFrame in the 'Common' directory.
When these files are created, simply drag and drop them into your current Xcode project.

For each java module, the script will output:
- 1 Module
- 1 Component
- 1 Interactor
- 1 Presenter
- 1 Activity
- X Fragments
- 1 Activity .xml and X Fragment .xml (inside a `layouts` directory)

At this time, no extra dependency files are created, and the script assumes that an existing project already exists, so no "base" files are created.


## Adding to an Existing Project
Sometimes you may want to add more modules to an existing script after already running the generator.
In these scenarios, simply create a fresh JSON file for the new module(s) and run the script with the `--existing' flag. This will create the new Models which can be dragged into your Xcode project. It will also print dependency code which can be copy and pasting into an existing AppDependencies file.


