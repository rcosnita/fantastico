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
.. py:module:: fantastico.middleware.tests.itest_model_session_middleware
'''
from fantastico import mvc
from fantastico.middleware.model_session_middleware import ModelSessionMiddleware
from fantastico.tests.base_case import FantasticoIntegrationTestCase
from mock import Mock

class ModelSessionMiddlewareIntegration(FantasticoIntegrationTestCase):
    '''This class provides the test cases for model session middleware.'''

    _environ = None
    _normal_response = None
    _app = None
    _middleware = None

    def init(self):
        self._environ = {}
        self._normal_response = Mock()
        self._app = Mock(return_value=self._normal_response)
        self._middleware = ModelSessionMiddleware(self._app)
        mvc.CONN_MANAGER = None

    def test_session_init_ok(self):
        '''This test case ensures an active db session is opened by model session middleware.'''

        self.assertIsNone(mvc.CONN_MANAGER)

        response = self._middleware(self._environ, Mock())

        self.assertEqual(self._normal_response, response)
        self.assertIsNotNone(mvc.CONN_MANAGER)
