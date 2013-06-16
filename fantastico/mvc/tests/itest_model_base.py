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
.. py:module:: fantastico.mvc.tests.itest_model_base
'''
from fantastico.settings import SettingsFacade
from fantastico.tests.base_case import FantasticoIntegrationTestCase
import uuid

class BaseModelIntegration(FantasticoIntegrationTestCase):
    '''This class provides the test cases that ensures sql alchemy configuration works as expected.'''
    
    def init(self):
        self._settings_facade = SettingsFacade()
    
    def test_connection_ok(self):
        '''This test case execute a simple sanity check against database configuration.'''
        
        db_config = self._settings_facade.get("database_config")
        
        from fantastico import mvc
        
        mvc.init_dm_db_engine(db_config)
        
        self.assertIsNotNone(mvc.BASEMODEL)
        self.assertIsNotNone(mvc.CONN_MANAGER)
        
        session = mvc.CONN_MANAGER.get_connection(uuid.uuid4())
        
        session.execute("SELECT 1")