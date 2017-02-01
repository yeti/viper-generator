import json
from collections import namedtuple
import sys
import os
import os.path
import templates
import errno
from jinja2 import Template

# Globals
from android_generator_methods import create_android_presenter, create_android_module, create_android_component, \
    create_android_activity, create_android_interactor, create_android_fragments

Module = namedtuple('Module', ['name', 'views'])  # Access attributes with dot syntax


# Functions
def check_valid_input():
    if len(sys.argv) <= 1:
        print "JSON file not provided\n"
        exit(1)


def print_dependencies(modules):
    template = Template(templates.new_dependencies)
    print "\n{}\n".format(file.write(
        template.render(lower__modules=lower_module_names(modules), upper_modules=upper_module_names(modules))))


def get_generator_from_json(json):
    generator = json[0]
    return generator


# returns a list of Module tuples from given JSON
def get_modules_from_json(json):
    mod_array = []
    json.pop(0)  # Remove generator type from start of list
    for mod in json:
        val = Module(name=mod["ModuleName"], views=mod["Views"])
        mod_array.append(val)
    return mod_array


def uppercase_first_letter(s):
    return s[0].upper() + s[1:]


def lowercase_first_letter(s):
    return s[0].lower() + s[1:]


def uppercase_views(views):
    return [uppercase_first_letter(view) for view in views]


def lower_module_names(modules):
    return [lowercase_first_letter(module.name) for module in modules]


def upper_module_names(modules):
    return [uppercase_first_letter(module.name) for module in modules]


# Indicator for how many files were created
def file_count(modules):
    base_files = len(modules) * 3
    app_dependencies = 1
    storyboard = 1
    root_view_controller = 1
    view_count = 0
    for module in modules:
        view_count += len(module.views)
    return base_files + app_dependencies + view_count + root_view_controller + storyboard


# Get the current working directory OR user provided path
def cwd():
    if len(sys.argv) >= 3:
        if sys.argv[2] == "--existing":
            return os.getcwd()
        else:
            return sys.argv[2]
    else:
        return os.getcwd()


# get the given module's directory
def module_directory(module):
    return "{}/Modules/{}".format(cwd(), module.name)


def change_permissions_recursive(path, mode):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            os.chmod(dir, mode)
        for file in files:
            os.chmod(file, mode)


# check if this directory exists, if not, create it
def check_directory(path):
    try:
        os.mkdir(path)
        change_permissions_recursive(path, 777)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            pass


# get JSON from Command Line
def get_json():
    json_filename = sys.argv[1]
    with open(json_filename, 'r') as json_file:
        parsed_json = json.loads(json_file.read())
    return parsed_json


# create all required directories for project
def create_directories(modules):
    current_dir = cwd()
    check_directory(current_dir)
    check_directory("{}/Modules".format(current_dir))
    check_directory("{}/Common".format(current_dir))
    check_directory("{}/Common/Models".format(current_dir))
    for module in modules:
        check_directory("{}/Modules/{}".format(current_dir, uppercase_first_letter(module.name)))
        check_directory("{}/Modules/{}/ViewControllers".format(current_dir, uppercase_first_letter(module.name)))


def create_android_directories(modules):
    current_dir = cwd()
    check_directory(current_dir)
    check_directory("{}/Modules".format(current_dir))
    for module in modules:
        check_directory("{}/Modules/{}".format(current_dir, lowercase_first_letter(module.name)))
        check_directory("{}/Modules/{}/layouts".format(current_dir, uppercase_first_letter(module.name)))


# create base module file
def create_module_file(module, file_name, template):
    directory = module_directory(module)
    file_path = "{}/{}.swift".format(directory, file_name)
    with open(file_path, 'w+') as swift_file:
        template_output = Template(template).render(upper_name=uppercase_first_letter(module.name),
                                                    lower_name=lowercase_first_letter(module.name),
                                                    upper_views=uppercase_views(module.views))
        swift_file.write(template_output)


def create_generic_file(directory, file_name, template):
    file_path = "{}/{}".format(directory, file_name)
    with open(file_path, 'w+') as generic_file:
        generic_file.write(Template(template).render())


# Create Presenter for this module
def create_presenter(module):
    create_module_file(module, "{}Presenter".format(uppercase_first_letter(module.name)), templates.presenter)


# Create Interactor for this module
def create_interactor(module):
    create_module_file(module, "{}Interactor".format(uppercase_first_letter(module.name)), templates.interactor)


# Create wireframe from this module
def create_wireframe(module):
    create_module_file(module, "{}Wireframe".format(uppercase_first_letter(module.name)), templates.wireframe)


# Create ViewController.swift file for each of the module's views.
def create_views(module):
    directory = "{}/ViewControllers".format(module_directory(module))
    for view in module.views:
        file_path = "{}/{}{}ViewController.swift".format(directory,
                                                         uppercase_first_letter(module.name),
                                                         uppercase_first_letter(view))
        with open(file_path, 'w+') as view_controller_file:
            template = Template(templates.view_controller_template)
            view_controller_file.write(template.render(upper_name=uppercase_first_letter(module.name),
                                                       upper_view=uppercase_first_letter(view)))


# Create App Dependencies File
def create_app_dependencies(modules):
    file_path = "{}/AppDependencies.swift".format(cwd())
    with open(file_path, 'w+') as app_dependencies_file:
        template = Template(templates.dependencies_template)
        app_dependencies_file.write(template.render(lower_modules=lower_module_names(modules),
                                                    upper_modules=upper_module_names(modules)))


# Generate the Root Wire frame
def create_root_wireframe():
    create_generic_file("{}/Common".format(cwd()), "RootWireframe.swift", templates.root_wireframe)


# create the storyboard file
def create_storyboard(module):
    create_generic_file(module_directory(module),
                        "{}.storyboard".format(module.name.capitalize()),
                        templates.storyboard)


def main():
    check_valid_input()  # right now just checks number of arguments
    json_input = get_json()  # get json from system args -> exits if not valid JSON
    generator = get_generator_from_json(json_input)  # Get generator type
    all_modules = get_modules_from_json(json_input)

    if generator["Generator"] == "android":
        # TODO: Check if "Project" key exists
        project_name = generator["Project"]
        # TODO: Currently only works for preexisting projects
        create_android_directories(all_modules)  # TODO: Merge with ios method?

        # What to do with this?
        # if "--existing" in sys.argv:
        #     print_dependencies(all_modules)
        # else:
        #     create_app_dependencies(all_modules)  # dependencies file
        #     create_root_wireframe()  # root Wireframe

        # Create All Module Files
        for module in all_modules:
            create_android_module(project_name, module)
            create_android_component(project_name, module)
            create_android_activity(project_name, module)
            create_android_presenter(project_name, module)
            create_android_interactor(project_name, module)
            create_android_fragments(project_name, module)
        # Finished

        pass
    elif generator["Generator"] == "ios":
        create_directories(all_modules)  # all needed directories

        if "--existing" in sys.argv:
            print_dependencies(all_modules)
        else:
            create_app_dependencies(all_modules)  # dependencies file
            create_root_wireframe()  # root Wireframe

        # Create All Module Files
        for module in all_modules:
            create_views(module)
            create_presenter(module)
            create_interactor(module)
            create_wireframe(module)
            create_storyboard(module)
        # end
        print("{} Files Created.".format(file_count(all_modules)))
    else:
        print "Invalid Generator type\n"
        exit(1)

if __name__ == "__main__":
    main()
