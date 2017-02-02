# Create base module file
from jinja2 import Template

import android_templates
from shared_generator_methods import uppercase_first_letter, lowercase_first_letter, cwd, \
    check_directory


def create_android_directories(modules):
    current_dir = cwd()
    check_directory(current_dir)
    for module in modules:
        check_directory("{}/{}".format(current_dir, lowercase_first_letter(module.name)))
        check_directory("{}/{}/layouts".format(current_dir, uppercase_first_letter(module.name)))


def get_module_directory(module):
    return "{}/{}".format(cwd(), module.name)


def create_java_file(project_name, module, file_name, template):
    directory = get_module_directory(module)
    file_path = "{}/{}.java".format(directory, file_name)
    with open(file_path, 'w+') as java_file:
        template_output = Template(template).render(lower_project_name=lowercase_first_letter(project_name),
                                                    upper_project_name=uppercase_first_letter(project_name),
                                                    lower_module_name=lowercase_first_letter(module.name),
                                                    upper_module_name=uppercase_first_letter(module.name))

        java_file.write(template_output)


def create_xml_file(project_name, module, file_name, template):
    directory = get_module_directory(module)
    file_path = "{}/layouts/{}.xml".format(directory, file_name)
    with open(file_path, 'w+') as java_file:
        template_output = Template(template).render(lower_project_name=lowercase_first_letter(project_name),
                                                    upper_project_name=uppercase_first_letter(project_name),
                                                    lower_module_name=lowercase_first_letter(module.name),
                                                    upper_module_name=uppercase_first_letter(module.name))

        java_file.write(template_output)


# Create Module for this module
def create_android_module(project_name, module):
    create_java_file(project_name=project_name,
                     module=module,
                     file_name="{}Module".format(uppercase_first_letter(module.name)),
                     template=android_templates.module)


# Create Component for this module
def create_android_component(project_name, module):
    create_java_file(project_name=project_name,
                     module=module,
                     file_name="{}Component".format(uppercase_first_letter(module.name)),
                     template=android_templates.component)


# Create Activity and Activity XML for this module
def create_android_activity(project_name, module):
    create_java_file(project_name=project_name,
                     module=module,
                     file_name="{}Activity".format(uppercase_first_letter(module.name)),
                     template=android_templates.activity)

    create_xml_file(project_name=project_name,
                    module=module,
                    file_name="activity_{}".format(lowercase_first_letter(module.name)),
                    template=android_templates.fragment_xml)

    create_xml_file(project_name=project_name,
                    module=module,
                    file_name="{}_activity_update_for_android_manifest".format(lowercase_first_letter(module.name)),
                    template=android_templates.update_android_manifest_xml)


# Create Presenter for this module
def create_android_presenter(project_name, module):
    create_java_file(project_name=project_name,
                     module=module,
                     file_name="{}Presenter".format(uppercase_first_letter(module.name)),
                     template=android_templates.presenter)


# Create Interactor for this module
def create_android_interactor(project_name, module):
    create_java_file(project_name=project_name,
                     module=module,
                     file_name="{}Interactor".format(uppercase_first_letter(module.name)),
                     template=android_templates.interactor)


# Create ViewController.swift file for each of the module's views.
def create_android_fragments(project_name, module):
    for view in module.views:
        directory = get_module_directory(module)
        file_path = "{}/{}Fragment.java".format(directory, view)
        with open(file_path, 'w+') as java_file:
            template_output = Template(android_templates.fragment).render(
                lower_project_name=lowercase_first_letter(project_name),
                lower_module_name=lowercase_first_letter(module.name),
                upper_module_name=uppercase_first_letter(module.name),
                upper_fragment_name=uppercase_first_letter(view))

            java_file.write(template_output)

            create_xml_file(project_name=project_name,
                            module=module,
                            file_name="fragment_{}".format(lowercase_first_letter(view)),
                            template=android_templates.fragment_xml)
