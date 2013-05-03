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

.. py:module:: fantastico.routing_engine.tests.test_dummy_routeloader
'''
from fantastico.routing_engine.dummy_routeloader import DummyRouteLoader
from fantastico.tests.base_case import FantasticoIntegrationTestCase
from mock import Mock

class TestDummyRouteLoader(FantasticoIntegrationTestCase):
    '''Test suite that ensures dummy route loader works as expected.'''
    
    def init(self):
        self._dummy_loader = DummyRouteLoader(Mock())
    
    def test_load_routes_ok(self):
        '''Test case that ensures only one route is loaded by this dummy route loader.'''
        
        routes = self._dummy_loader.load_routes()
        
        self.assertIsNotNone(routes)
        self.assertEqual(1, len(routes))
        self.assertTrue(DummyRouteLoader.DUMMY_ROUTE in routes)
        self.assertEqual("fantastico.routing_engine.dummy_routeloader.DummyRouteLoader.display_test",
                         routes["/dummy/route/loader/test"])