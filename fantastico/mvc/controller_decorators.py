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

from fantastico import mvc
from fantastico.exceptions import FantasticoControllerInvalidError
from fantastico.mvc.base_controller import BaseController
from fantastico.mvc.model_facade import ModelFacade
from fantastico.oauth2.exceptions import OAuth2UnauthorizedError, OAuth2Error
from fantastico.utils import instantiator
from webob.response import Response


class ModelsHolder(dict):
    '''This class is used for holding all models injected into a controller.'''

    def __getattr__(self, name):
        '''This method allows dictionary keys to be accessed as attributes.'''

        return self.get(name)

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

                blogs = Blog.get_records_paged(start_record=0, end_record=5,
                                       sort_expr=[ModelSort(Blog.model_cls.create_date, ModelSort.ASC,
                                                  ModelSort(Blog.model_cls.title, ModelSort.DESC)],
                                       filter_expr=ModelFilterAnd(
                                                       ModelFilter(Blog.model_cls.id, 1, ModelFilter.GT),
                                                       ModelFilter(Blog.model_cls.id, 5, ModelFilter.LT))))

                # convert blogs to desired format. E.g: json.

                return Response(blogs)

    The above code assume the following:

    #. As developer you created a model called blog (this is already mapped to some sort of storage).
    #. Fantastico framework generate the facade automatically (and you never have to know anything about underlining repository).
    #. Fantastico framework takes care of data conversion.
    #. As developer you create the method that knows how to handle **/blog/** url.
    #. Write your view.

    You can also map multiple routes for the same controller:

    .. code-block python

        @ControllerProvider()
        class SimpleExample(BaseController):
            @Controller(url=["/url1$", "/url2$")
            def handle_urls(self, request):
                # your logic comes here

    Below you can find the design for MVC provided by **Fantastico** framework:

    .. image:: /images/core/mvc.png'''

    _SUPPORTED_VERBS = ["get", "head", "post", "put", "delete", "trace", "options", "connect", "patch"]
    _REGISTERED_ROUTES = []

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

    def __init__(self, url, method="GET", models=None, **kwargs):
        if isinstance(url, str):
            self._url = [url]
        elif isinstance(url, list):
            self._url = url

        self._method = None

        if isinstance(method, str):
            self._method = [method]
        elif isinstance(method, list):
            self._method = method

        self._is_method_valid(self._method)

        if not models:
            models = {}

        self._models = models
        self._model_facade = kwargs.get("model_facade", ModelFacade)
        self._conn_manager = kwargs.get("conn_manager")

        self._fn_handler = None

    def _is_method_valid(self, http_methods):
        '''This method detects if the specified http method is valid or not.'''

        if not isinstance(http_methods, list):
            http_methods = [http_methods]

        for http_method in http_methods:
            if not http_method or http_method.lower() not in Controller._SUPPORTED_VERBS:
                raise FantasticoControllerInvalidError("Http verb %s not supported as controller method." % http_method)

    @classmethod
    def get_registered_routes(cls):
        '''This class methods retrieve all registered routes through Controller decorator.'''

        return cls._REGISTERED_ROUTES

    def _inject_models(self, request, session):
        '''This method is used to inject the models required by a controller into request. Model fully qualified
        name is resolved to a class and appended to request.models attribute.'''

        models_to_inject = ModelsHolder()

        for model_name in self.models:
            model_cls = instantiator.import_class(self.models[model_name])

            models_to_inject[model_name] = self._model_facade(model_cls, session)

        request.models = models_to_inject

    def __call__(self, orig_fn):
        '''This method takes care of registering the controller when the class is first loaded by python vm.'''

        def new_handler(*args, **kwargs):
            '''This method is the one that replaces the original decorated method.'''

            request = self._get_request_from_args(args)

            self._validate_security_context(request)

            conn_manager = self._conn_manager or mvc.CONN_MANAGER
            db_conn = conn_manager.get_connection(request.request_id)

            self._inject_models(request, db_conn)

            return orig_fn(*args, **kwargs)

        new_handler.__name__ = orig_fn.__name__
        new_handler.__doc__ = orig_fn.__doc__
        new_handler.__module__ = orig_fn.__module__
        setattr(new_handler, "orig_fn", orig_fn)

        self._fn_handler = new_handler

        self.get_registered_routes().append(self)

        return self._fn_handler

    def _get_request_from_args(self, args):
        '''This method extract the current request from arguments array. It is possible to raise an exception when the method
        does not have the correct signature (request argument not present).'''

        request = None

        try:
            request = args[0]

            if isinstance(request, BaseController):
                contr = request
                request = args[1]

                contr.curr_request = request
        except IndexError as ex:
            raise FantasticoControllerInvalidError(ex)

        return request

    def _validate_security_context(self, request):
        '''This method triggers security request validation. Security context is always present (being injected by oauth2
        tokens middleware).'''

        security_ctx = request.context.security

        try:
            if not security_ctx.validate_context():
                raise OAuth2UnauthorizedError(msg="Security context insufficient scopes.")
        except OAuth2Error:
            raise
        except Exception as ex:
            raise OAuth2UnauthorizedError(msg="Security context validation exception: %s" % str(ex))

class ControllerProvider(object):
    '''This class marks a class as being a controller provider. It means that some of the methods from decorated class
    provide routes that must be registered into routing engine.'''

    def __init__(self):
        pass

    def __call__(self, cls):
        '''This method is used to enrich all methods of the class with full_name attribute.'''

        def is_function(obj):
            '''This function determines if the given obj argument is a function or not.'''

            return inspect.isfunction(obj)

        for meth_name, meth_value in inspect.getmembers(cls, is_function):
            full_name = "%s.%s.%s" % (cls.__module__, cls.__name__, meth_name)
            setattr(meth_value, "full_name", full_name)

        return cls

class CorsEnabled(object):
    '''This class provides the cors behavior which ensures all cors required headers are appended to response. It is designed
    to be used on controller methods decorated with @Controller attribute.
    
    .. code-block:: python
    
        @Controller(url="/api/filesystem/(?P<filename>.*)$", method="OPTIONS")
        @CorsEnabled()
        def upload_file_options(self, request, filename):        
            pass
        
    As you can see there is no need to implement cors controller methods because the decorator does all the job.
    '''
    
    def __call__(self, orig_fn):
        def cors_enabled_fn(self, request, *args, **kwargs): # pylint: disable=W0613
            '''This method provides the algorithm for building a generic cors response for the current request.'''
            
            kwargs = kwargs or {}
    
            response = Response(content_type="application/json", status_code=200)
            response.headers["Content-Length"] = "0"
            response.headers["Cache-Control"] = "private"
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "OPTIONS,GET,POST,PUT,DELETE"
            response.headers["Access-Control-Allow-Headers"] = request.headers.get("Access-Control-Request-Headers", "")
    
            return response

        cors_enabled_fn.__name__ = orig_fn.__name__
        cors_enabled_fn.__doc__ = orig_fn.__doc__
        cors_enabled_fn.__module__ = orig_fn.__module__

        return cors_enabled_fn
