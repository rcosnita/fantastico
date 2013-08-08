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

.. py:module:: fantastico.middleware.tests.test_request_middleware
'''
from fantastico import mvc
from fantastico.middleware.request_middleware import RequestMiddleware
from fantastico.settings import BasicSettings
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
import os
from fantastico.routing_engine.custom_responses import RedirectResponse


class RequestMiddlewareTests(FantasticoUnitTestsCase):
    '''Test suite for ensuring that environ wsgi dictionary is correctly converted to a request object.'''

    def init(self):
        self._app = Mock()
        self._start_response = Mock()
        self._middleware = RequestMiddleware(self._app)

        self._environ = {"CONTENT_TYPE": "application/json",
                       "HTTP_ACCEPT": "application/json",
                       "HTTP_ACCEPT_LANGUAGE": "ro-ro,en-US;q=0.8",
                       "HTTP_OAUTH_BEARER": "123",
                       "HTTP_HOST": "localhost:80",
                       "PATH_INFO": "/article",
                       "QUERY_STRING": "id=1",
                       "REQUEST_METHOD": "GET",
                       "SCRIPT_NAME": "",
                       "SERVER_NAME": "localhost",
                       "SERVER_PORT": "80",
                       "SERVER_PROTOCOL": "HTTP/1.1",
                       "wsgi.multiprocess": False,
                       "wsgi.multithread": False,
                       "wsgi.run_once": False,
                       "wsgi.url_scheme": 'http',
                       "wsgi.version": (1, 0)}

    def cleanup(self):
        mvc.CONN_MANAGER = None

    def test_convert_request_ok(self):
        '''Test case that ensuring that request conversion works as expected.'''

        uuid_generator = lambda: 1

        self._middleware(self._environ, self._start_response, uuid_generator=uuid_generator)

        request = self._environ.get("fantastico.request")

        self.assertIsNotNone(request)
        self.assertEqual(1, request.request_id)
        self.assertEqual("GET", request.method)
        self.assertEqual("http", request.scheme)
        self.assertEqual("", request.script_name)
        self.assertEqual("/article", request.path_info)
        self.assertEqual("localhost:80", request.host)
        self.assertTrue("application/json" in request.accept)
        self.assertEqual("application/json", request.content_type)
        self.assertEqual("123", request.headers.get("oauth_bearer"))
        self.assertEqual(1, int(request.params.get("id")))

    def test_context_settings_initialized(self):
        '''Test case that ensures settings is binded to the request context.'''

        self._middleware(self._environ, self._start_response)

        old_settings = os.environ.get("FANTASTICO_ACTIVE_CONFIG") or ""
        os.environ["FANTASTICO_ACTIVE_CONFIG"] = "fantastico.settings.BasicSettings"

        try:
            request = self._environ.get("fantastico.request")
            context = getattr(request, "context")

            self.assertIsNotNone(context)
            self.assertEqual(BasicSettings().installed_middleware, context.settings.get("installed_middleware"))
        finally:
            os.environ["FANTASTICO_ACTIVE_CONFIG"] = old_settings

    def test_context_language_detected(self):
        '''Test case that ensures language is detected correctly based on provided Accept-Language header. This is an exact matching
        when language is in format <langcode>-<countrycode>.'''

        self._middleware(self._environ, self._start_response)

        request = self._environ.get("fantastico.request")
        context = getattr(request, "context")

        self.assertIsNotNone(context)
        self.assertIsNotNone(context.language)
        self.assertEqual("en_us", str(context.language))

    def test_context_language_detected_by_langcode(self):
        '''Test case that ensures language is detected correctly based on provide Accept-Language header when languages listed
        contain only langcode: E.g: en'''

        self._environ["HTTP_ACCEPT_LANGUAGE"] = "ro,en;q=0.8"

        self._middleware(self._environ, self._start_response)

        request = self._environ.get("fantastico.request")
        context = getattr(request, "context")

        self.assertIsNotNone(context)
        self.assertIsNotNone(context.language)
        self.assertEqual("en_us", str(context.language))

    def test_context_language_default_detected(self):
        '''Test case that ensures request response middleware can successfully detect language even when Accept-Language header
        is not sent.'''

        del self._environ["HTTP_ACCEPT_LANGUAGE"]

        self._middleware(self._environ, self._start_response)

        request = self._environ.get("fantastico.request")
        context = getattr(request, "context")

        self.assertIsNotNone(context)
        self.assertIsNotNone(context.language)
        self.assertEqual("en_us", str(context.language))

    def test_connection_closed(self):
        '''This test case ensures connection is closed once the request is done.'''

        conn_manager = Mock()

        mvc.CONN_MANAGER = conn_manager

        def close(request_id):
            raise ValueError("Connection closed.")

        conn_manager.close_connection = close

        with self.assertRaises(ValueError) as cm:
            self._middleware(self._environ, self._start_response)

        self.assertEqual("Connection closed.", str(cm.exception))

    def test_redirect_appended(self):
        '''This test case ensures redirect method is correctly appended to the current request.'''

        self._middleware(self._environ, self._start_response)

        request = self._environ.get("fantastico.request")

        self.assertIsNotNone(request)
        self.assertIsInstance(request.redirect("/simple/test"), RedirectResponse)
