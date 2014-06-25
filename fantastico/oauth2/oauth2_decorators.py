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
.. py:module:: fantastico.oauth2.oauth2_decorators
'''
import inspect

from fantastico.exceptions import FantasticoControllerInvalidError
from fantastico.mvc.base_controller import BaseController
from fantastico.oauth2.exceptions import OAuth2UnauthorizedError
from fantastico.oauth2.security_context import SecurityContext


class RequiredScopes(object):
    '''This class provides the decorator for enforcing fantastico to authorize requests against ROA resources and MVC controllers.

    .. code-block:: python

        # enforce authorization for MVC controllers.
        @ControllerProvider()
        class SecuredController(BaseController):
            @Controller(url="/secured-controller/ui/index")
            @RequiredScopes(scopes=["greet.verbose", "greet.read"])
            def say_hello(self, request):
                return "<html><body><h1>Hello world</body></html>"

    .. code-block:: python

        # enforce authorization for ROA resources.
        @Resource(name="app-setting", url="/app-settings", version=1.0)
        @RequiredScopes(create="app_setting.create",
                        read="app_setting.read",
                        update="app_setting.update",
                        delete="app_setting.delete"})
        class AppSetting(BASEMODEL):
            id = Column("id", Integer, primary_key=True, autoincrement=True)
            name = Column("name", String(50), unique=True, nullable=False)
            value = Column("value", Text, nullable=False)

            def __init__(self, name, value):
                self.name = name
                self.value = value
    '''

    @property
    def scopes(self):
        '''This property returns the currently set scopes (including create, read, update, delete).'''

        return self._scopes

    @property
    def create_scopes(self):
        '''This property returns the scopes required for create calls.'''

        return self._create_scopes

    @property
    def read_scopes(self):
        '''This property returns the scopes required for read calls.'''

        return self._read_scopes

    @property
    def update_scopes(self):
        '''This property returns the scopes required for update calls.'''

        return self._update_scopes

    @property
    def delete_scopes(self):
        '''This property returns the scopes required for delete calls.'''

        return self._delete_scopes

    def __init__(self, scopes=None, create=None, read=None, update=None, delete=None):
        self._scopes = set(self._get_list_from_param(scopes))
        self._create_scopes = self._get_list_from_param(create)
        self._read_scopes = self._get_list_from_param(read)
        self._update_scopes = self._get_list_from_param(update)
        self._delete_scopes = self._get_list_from_param(delete)

        tmp_scopes = []
        tmp_scopes.extend(self._create_scopes)
        tmp_scopes.extend(self._read_scopes)
        tmp_scopes.extend(self._update_scopes)
        tmp_scopes.extend(self._delete_scopes)

        for scope in tmp_scopes:
            self._scopes.add(scope)

        self._scopes = list(self._scopes)
        self._scopes.sort()

    def _get_list_from_param(self, param_value):
        '''This method ensures param_value is a list. In case param value is string it is transformed to a list with
        one element.'''

        param_value = param_value or []

        if isinstance(param_value, list):
            return param_value

        if isinstance(param_value, str):
            return [param_value]

        raise ValueError("param value %s is not supported for scopes." % param_value)

    def __call__(self, orig_fn):
        '''This method is invoked once when decorated function is wrapped.'''

        if inspect.isfunction(orig_fn):
            return self._handle_fn_decoration(orig_fn)
        elif inspect.isclass(orig_fn):
            return self._handle_class_decoration(orig_fn)

    def _handle_class_decoration(self, orig_class):
        '''This method appends get_required_scopes method to the given class in order to make it aware of mandatory scopes
        which must be available when invoked.'''

        orig_class.get_required_scopes = lambda inst = None: self

        return orig_class

    def _handle_fn_decoration(self, orig_fn):
        '''This method decorates a given method and enrich it's behavior so that request security context is also aware of
        required scopes.'''

        def new_fn(*args, **kwargs):
            '''This method replaces the original decorated method and it first injects security scopes into security context and
            then it executes the original method.'''

            request = self._get_request_from_args(args)
            self.inject_scopes_in_security(request)

            if not request.context.security.validate_context():
                raise OAuth2UnauthorizedError("You are not authorized to access the resource.")

            return orig_fn(*args, **kwargs)

        new_fn.__name__ = orig_fn.__name__
        new_fn.__doc__ = orig_fn.__doc__
        new_fn.__module__ = orig_fn.__module__

        return new_fn

    def _get_request_from_args(self, args):
        '''This method obtains the current request argument from a list of arguments.'''

        try:
            request = args[0]

            if isinstance(request, BaseController):
                request = args[1]
        except IndexError as ex:
            raise FantasticoControllerInvalidError(ex)

        return request

    def inject_scopes_in_security(self, request):
        '''This method injects the request scopes into request security context.'''

        security_ctx = request.context.security

        ctx = SecurityContext(access_token=security_ctx.access_token,
                              required_scopes=self)
                
        request.context.security = ctx