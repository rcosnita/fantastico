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
.. py:module:: fantastico.rendering.url_invoker
'''

from fantastico.exceptions import FantasticoUrlInvokerError
import abc

class UrlInvoker(object, metaclass=abc.ABCMeta):
    '''This class is responsible for invoking urls and returning the rendered result. Each concrete implementation is responsible
    for providing the actual invoking mechanism for the protocol it provides support for.'''

    @abc.abstractmethod
    def invoke_url(self, url, headers, method):
        '''This generic method invoke an url for a specific list of headers and a given method.

        :param url: The url we want to render.
        :type url: string
        :param headers: A dictionary of headers that must be passed to the url.
        :type headers: dict
        :param method: The method used for invoking the url. For an http invoker this is GET (the only supported method for now).
        :type method: string
        :returns: The string containing the invoke result.'''

class FantasticoUrlInternalInvoker(UrlInvoker):
    '''This class provides a reliable mechanism for invoking internal fantastico urls and retrieving their result. In order
    to use this type of url invoker you need to provide the current uwsgi application as well as the wsgi environment under
    which the given url must be rendered.'''

    _http_headers = None
    _http_status = None

    def __init__(self, fantastico_app, environ):
        self._reset_internal_state()

        self._app = fantastico_app
        self._environ = environ

    @property
    def http_status(self):
        '''This property retrieves the last invoked url response status.'''

        return self._http_status

    @property
    def http_headers(self):
        '''This property retrieves the last invoked url response headers.'''

        return self._http_headers

    def invoke_url(self, url, headers, method="GET"):
        '''This method correctly invokes an url from the current fantastico application.'''

        self._http_headers = []
        self._http_status = None

        try:
            response = self._app(self._environ, self._start_response)
        except Exception as ex:
            raise FantasticoUrlInvokerError(ex)

        return response

    def _start_response(self, http_status, http_headers):
        '''This method replaces WSGI start_response method. It collects the response status and headers and make them
        available to the current invoker.'''

        self._http_status = http_status
        self._http_headers = http_headers

    def _reset_internal_state(self):
        '''This method reset the internal state variables from the last invocation to default values.'''

        self._http_headers = []
        self._http_status = None
