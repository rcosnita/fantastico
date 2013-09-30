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
.. py:module:: fantastico.roa.tests.test_resource_decorator
'''
from fantastico.roa.resource_decorator import Resource
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock

class ResourceDecoratorTests(FantasticoUnitTestsCase):
    '''This class provides test cases for resource decorator @Resource.'''

    def test_check_instantiation(self):
        '''This test case ensures resource instantiation work as expected (with and without explicit values).'''

        expected_name = "app-setting"
        expected_url = "/app-settings"
        expected_version = 1.0
        expected_subresources = {"default_address": ["default_address_id"]}

        resource = Resource(name=expected_name, url=expected_url, subresources=expected_subresources)
        resource_explicit = Resource(name=expected_name, url=expected_url, version=expected_version)

        self.assertEqual(resource.name, resource_explicit.name)
        self.assertEqual(resource.url, resource_explicit.url)
        self.assertEqual(resource.version, resource_explicit.version)
        self.assertEqual(resource.model, resource_explicit.model)

        self.assertEqual(resource.name, expected_name)
        self.assertEqual(resource.url, expected_url)
        self.assertEqual(resource.version, expected_version)
        self.assertEqual(resource.subresources, expected_subresources)
        self.assertIsNone(resource.model)

    def test_check_call(self):
        '''This test case ensures call method correctly registers a resource to a given resource.'''

        expected_name = "app-setting"
        expected_url = "/app-settings"

        registry = Mock()
        model = Mock()

        resource = Resource(name=expected_name, url=expected_url)

        self.assertEqual(resource(model, resources_registry=registry), model)

        self.assertEqual(resource.name, expected_name)
        self.assertEqual(resource.url, expected_url)
        self.assertEqual(resource.version, 1.0)
        self.assertEqual(resource.model, model)

        registry.register_resource.assert_called_once_with(resource)
