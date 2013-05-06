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
.. py:module:: fantastico.mvc.controller_registrator
'''
from fantastico.mvc.controller_decorators import Controller
from fantastico.routing_engine.routing_loaders import RouteLoader
from fantastico.settings import SettingsFacade
from fantastico.utils import instantiator
import importlib
import os

class ControllerRouteLoader(RouteLoader):
    '''This class provides a route loader that is capable of scanning the disk and registering only the routes that 
    contain a controller decorator in them. This happens when **Fantastico** servers starts. In standard configuration
    it ignores tests subfolder as well as test_* / itest_* modules.'''
    
    def __init__(self, settings_facade=SettingsFacade, scanned_folder=None, ignore_prefix=None):
        super(ControllerRouteLoader, self).__init__(settings_facade)
        
        self._scanned_folder = scanned_folder or instantiator.get_class_abslocation(settings_facade.__class__)
        self._ignore_prefix = ignore_prefix or ["__init__", "__pycache__", "tests", "test", "itest"]
    
    def _transform_to_fqdn(self, abspath):
        '''This method transform an absolute file location to fully qualified name python notation.'''
        
        root_folder = instantiator.get_class_abslocation(SettingsFacade)
        
        module_name = abspath.replace(root_folder, "").replace("/", ".")
        
        return "fantastico.%s" % module_name[:module_name.rfind(".")]

    def _is_ignored_file(self, filename):
        '''This method determines if a filename is ignored or not.'''
        
        for prefix in self._ignore_prefix:
            if filename.startswith(prefix):
                return True
            
        return False
    
    def _register_from_folder(self, folder):
        '''This method is used for registering all modules that contains Controller from a given location.'''

        for filename in os.listdir(folder):
            if self._is_ignored_file(filename):
                continue
            
            abspath = "%s%s" % (folder, filename)
            
            if os.path.isdir(abspath):
                self._register_from_folder(abspath + "/")
            else:
                if not filename.endswith(".py"):
                    continue
                
                module_name = self._transform_to_fqdn(abspath)
            
                importlib.import_module(module_name)
    
    def load_routes(self):
        '''This method is used for loading all routes that are mapped through 
        :py:class:`fantastico.mvc.controller_decorators.Controller` decorator.'''
        
        self._register_from_folder(self._scanned_folder)
            
        return Controller.get_registered_routes()