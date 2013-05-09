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

.. py:module:: fantastico.mvc.base_controller
'''
from fantastico.utils import instantiator
from jinja2.loaders import FileSystemLoader
from jinja2.environment import Environment

class BaseController(object):
    '''This class provides common methods useful for every concrete controller. Even if no type checking is done in 
    Fantastico it is recommended that every controller implementation inherits this class.'''
    
    def __init__(self, settings_facade):
        self._settings_facade = settings_facade
        
        self._tpl_loader = None
        self._tpl_env = None
    
    def __init_jinja_context(self):
        '''This method initialize the jinja context in order to make the controller able to render jinja2 files.'''
        
        views_folder = ("%s%s/views/" % (self._settings_facade.get_root_folder(), self.get_component_folder()))
        
        self._tpl_loader = FileSystemLoader(searchpath=views_folder)
        self._tpl_env = Environment(loader=self._tpl_loader)
    
    def get_component_folder(self):
        '''This method is used to retrieve the component folder name under which this controller is defined.'''
        
        root_folder = self._settings_facade.get_root_folder()
        
        return instantiator.get_component_path_data(self.__class__, root_folder)[0]
    
    def load_template(self, tpl_name, model_data=None):
        '''This method is responsible for loading a template from disk and render it using the given model data.
        
        .. code-block:: python
        
            @ControllerProvider()
            class TestController(BaseController):
                @Controller(url="/simple/test/hello", method="GET")
                def say_hello(self, request):
                    return Response(self.load_template("/hello.html"))
                    
            The above snippet will search for **hello.html** into component folder/views/.
        '''
        
        if self._tpl_env is None:
            self.__init_jinja_context()
        
        model_data = model_data or {}
        
        return self._tpl_env.get_template(tpl_name, model_data) 