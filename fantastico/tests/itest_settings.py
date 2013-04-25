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
from fantastico.settings import SettingsFacade, BasicSettings
import os
import unittest

class SettingsIntegration(unittest.TestCase):
    '''Test suite that ensures current settings for various environments remain stable.'''
    
    def setUp(self):
        self._envs = [("fantastico.settings.BasicSettings", BasicSettings)]
        self._settings_facade = SettingsFacade() 
    
    def test_settings_ok(self):
        '''Test case that ensures settings are functional for each environment available.'''
        
        old_env = os.environ.get("FANTASTICO_ACTIVE_CONFIG")
        
        for env, settings_cls in self._envs:
            try:
                os.environ["FANTASTICO_ACTIVE_CONFIG"] = env
                
                self.assertIsInstance(self._settings_facade.get_config(), settings_cls)
                
                self.assertEqual(["fantastico.middleware.RequestMiddleware", "fantastico.middleware.RoutingEngineMiddleware"], 
                                  self._settings_facade.get("installed_middleware"))
                
                self.assertEqual(["en_us"], self._settings_facade.get("supported_languages"))
            finally:
                if old_env is not None:
                    os.environ["FANTASTICO_ACTIVE_CONFIG"] = old_env