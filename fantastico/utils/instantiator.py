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
import importlib
from fantastico.exceptions import FantasticoClassNotFoundError

def instantiate_class(full_name, constr_args=[]):
    '''Method used to instantiate a class starting from it's full name.
    
    :param full_name: fully qualified class name.
    :type full_name: string
    :param constr_args: A list of arguments we want to pass to the constructor.
    :type constr_args: list
    :returns: A new instance of the full_name class.
    '''
    
    last_dot = full_name.rfind(".")
    
    module_name, class_name = full_name[:last_dot], full_name[last_dot + 1:]
    
    try:
        module = importlib.import_module(module_name)
    except ImportError as ex:
        raise FantasticoClassNotFoundError(str(ex))
    
    try:
        return getattr(module, class_name)(*constr_args)
    except AttributeError as ex:
        raise FantasticoClassNotFoundError(str(ex))    