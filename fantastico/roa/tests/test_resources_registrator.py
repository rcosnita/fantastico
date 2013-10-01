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
from fantastico.settings import SettingsFacade
from fantastico.tests.base_case import FantasticoUnitTestsCase
from fantastico.utils import instantiator
from fantastico.roa.resources_registry import ResourcesRegistry

class ResourcesRegistratorTest(FantasticoUnitTestsCase):
    '''This class provides the test cases for resources registration algorithm.'''


    def cleanup(self):
        '''This method cleanup all affected dependencies.'''

        ResourcesRegistry.AVAILABLE_RESOURCES.clear()
        ResourcesRegistry.AVAILABLE_URL_RESOURCES.clear()

    def test_registration_ok(self):
        '''This test case ensures all resources are registered correctly.'''

        registrator = ResourcesRegistrator(file_patterns=["simple_resource.py"])

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
