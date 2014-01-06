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
.. py:module:: fantastico.oauth2.tests.test_granthandler_factory
'''

from fantastico.oauth2.exceptions import OAuth2UnsupportedGrantError
from fantastico.oauth2.grant_handler_factory import GrantHandlerFactory
from fantastico.oauth2.implicit_grant_handler import ImplicitGrantHandler
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock

class GrantHandlerFactoryTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for supported handlers factory.'''

    _tokens_service = None
    _tokens_service_cls = None
    _settings_facade = None
    _factory = None

    def init(self):
        '''This method is invoked automatically in order to setup common dependencies for all test cases.'''

        self._tokens_service = Mock()
        self._tokens_service_cls = Mock(return_value=self._tokens_service)

        self._settings_facade = Mock()

        settings_facade_cls = Mock(return_value=self._settings_facade)
        self._settings_facade.get = self._mock_get_setting

        self._factory = GrantHandlerFactory(tokens_service_cls=self._tokens_service_cls, settings_facade_cls=settings_facade_cls)

        settings_facade_cls.assert_called_once_with()

    def _mock_get_setting(self, setting_name):
        '''This method mocks get from settings_facade instance.'''

        if setting_name == "oauth2_idp":
            return {"idp_index": "/oauth/idp/ui/login"}

        return Mock()

    def test_get_handler_ok(self):
        '''This test case ensures a correct instance of a grant handler can be obtained using the factory.'''

        db_conn = Mock()

        grant_handler = self._factory.get_handler(GrantHandlerFactory.IMPLICIT_GRANT, db_conn)

        self.assertIsInstance(grant_handler, ImplicitGrantHandler)

        self._tokens_service_cls.assert_called_once_with(db_conn)

    def test_get_handler_unsupported(self):
        '''This test case ensures a concrete oauth2 exception is raised if a handler_type is not supported.'''

        db_conn = Mock()
        handler_type = "unsupported"

        with self.assertRaises(OAuth2UnsupportedGrantError) as ctx:
            self._factory.get_handler(handler_type, db_conn)

        self.assertEqual(handler_type, ctx.exception.handler_type)
