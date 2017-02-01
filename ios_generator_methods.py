from jinja2 import Template

import ios_templates
from shared_generator_methods import cwd, check_directory, uppercase_first_letter, module_directory, \
    lowercase_first_letter, uppercase_views, create_generic_file, lower_module_names, upper_module_names


# create all required directories for project
def create_ios_directories(modules):
    current_dir = cwd()
    check_directory(current_dir)
    check_directory("{}/Modules".format(current_dir))
    check_directory("{}/Common".format(current_dir))
    check_directory("{}/Common/Models".format(current_dir))
    for module in modules:
        check_directory("{}/Modules/{}".format(current_dir, uppercase_first_letter(module.name)))
        check_directory("{}/Modules/{}/ViewControllers".format(current_dir, uppercase_first_letter(module.name)))


# create base module file
def create_ios_module_file(module, file_name, template):
    directory = module_directory(module)
    file_path = "{}/{}.swift".format(directory, file_name)
    with open(file_path, 'w+') as swift_file:
        template_output = Template(template).render(upper_name=uppercase_first_letter(module.name),
                                                    lower_name=lowercase_first_letter(module.name),
                                                    upper_views=uppercase_views(module.views))
        swift_file.write(template_output)


# Create Presenter for this module
def create_ios_presenter(module):
    create_ios_module_file(module, "{}Presenter".format(uppercase_first_letter(module.name)), ios_templates.presenter)


# Create Interactor for this module
def create_ios_interactor(module):
    create_ios_module_file(module, "{}Interactor".format(uppercase_first_letter(module.name)), ios_templates.interactor)


# Create wireframe from this module
def create_wireframe(module):
    create_ios_module_file(module, "{}Wireframe".format(uppercase_first_letter(module.name)), ios_templates.wireframe)


# Create ViewController.swift file for each of the module's views.
def create_view_controllers(module):
    directory = "{}/ViewControllers".format(module_directory(module))
    for view in module.views:
        file_path = "{}/{}{}ViewController.swift".format(directory,
                                                         uppercase_first_letter(module.name),
                                                         uppercase_first_letter(view))
        with open(file_path, 'w+') as view_controller_file:
            template = Template(ios_templates.view_controller_template)
            view_controller_file.write(template.render(upper_name=uppercase_first_letter(module.name),
                                                       upper_view=uppercase_first_letter(view)))


# Generate the Root Wire frame
def create_root_wireframe():
    create_generic_file("{}/Common".format(cwd()), "RootWireframe.swift", ios_templates.root_wireframe)


# create the storyboard file
def create_storyboard(module):
    create_generic_file(module_directory(module),
                        "{}.storyboard".format(module.name.capitalize()),
                        ios_templates.storyboard)


# Create App Dependencies File
def create_app_dependencies(modules):
    file_path = "{}/AppDependencies.swift".format(cwd())
    with open(file_path, 'w+') as app_dependencies_file:
        template = Template(ios_templates.dependencies_template)
        app_dependencies_file.write(template.render(lower_modules=lower_module_names(modules),
                                                    upper_modules=upper_module_names(modules)))
