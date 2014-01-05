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
.. py:module:: fantastico.oauth2.tests.test_oauth2_controller
'''
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from fantastico.oauth2.exceptions import OAuth2MissingQueryParamError

class OAuth2ControllerTests(FantasticoUnitTestsCase):
    '''This class provides tests suite for oauth 2 controller.'''

    _settings_facade = None
    _handlers_factory = None
    _oauth2_controller = None

    def init(self):
        '''This method is invoked automatically in order to set common dependencies for all test cases.'''

        from fantastico.oauth2.oauth2_controller import OAuth2Controller

        self._settings_facade = Mock()

        self._handlers_factory = Mock()
        handler_factory_cls = Mock(return_value=self._handlers_factory)

        self._oauth2_controller = OAuth2Controller(self._settings_facade, handler_factory_cls=handler_factory_cls)

        handler_factory_cls.assert_called_once_with()

    def test_authorize_supported_grant_ok(self):
        '''This test case ensures authorize works as expected for a supported grant type.'''

        self._test_authorize_template()

    def test_authorize_grant_factory_ex(self):
        '''This test case ensures grant factory exceptions are bubbled up.'''

        factory_ex = Exception("Unexpected factory exception.")

        with self.assertRaises(Exception) as ctx:
            self._test_authorize_template(factory_ex=factory_ex)

        self.assertEqual(factory_ex, ctx.exception)

    def test_authorize_responsetype_missing(self):
        '''This test case ensures a query parameter missing exception is raised when response_type is missing.'''

        with self.assertRaises(OAuth2MissingQueryParamError) as ctx:
            self._test_authorize_template(response_type=None)

        self.assertEqual("response_type", ctx.exception.param_name)

    def test_authorize_grant_handler_ex(self):
        '''This test case ensures grant handler exceptions are bubbled up.'''

        handler_ex = Exception("Unexpected factory exception.")

        with self.assertRaises(Exception) as ctx:
            self._test_authorize_template(handler_ex=handler_ex)

        self.assertEqual(handler_ex, ctx.exception)

    def _test_authorize_template(self, response_type="supported_grant", factory_ex=None, handler_ex=None):
        '''This method provides a template method for testing handle_authorize method from oauth2 controller.'''

        expected_response = Mock()

        client_facade = Mock()
        client_facade.session = Mock()

        request = Mock()
        request.params = {"response_type": response_type}

        request.models = Mock()
        request.models.Client = client_facade

        grant_handler = Mock()

        if not handler_ex:
            grant_handler.handle_grant = Mock(return_value=expected_response)
        else:
            grant_handler.handle_grant = Mock(side_effect=handler_ex)

        if not factory_ex:
            self._handlers_factory.get_handler = Mock(return_value=grant_handler)
        else:
            self._handlers_factory.get_handler = Mock(side_effect=factory_ex)

        response = self._oauth2_controller.handle_authorize(request)

        self.assertEqual(expected_response, response)

        self._handlers_factory.get_handler.assert_called_once_with("supported_grant", client_facade.session)
        grant_handler.handle_grant.assert_called_once_with(request)
