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
.. py:module:: fantastico.server.prod_server
'''

from fantastico.middleware.fantastico_app import FantasticoApp
import threading

class WsgiFantasticoStarter(object):
    '''This class is a wrapper used to start fantastico production server.'''
    
    def __init__(self):
        self._fantastico = None
        self._instantiator_lock = None
    
    def __call__(self, environ, start_response):
        if self._fantastico is None:
            if not self._instantiator_lock:
                self._instantiator_lock = threading.Lock()
                self._instantiator_lock.acquire()
                
                self._fantastico = FantasticoApp()
                
                self._instantiator_lock.release()
            else:
                self._instantiator_lock.acquire()
        
        return self._fantastico(environ, start_response)
    
application = WsgiFantasticoStarter()