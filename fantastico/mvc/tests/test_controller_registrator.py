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

from fantastico import settings
from fantastico.mvc import controller_decorators
from fantastico.tests.base_case import FantasticoUnitTestsCase
from fantastico.utils import instantiator
from mock import Mock

class ControllerRouteLoaderTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for ensuring routes are correctly registered using Controller decorator.'''

    @classmethod
    def setup_once(cls):
        '''We rebind original Controller decorator to its module.'''

        super(ControllerRouteLoaderTests, cls).setup_once()

        controller_decorators.Controller = cls._old_controller_decorator

    def init(self):
        from fantastico.mvc.controller_registrator import ControllerRouteLoader

        self._settings_facade = Mock()
        self._settings_facade.get_config = Mock(return_value=settings.BasicSettings())
        self._settings_facade.get = Mock(return_value=["fantastico.locale"])

        self._route_loader = ControllerRouteLoader(settings_facade=self._settings_facade,
                                                   scanned_folder=instantiator.get_class_abslocation(ControllerRouteLoaderTests))

        self._settings_facade.get.assert_called_once_with("mvc_additional_paths")

    def test_route_loading_ok(self):
        '''Test case that ensure routes mapped through Controller decorator are registered ok. It also makes sure
        subfolders are scanned and registered if necessary.'''

        routes = self._route_loader.load_routes()

        self.assertIsNotNone(routes)

        self.assertEqual("fantastico.mvc.tests.routes_for_testing.RoutesForControllerTesting.say_hello",
                         routes.get("/say_hello")["http_verbs"]["GET"])

        self.assertEqual("fantastico.mvc.tests.routes_for_testing.RoutesForControllerTesting.upload_file",
                         routes.get("/upload_file")["http_verbs"]["POST"])

        self.assertEqual("fantastico.mvc.tests.subroutes.subroutes_controller.SubroutesController.handle_route",
                         routes.get("/route_from_subfolder")["http_verbs"]["GET"])

    def test_scanned_folder_custom(self):
        '''This test case ensures scanned folder is correctly detected based on active config.'''

        from fantastico.mvc.controller_registrator import ControllerRouteLoader

        settings_facade = Mock()
        settings_facade.get_config = Mock(return_value=TestProfileNotUsed())
        settings_facade.get = Mock(return_value=[])

        loader = ControllerRouteLoader(settings_facade)

        self.assertTrue(loader.scanned_folders[0].endswith("fantastico/mvc/tests/"))

class TestProfileNotUsed(settings.BasicSettings):
    '''This profile is used for testing purposes only.'''
