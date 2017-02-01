# Get the current working directory OR user provided path
import os
import sys


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