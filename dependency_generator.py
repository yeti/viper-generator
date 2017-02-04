import json
from collections import namedtuple
import sys
import ios_templates
from jinja2 import Template

# Globals
from android_generator_methods import create_android_presenter, create_android_module, create_android_component, \
    create_android_activity, create_android_interactor, create_android_fragments
from ios_generator_methods import create_app_dependencies, create_root_wireframe, \
    create_view_controllers, create_ios_presenter, create_ios_interactor, create_wireframe, create_storyboard
from shared_generator_methods import lower_module_names, upper_module_names, create_directories

Project = namedtuple('Project', ['platform', 'name'])
Module = namedtuple('Module', ['name', 'views'])  # Access attributes with dot syntax

# Platform Constants
IOS = "ios"
ANDROID = "android"


# Functions
def check_valid_input():
    if len(sys.argv) <= 1:
        print("JSON file not provided\n")
        exit(1)


def print_dependencies(modules):
    template = Template(ios_templates.new_dependencies)
    print("\n{}\n".format(file.write(
        template.render(lower__modules=lower_module_names(modules), upper_modules=upper_module_names(modules)))))


# Get Project info from given JSON
def get_project_from_json(json_input):
    project_info = json_input[0]
    project = Project(platform=project_info["Platform"], name=project_info["Project"])
    return project


# returns a list of Module tuples from given JSON
def get_modules_from_json(json_input):
    mod_array = []
    json_input.pop(0)  # Remove generator type from start of list
    for mod in json_input:
        val = Module(name=mod["ModuleName"], views=mod["Views"])
        mod_array.append(val)
    return mod_array


# Indicator for how many files were created
def file_count(platform, modules):
    if platform == IOS:
        base_files = len(modules) * 3
        app_dependencies = 1
        storyboard = 1
        root_view_controller = 1
        view_count = 0
        for module in modules:
            view_count += len(module.views)
        return base_files + app_dependencies + view_count + root_view_controller + storyboard
    else:
        # Module, Component, Interactor, Presenter, Axtivity, Activity .xml, Manifest .xml
        base_files = len(modules) * 7
        view_count = 0
        for module in modules:
            # Fragment, Fragment .xml
            view_count += len(module.views) * 2
        return base_files + view_count


# get JSON from Command Line
def get_json():
    json_filename = sys.argv[1]
    with open(json_filename, 'r') as json_file:
        parsed_json = json.loads(json_file.read())
    return parsed_json


def main():
    check_valid_input()  # right now just checks number of arguments
    json_input = get_json()  # get json from system args -> exits if not valid JSON
    project = get_project_from_json(json_input)  # Get project info
    all_modules = get_modules_from_json(json_input)

    create_directories(project.platform, all_modules)

    if project.platform == ANDROID:
        if "--existing" in sys.argv:
            # TODO: Currently no difference between new and existing projects
            pass

        # Create All Module Files
        for module in all_modules:
            create_android_module(project.name, module)
            create_android_component(project.name, module)
            create_android_activity(project.name, module)
            create_android_presenter(project.name, module)
            create_android_interactor(project.name, module)
            create_android_fragments(project.name, module)
    elif project.platform == IOS:
        if "--existing" in sys.argv:
            print_dependencies(all_modules)
        else:
            create_app_dependencies(all_modules)  # dependencies file
            create_root_wireframe()  # root Wireframe

        # Create All Module Files
        for module in all_modules:
            create_view_controllers(module)
            create_ios_presenter(module)
            create_ios_interactor(module)
            create_wireframe(module)
            create_storyboard(module)
        # end
    else:
        print("Invalid Generator type\n")
        exit(1)

    print("{} Files Created.".format(file_count(project.platform, all_modules)))

if __name__ == "__main__":
    main()
