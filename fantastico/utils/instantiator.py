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

def get_component_path_data(cls):
    '''This method is used to return component folder name and framework root folder starting from a class.'''

    root_folder = get_class_abslocation(cls)[:-1]
    component_folder = root_folder[root_folder.rfind("/") + 1:]
    root_folder = root_folder[:-len(component_folder)]

    return (component_folder, root_folder)

def get_path_to_module_fqdn(abspath, settings_facade):
    '''This method returns the fully qualified module name represented by the given **abspath**.'''
    
    root_folder = get_component_path_data(settings_facade.get_config().__class__)[1]
    
    module_name = abspath.replace(root_folder, "").replace("/", ".")
    
    return "%s" % module_name[:module_name.rfind(".")]
    