import json
from collections import namedtuple
import sys
import ios_templates
from jinja2 import Template

# Globals
from android_generator_methods import create_android_presenter, create_android_module, create_android_component, \
    create_android_activity, create_android_interactor, create_android_fragments, create_android_directories
from ios_generator_methods import create_ios_directories, create_app_dependencies, create_root_wireframe, \
    create_view_controllers, create_ios_presenter, create_ios_interactor, create_wireframe, create_storyboard
from shared_generator_methods import lower_module_names, upper_module_names

Project = namedtuple('Project', ['platform', 'name'])
Module = namedtuple('Module', ['name', 'views'])  # Access attributes with dot syntax


# Functions
def check_valid_input():
    if len(sys.argv) <= 1:
        print "JSON file not provided\n"
        exit(1)


def print_dependencies(modules):
    template = Template(ios_templates.new_dependencies)
    print "\n{}\n".format(file.write(
        template.render(lower__modules=lower_module_names(modules), upper_modules=upper_module_names(modules))))


# Get Project info from given JSON
def get_project_from_json(json):
    project = Project(platform=json[0]["Platform"], name=json[0]["Project"])
    return project


# returns a list of Module tuples from given JSON
def get_modules_from_json(json):
    mod_array = []
    json.pop(0)  # Remove generator type from start of list
    for mod in json:
        val = Module(name=mod["ModuleName"], views=mod["Views"])
        mod_array.append(val)
    return mod_array


# Indicator for how many files were created
def file_count(modules):
    # TODO: Only works for ios
    base_files = len(modules) * 3
    app_dependencies = 1
    storyboard = 1
    root_view_controller = 1
    view_count = 0
    for module in modules:
        view_count += len(module.views)
    return base_files + app_dependencies + view_count + root_view_controller + storyboard


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

    if project.platform == "android":
        create_android_directories(all_modules)  # TODO: Merge with ios method

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
        # Finished
        # TODO: Update file_count method for android
    elif project.platform == "ios":
        create_ios_directories(all_modules)  # all needed directories

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
        print("{} Files Created.".format(file_count(all_modules)))
    else:
        print "Invalid Generator type\n"
        exit(1)

if __name__ == "__main__":
    main()
