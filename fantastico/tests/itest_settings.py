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

.. py:module:: fantastico.tests.itest_settings
'''
from fantastico.exceptions import FantasticoSettingNotFoundError
from fantastico.settings import SettingsFacade
from fantastico.tests.base_case import FantasticoIntegrationTestCase
import os

class SettingsIntegration(FantasticoIntegrationTestCase):
    '''Test suite that ensures current settings for various environments remain stable.'''
    
    def init(self):
        self._settings_facade = SettingsFacade() 
    
    def test_settings_ok(self):
        '''Test case that ensures settings are functional for each environment available.'''
        
        def exec_test(env, settings_cls):
            os.environ["FANTASTICO_ACTIVE_CONFIG"] = env
            
            self.assertIsInstance(self._settings_facade.get_config(), settings_cls)
            
            self.assertEqual(["fantastico.middleware.RequestMiddleware", "fantastico.middleware.RoutingEngineMiddleware"], 
                              self._settings_facade.get("installed_middleware"))
            
            self.assertEqual(["en_us"], self._settings_facade.get("supported_languages"))
            
        self._run_test_all_envs(exec_test)
                    
    def test_settings_invalid_ok(self):
        '''Test case that ensures settings exception cases raise strong type exception.'''
        
        def exec_test(env, settings_cls):
            os.environ["FANTASTICO_ACTIVE_CONFIG"] = "not.found.package"
            
            self.assertRaises(FantasticoSettingNotFoundError, self._settings_facade.get, *["not_found_attr_1234"])
            
            os.environ["FANTASTICO_ACTIVE_CONFIG"] = self._envs[0][0]
                        
            self.assertRaises(FantasticoSettingNotFoundError, self._settings_facade.get, *["not_found_attr_1234"])
        
        self._run_test_all_envs(exec_test)