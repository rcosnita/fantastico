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
.. py:module:: fantastico.server.tests.test_dev_server
'''
from fantastico.server.dev_server import DevServer
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock

class DevServerTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for making sure dev server class works.'''
    
    def init(self):
        self._settings_facade = Mock()
        self._settings_facade.get = self._get_server_key
        self._settings_facade_cls = Mock(return_value=self._settings_facade)
        self._server = DevServer(self._settings_facade_cls)
    
    def _get_server_key(self, key):
        if key == "dev_server_port":
            return 12000
        
        if key == "dev_server_host":
            return "localhost"
    
    def test_start_ok(self):
        '''This test case ensures development server starts ok scenario.'''
        
        make_server = Mock()
        app = Mock()
        
        self._server.start(make_server, app)
        
        self.assertEqual("localhost", self._server.hostname)
        self.assertEqual(12000, self._server.port)
        self.assertTrue(self._server.started)
        
    def test_start_error(self):
        '''This test case ensures development server does not start if an exception is raised by make_server or 
        app parameters.'''
        
        inputs = [(Mock(side_effect=Exception("Error make_server")), Mock(), "Error make_server"),
                  (Mock(), Mock(side_effect=Exception("Error app")), "Error app")]
        
        for make_server, app, expected_msg in inputs:
            with self.assertRaises(Exception) as cm: 
                self._server.start(make_server, app)
                
            self.assertTrue(str(cm.exception).find(expected_msg) > -1)
            
    def test_stop_server_notstarted(self):
        '''This test case makes sure stop method does not crash when dev server was not started.'''
        
        self._server.stop()
        
        self.assertFalse(self._server.started)
        
    def test_stop_server_whenstarted(self):
        '''This test case makes sure stop method correctly shutdowns a running dev server.'''
        
        self._shutdown_invoked = False
                
        def fake_shutdown():
            self._shutdown_invoked = True
        
        http_server = Mock()
        http_server.shutdown = fake_shutdown
        make_server = Mock(return_value=http_server) 
        app = Mock()
        
        self._server.start(make_server, app)
        
        self._server.stop()
        
        self.assertTrue(self._shutdown_invoked)
        self.assertFalse(self._server.started)        