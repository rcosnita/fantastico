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
.. py:module:: fantastico.oauth2.middleware.exceptions_middleware
'''
from fantastico.oauth2.exceptions import OAuth2MissingQueryParamError, OAuth2AuthenticationError, OAuth2InvalidClientError, \
    OAuth2Error, OAuth2UnsupportedGrantError
from fantastico.routing_engine.custom_responses import RedirectResponse
from fantastico.settings import SettingsFacade
from webob.response import Response
import json
from fantastico.exception_formatters import ExceptionFormattersFactory

class OAuth2ExceptionsMiddleware(object):
    '''This class provides the support for dynamically casting OAuth2 errors into concrete error responses. At the moment
    responses are returned only in english and have the format specified in RFC6749. Mainly, at each intercepted OAuth2
    exceptions a json response is returned to the client.'''

    def __init__(self, app, settings_facade_cls=SettingsFacade, exceptions_factory_cls=ExceptionFormattersFactory):
        self._app = app
        self._doc_base = settings_facade_cls().get("doc_base")
        self._exceptions_factory = exceptions_factory_cls()

    def __call__(self, environ, start_response):
        body = None
        http_code = None

        try:
            return self._app(environ, start_response)
        except OAuth2MissingQueryParamError as ex:
            body = {"error": "invalid_request",
                    "error_description": "%s query parameter is mandatory." % ex.param_name,
                    "error_uri": self._get_error_uri(ex.error_code)}

            http_code = ex.http_code
        except OAuth2AuthenticationError as ex:
            body = {"error": "access_denied",
                    "error_description": str(ex),
                    "error_uri": self._get_error_uri(ex.error_code)}

            http_code = ex.http_code
        except OAuth2InvalidClientError as ex:
            body = {"error": "invalid_client",
                    "error_description": str(ex),
                    "error_uri": self._get_error_uri(ex.error_code)}

            http_code = ex.http_code
        except OAuth2UnsupportedGrantError as ex:
            body = {"error": "unsupported_grant_type",
                    "error_description": str(ex),
                    "error_uri": self._get_error_uri(ex.error_code)}

            http_code = ex.http_code
        except OAuth2Error as ex:
            body = {"error": "server_error",
                    "error_description": str(ex),
                    "error_uri": self._get_error_uri(ex.error_code)}

            if ex.http_code >= 500:
                http_code = 400
            else:
                http_code = ex.http_code

        response = self._build_response(environ, body, http_code)

        start_response(response.status, response.headerlist)

        return [response.body]

    def _get_error_uri(self, error_code):
        '''This method return the error_uri value based on the given error code. It points to a Fantastico official documentation
        page.'''

        return "%sfeatures/oauth2/exceptions/%s.html" % (self._doc_base, error_code)

    def _build_response(self, environ, body, http_code):
        '''This method builds transforms the given body into a wsgi response object.'''

        curr_request = environ["fantastico.request"]
        redirect_uri = curr_request.params.get("redirect_uri")

        ex_format = curr_request.params.get("error_format", ExceptionFormattersFactory.JSON)
        ex_formatter = self._exceptions_factory.get_formatter(ex_format)

        response = ex_formatter.format_ex(body, ctx={"redirect_uri": redirect_uri})

        if ex_format == ExceptionFormattersFactory.JSON:
            response = Response(body=json.dumps(response).encode(), content_type="application/json; charset=UTF-8", 
                                status=http_code)
            self._add_cors_headers(response)
            
            return response

        response = RedirectResponse(response)
        self._add_cors_headers(response)
        
        return response

    def _add_cors_headers(self, response):
        '''This method adds the cors headers required to support cross domain requests exception serialization.'''
        
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "OPTIONS,GET,POST,PUT,DELETE"
