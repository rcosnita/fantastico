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
.. py:module:: fantastico.roa.tests.test_resources_registrator
'''

from fantastico.roa.resources_registrator import ResourcesRegistrator
from fantastico.roa.resources_registry import ResourcesRegistry
from fantastico.settings import SettingsFacade
from fantastico.tests.base_case import FantasticoUnitTestsCase
from fantastico.utils import instantiator
from mock import Mock

class ResourcesRegistratorTest(FantasticoUnitTestsCase):
    '''This class provides the test cases for resources registration algorithm.'''

    def init(self):
        '''This method ensures registry is empty before each test case.'''

        registry = ResourcesRegistry()
        registry.available_resources.clear()
        registry.available_url_resources.clear()

    def cleanup(self):
        '''This method cleanup all affected dependencies.'''

        registry = ResourcesRegistry()
        registry.available_resources.clear()
        registry.available_url_resources.clear()

    def test_registration_ok(self):
        '''This test case ensures all resources are registered correctly.'''

        registrator = ResourcesRegistrator(Mock(), file_patterns=["simple_resource.py"], folder_pattern=["tests/"])

        root_folder = instantiator.get_class_abslocation(SettingsFacade)

        registrator.register_resources(root_folder)

        registry = ResourcesRegistry()
        resource = registry.find_by_name("Simple Resource")

        self.assertIsNotNone(resource)
        self.assertEqual(resource.name, "Simple Resource")
        self.assertEqual(resource.version, 1.0)
        self.assertEqual(resource.url, "/simple-resources")
        self.assertEqual(resource.subresources, {"address": ["address_id"]})

        model = resource.model

        self.assertIsNotNone(model)

        from fantastico.roa.tests.simple_resource import SimpleResource

        self.assertEqual(model, SimpleResource)

    def test_loadroutes_ok(self):
        '''This test case ensures loadroutes method first scans all files for resources and then returns an empty dictionary
        of routes.'''

        expected_path = instantiator.get_class_abslocation(self.__class__)

        settings_facade = Mock()
        settings_facade.get_config = lambda: self

        registrator = ResourcesRegistrator(settings_facade)

        registrator.register_resources = Mock()

        self.assertEqual(registrator.load_routes(), {})

        registrator.register_resources.assert_called_once_with(expected_path)
