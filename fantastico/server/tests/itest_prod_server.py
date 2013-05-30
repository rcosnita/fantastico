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
.. py:module:: fantastico.server.tests.itest_prod_server
'''

from fantastico.tests.base_case import FantasticoIntegrationTestCase
from fantastico.utils import instantiator
from subprocess import Popen
from urllib.request import Request
import os
import socket
import subprocess
import threading
import time
import urllib

class ProdServerIntegration(FantasticoIntegrationTestCase):
    '''This class provides the test case for fantastico production server placed behind nginx.'''
    
    MAX_RUN_TIMEOUT = 2
    
    def init(self):
        self._server_proc = None
    
    def _is_port_opened(self, ip, port):
        '''This method determines if a given port is opened or not.'''
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            s.connect((ip, int(port)))
            s.shutdown(2)
            
            return True
        except:
            return False
    
    def test_requests_handled_ok(self):
        '''This test case ensures requests are handled correctly by nginx.'''
        
        
        def start_server():
            root_folder = os.path.realpath(instantiator.get_class_abslocation(ProdServerIntegration) + "/../../../") + "/"
            start_prod_server = ["%srun_prod_server.sh" % root_folder]

            self._server_proc = Popen(start_prod_server, cwd=root_folder, env=os.environ,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self._server_proc.communicate()
                                
        server_thread = threading.Thread(target=start_server)
        server_thread.start()
        
        timeout = 0
        
        while not self._is_port_opened("127.0.0.1", "12090") and timeout <= ProdServerIntegration.MAX_RUN_TIMEOUT:
            timeout += 0.2
            time.sleep(0.2)

        try:
            if timeout >= 2:
                self.assertTrue(False, "Unable to run wsgi prod instance in %s seconds." % ProdServerIntegration.MAX_RUN_TIMEOUT)
            else:
                request = Request("http://fantastico-framework.com/mvc/hello-world") 
                response = urllib.request.urlopen(request)
            
                self.assertEqual(200, response.code)
        finally:
            self._server_proc.terminate()
            
            Popen(["/usr/bin/killall", "-9", "uwsgi"], env=os.environ).communicate()