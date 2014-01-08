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

.. py:module:: fantastico.tests.test_settings
'''

from fantastico.exceptions import FantasticoClassNotFoundError, \
    FantasticoSettingNotFoundError
from fantastico.settings import SettingsFacade, BasicSettings
from fantastico.tests.base_case import FantasticoUnitTestsCase

class SampleSettings(BasicSettings):
    '''Just a simple settings implementation for testing purposes.'''

    @property
    def installed_middleware(self):
        raise Exception("Internal error")

class TestSettingsFacadeSuite(FantasticoUnitTestsCase):
    '''Test suite for settings facade functionality.'''

    def init(self):
        self._environ = {}
        self._settings = SettingsFacade(self._environ)

    def test_get_config_noenv(self):
        '''Test case that checks a settings class can be obtained even if FANTASTICO_ACTIVE_CONFIG environment variable
        is not found.'''

        self.assertIsInstance(self._settings.get_config(), BasicSettings)

    def test_get_config_env_notfound(self):
        '''Test case that checks an exception is thrown when the specified class config can not be resolved.'''

        self._environ["FANTASTICO_ACTIVE_CONFIG"] = "not.found.class"

        self.assertRaises(FantasticoClassNotFoundError, self._settings.get_config)

    def test_get_config_env_found(self):
        '''Test case that checks that a custom configuration is instantiated correctly.'''

        self._environ["FANTASTICO_ACTIVE_CONFIG"] = "fantastico.tests.test_settings.SampleSettings"

        self.assertIsInstance(self._settings.get_config(), SampleSettings)

    def test_get_setting(self):
        '''Test case that checks settings are correctly retrieved from the active configuration. In addition
        it ensures the configuration contains the minimum amount of information for installed_middleware.'''

        installed_middleware = self._settings.get("installed_middleware")

        self.assertGreaterEqual(len(installed_middleware), 3)
        self.assertEqual(["fantastico.middleware.request_middleware.RequestMiddleware",
                          "fantastico.middleware.model_session_middleware.ModelSessionMiddleware",
                          "fantastico.middleware.routing_middleware.RoutingMiddleware",
                          "fantastico.oauth2.middleware.exceptions_middleware.OAuth2ExceptionsMiddleware",
                          "fantastico.oauth2.middleware.tokens_middleware.OAuth2TokensMiddleware"], installed_middleware)

    def test_get_setting_unavailable(self):
        '''Test case that ensures an exception is thrown whenever we try to get a setting that is not
        available.'''

        self.assertRaises(FantasticoSettingNotFoundError, self._settings.get, *["setting_not_found"])

    def test_get_setting_internal_error(self):
        '''Test case that ensures properties internal server errors are handled gracefully.'''

        self._environ["FANTASTICO_ACTIVE_CONFIG"] = "fantastico.tests.test_settings.SampleSettings"

        self.assertRaises(FantasticoSettingNotFoundError, self._settings.get, *["installed_middleware"])

    def test_get_root_folder(self):
        '''Test case that ensures get root folder works correctly.'''

        self._environ["FANTASTICO_ACTIVE_CONFIG"] = "fantastico.settings.BasicSettings"

        expected_root = self._get_root_folder()

        root_folder = self._settings.get_root_folder()

        self.assertEqual(expected_root, root_folder)
