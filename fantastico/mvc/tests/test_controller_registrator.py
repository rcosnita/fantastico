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
.. py:module:: fantastico.mvc.tests.itest_controller_registrator
'''

from fantastico.mvc.controller_registrator import ControllerRouteLoader
from fantastico.tests.base_case import FantasticoIntegrationTestCase
from fantastico.utils import instantiator
from mock import Mock

class ControllerRouteLoaderTests(FantasticoIntegrationTestCase):
    '''This class provides the test cases for ensuring routes are correctly registered using Controller decorator.'''
    
    def init(self):        
        self._settings_facade = Mock()
        self._settings_facade_cls = Mock(return_value=self._settings_facade)
        
        self._route_loader = ControllerRouteLoader(settings_facade=self._settings_facade_cls, 
                                                   scanned_folder=instantiator.get_class_abslocation(ControllerRouteLoaderTests))
        
    def test_route_loading_ok(self):
        '''Test case that ensure routes mapped through Controller decorator are registered ok. It also makes sure
        subfolders are scanned and registered if necessary.'''
        
        routes = self._route_loader.load_routes()
        
        self.assertIsNotNone(routes)

        self.assertEqual("fantastico.mvc.tests.routes_for_testing.RoutesForControllerTesting.say_hello", 
                         routes.get("/say_hello")["method"])
        self.assertEqual(["GET"], routes.get("/say_hello")["http_verbs"])

        self.assertEqual("fantastico.mvc.tests.routes_for_testing.RoutesForControllerTesting.upload_file",
                         routes.get("/upload_file")["method"])
        self.assertEqual(["POST"], routes.get("/upload_file")["http_verbs"])
        
        self.assertEqual("fantastico.mvc.tests.subroutes.subroutes_controller.SubroutesController.handle_route",
                         routes.get("/route_from_subfolder")["method"])
        self.assertEqual(["GET"], routes.get("/route_from_subfolder")["http_verbs"])