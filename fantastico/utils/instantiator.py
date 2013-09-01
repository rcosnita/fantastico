'''
Copyright 2013 Cosnita Radu Viorel

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. codeauthor:: Radu Viorel Cosnita <radu.cosnita@gmail.com>

.. py:module:: fantastico.utils.instantiator

This module provides helper methods used for instantiating classes by given string values.
'''
from fantastico.exceptions import FantasticoClassNotFoundError
import importlib
import inspect
import os

def instantiate_class(full_name, constr_args=None):
    '''Method used to instantiate a class starting from its full name.

    :param full_name: fully qualified class name.
    :type full_name: string
    :param constr_args: A list of arguments we want to pass to the constructor.
    :type constr_args: list
    :returns: A new instance of the full_name class.
    '''

    if constr_args is None:
        constr_args = []

    return import_class(full_name)(*constr_args)

def import_class(full_name):
    '''Method used to import a class dynamically starting from its full name.

    :param full_name: fully qualified class name.
    :type full_name: string'''

    last_dot = full_name.rfind(".")

    module_name, class_name = full_name[:last_dot], full_name[last_dot + 1:]

    try:
        module = importlib.import_module(module_name)
    except ImportError as ex:
        raise FantasticoClassNotFoundError(str(ex))

    try:
        return getattr(module, class_name)
    except AttributeError as ex:
        raise FantasticoClassNotFoundError(str(ex))

def get_class_abslocation(cls):
    '''This method returns the absolute location for a given class (without class name and module name).'''

    module_name = cls.__module__[cls.__module__.rfind(".") + 1:]

    return inspect.getabsfile(cls).replace(module_name + ".py", "")

def get_component_path_data(cls, root_folder_ref=None):
    '''This method is used to return component folder name and framework root folder starting from a class.'''

    root_folder = root_folder_ref
    cls_folder = get_class_abslocation(cls)[:-1]

    if not root_folder_ref:
        root_folder = cls_folder
        component_folder = root_folder[root_folder.rfind("/") + 1:]
        root_folder = root_folder[:-len(component_folder)]
    else:
        component_folder = cls_folder[len(root_folder_ref):]

    return (component_folder, root_folder)

def get_path_to_module_fqdn(abspath, settings_facade):
    '''This method returns the fully qualified module name represented by the given **abspath**.'''

    root_folder = get_component_path_data(settings_facade.get_config().__class__)[1]

    module_name = abspath.replace(root_folder, "").replace("/", ".")

    return "%s" % module_name[:module_name.rfind(".")]

def scan_folder_by_criteria(folder, file_matcher, action, os_lib=os):
    '''This method provides the algorithm for scanning a given location and executing an action for each file.

    .. code-block:: python

        scan_folder_for_criteria("/test_folder",
                                lambda filename: filename.endswith(".py"),
                                lambda abspath, filename: print(abspath + "----> + filename))

    As you can see in the above example, for using this method you have to define a matcher which is executed against each
    filename found in the given folder as well as an action executed for each matched file.'''

    for filename in os_lib.listdir(folder):
        if not file_matcher(folder, filename):
            continue

        if folder[-1] != "/":
            folder += "/"

        abspath = "%s%s" % (folder, filename)

        action(abspath, filename)

def import_modules_from_folder(folder, file_matcher, settings_facade):
    '''This is a helper method used to register all python modules recursively using a given settings facade instance.'''

    def import_modules(abspath, filename):
        '''This is the method executed automatically for importing all modules from a given filename.'''

        if os.path.isdir(abspath):
            import_modules_from_folder(abspath + "/", file_matcher, settings_facade)
        else:
            if not filename.endswith(".py"):
                return

            module_name = get_path_to_module_fqdn(abspath, settings_facade)

            importlib.import_module(module_name)

    scan_folder_by_criteria(folder, file_matcher, import_modules)

def get_package_abslocation(package):
    '''This method obtains the absolute package location on disk from a given python package.'''

    pkg_location = package.__file__

    return pkg_location[:pkg_location.rfind("/") + 1]
