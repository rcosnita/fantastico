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

.. py:module:: fantastico.middleware.tests.test_request_context
'''
from fantastico.middleware.request_context import RequestContext
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock

class RequestContextTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for request context which ensures the class follows the expected requirements.'''

    def test_request_context_init_ok(self):
        '''This test case ensures the initializing of the component works as expected.'''

        expected_settings = Mock()
        expected_language = Mock()

        context = RequestContext(expected_settings, expected_language)

        self.assertEqual(expected_settings, context.settings)
        self.assertEqual(expected_language, context.language)
        self.assertIsNone(context.wsgi_app)

    def test_request_wsgi_app_inject(self):
        '''This test case ensures wsgi_app can be injected into an existing request context instance.'''

        expected_app = Mock()

        context = RequestContext(None, None)
        context.wsgi_app = expected_app

        self.assertIsNone(context.settings)
        self.assertIsNone(context.language)
        self.assertEqual(expected_app, context.wsgi_app)
