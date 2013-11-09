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

.. py:module:: fantastico.exceptions

This package contains all core fantastico exceptions that are raised by different methods.
'''

class FantasticoError(Exception):
    '''.. image:: /images/core/exceptions.png

    **FantasticoError** is the base of all exceptions raised within fantastico framework. It describe common attributes that
    each concrete fantastico exception must provide. By default all fantastico exceptions inherit FantasticoError exception.
    We do this because each raised unhandled FantasticoError is map to a specific exception response. This strategy guarantees
    that at no moment errors will cause fantastico framework wsgi container to crash.
    '''

    @property
    def http_code(self):
        '''This method returns the http code on which this exception is mapped.'''

        return self._http_code

    def __init__(self, msg=None, http_code=400):
        super(FantasticoError, self).__init__(msg)

        self._http_code = http_code

class FantasticoControllerInvalidError(FantasticoError):
    '''This exception is raised whenever a method is decorated with
    :py:class:`fantastico.mvc.controller_decorators.Controller` and the number of arguments is not correct. Usually
    developer forgot to add request as argument to the controller.'''

class FantasticoClassNotFoundError(FantasticoError):
    '''This exception is raised whenever code tries to dynamically import and instantiate a class which can not be resolved.'''

class FantasticoNotSupportedError(FantasticoError):
    '''This exception is raised whenever code tries to do an operation that is  not supported.'''

class FantasticoSettingNotFoundError(FantasticoError):
    '''This exception is raised whenever code tries to obtain a setting that is not available in the current fantastico
    configuration.'''

class FantasticoDuplicateRouteError(FantasticoError):
    '''This exception is usually raised by routing engine when it detects duplicate routes.'''

class FantasticoNoRoutesError(FantasticoError):
    '''This exception is usually raised by routing engine when no loaders are configured or no routes are registered.'''

class FantasticoRouteNotFoundError(FantasticoError):
    '''This exception is usually raised by routing engine when a requested url is not registered.'''

class FantasticoNoRequestError(FantasticoError):
    '''This exception is usually raised when some components try to use fantastico.request from WSGI environ before
    :py:class:`fantastico.middleware.request_middleware.RequestMiddleware` was executed.'''

class FantasticoContentTypeError(FantasticoError):
    '''This exception is usually thrown when a mismatch between request accept and response content type. In
    Fantastico we think it's mandatory to fulfill requests correctly and to take in consideration sent headers.'''

class FantasticoHttpVerbNotSupported(FantasticoError):
    '''This exception is usually thrown when a route is accessed with an http verb which does not support.'''

    @property
    def http_verb(self):
        '''This property returns the http verb that caused the problems.'''

        return self._http_verb

    def __init__(self, http_verb):
        super(FantasticoHttpVerbNotSupported, self).__init__()

        self._http_verb = http_verb

class FantasticoTemplateNotFoundError(FantasticoError):
    '''This exception is usually thrown when a controller tries to load a template which it does not found.'''

class FantasticoIncompatibleClassError(FantasticoError):
    '''This exception is usually thrown when we want to decorate / inject / mixin a class into another class
    that does not support it. For instance, we want to build a :py:class:`fantastico.mvc.model_facade.ModelFacade`
    with a class that does not extend **BASEMODEL.**'''

class FantasticoDbError(FantasticoError):
    '''This exception is usually thrown when a database exception occurs. For one good example where this is used see
    :py:class:`fantastico.mvc.model_facade.ModelFacade`.'''

class FantasticoDbNotFoundError(FantasticoDbError):
    '''This exception is usually thrown when an entity does not exist but we try to update it. For one good example where this is
    used see :py:class:`fantastico.mvc.model_facade.ModelFacade`.'''

class FantasticoInsufficientArgumentsError(FantasticoError):
    '''This exception is usually thrown when a component extension received wrong number of arguments. See
    :py:class:`fantastico.rendering.component.Component`.'''

class FantasticoUrlInvokerError(FantasticoError):
    '''This exception is usually thrown when an internal url invoker fails. For instance, if a component reusage rendering
    fails then this exception is raised.'''
