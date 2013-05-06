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
.. py:module:: fantastico.mvc.controller_decorator
'''
import inspect

class Controller(object):
    '''This class provides a decorator for magically registering methods as route handlers. This is an extremely important
    piece of Fantastico framework because it simplifies the way you as developer can define mapping between a method that
    must be executed when an http request to an url is made:
    
    .. code-block:: python
    
        @ControllerProvider()
        class BlogsController(BaseController):        
            @Controller(url="/blogs/", method="GET", 
                        models={"Blog": "fantastico.plugins.blog.models.blog.Blog"])
            def list_blogs(self, request):
                Blog = request.models.Blog
            
                blogs = Blog.all_paged(start_record=1, end_record=0, 
                                       sort_expr=[asc(Blog.create_date), desc(Blog.title)])
            
                return Response(blogs)
            
    The above code assume the following:
    
    #. As developer you created a model called blog (this is already mapped to some sort of storage).
    #. Fantastico framework generate the facade automatically (and you never have to know anything about underlining repository).
    #. Fantastico framework takes care of data conversion.
    #. As developer you create the method that knows how to handle **/blog/** url.
    #. Write your view.
    
    Below you can find the design for MVC provided by **Fantastico** framework:
    
    .. image:: /images/core/mvc.png'''
    
    _REGISTERED_ROUTES = {}
    
    @property
    def url(self):
        '''This property retrieves the url used when registering this controller.'''
        
        return self._url
    
    @property
    def method(self):
        '''This property retrieves the method(s) for which this controller can be invoked. Most of the time only one value is
        retrieved.'''
        
        return self._method
    
    @property
    def models(self):
        '''This property retrieves all the models required by this controller in order to work correctly.'''
        
        return self._models
    
    @property
    def fn_handler(self):
        '''This property retrieves the method which is executed by this controller.'''
        
        return self._fn_handler
    
    def __init__(self, url, method="GET", models=None):
        self._url = url
        
        if isinstance(method, str):
            self._method = [method]
        elif isinstance(method, list):
            self._method = method
        
        if not models:
            models = {}
            
        self._models = models
        
        self._fn_handler = None
    
    @classmethod
    def get_registered_routes(cls):
        '''This class methods retrieve all registered routes through Controller decorator.'''
        
        return cls._REGISTERED_ROUTES
    
    def __call__(self, orig_fn):
        '''This method takes care of registering the controller when the class is first loaded by python vm.'''
        
        def new_handler(*args):
            '''This method is the one that replaces the original decorated method.'''
            
            return orig_fn(*args)
        
        self._fn_handler = new_handler
        
        Controller.get_registered_routes()[self.url] = self
        
        return self._fn_handler
    
class ControllerProvider(object):
    '''This class marks a class as being a controller provider. It means that some of the methods from decorated class 
    provide routes that must be registered into routing engine.'''
    
    def __init__(self):
        self._decorated_cls = None
        self.__doc__ = None
        
    def __call__(self, cls):
        '''This method is used to enrich all methods of the class with full_name attribute.'''
        
        def is_function(obj):
            '''This function determines if the given obj argument is a function or not.'''
            
            return inspect.isfunction(obj)
        
        for meth_name, meth_value in inspect.getmembers(cls, is_function):
            full_name = "%s.%s.%s" % (cls.__module__, cls.__name__, meth_name)
            setattr(meth_value, "full_name", full_name)
                
        self._decorated_cls = cls
        self.__doc__ = cls.__doc__
        
        def instantiate(*args, **kwargs):
            '''This method returns a new instance of the decorated class. It passes all arguments to the underlining class
            __init__ method.'''
            
            instance = object.__new__(self._decorated_cls)
            self._decorated_cls.__init__(instance, *args, **kwargs)
            
            return instance
        
        return instantiate