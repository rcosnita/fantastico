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
.. py:module:: fantastico.roa.tests.test_resources_registry
'''
from fantastico.roa.resource_decorator import Resource
from fantastico.roa.resources_registry import ResourcesRegistry
from fantastico.roa.roa_exceptions import FantasticoRoaDuplicateError
from fantastico.tests.base_case import FantasticoUnitTestsCase

class ResourcesRegistryTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for resources registry.'''

    def cleanup(self):
        '''This method cleanup all affected dependencies after each test case.'''

        ResourcesRegistry.AVAILABLE_RESOURCES.clear()
        ResourcesRegistry.AVAILABLE_URL_RESOURCES.clear()

    def _register_resource_duplicate(self, resource1, resource2):
        '''This method executes register resource test case for duplicate exception.'''

        registry = ResourcesRegistry()

        registry.register_resource(resource1)

        with self.assertRaises(FantasticoRoaDuplicateError):
            registry.register_resource(resource2)

    def test_register_resource_duplicate_nameversion(self):
        '''This test case ensures an exception is raised when we try to register multiple resources with the same name and
        version.'''

        resource = Resource(name="app-setting", url="/app-settings")

        self._register_resource_duplicate(resource, resource)

    def test_register_resource_duplicate_url(self):
        '''This test case ensures different resources can not be registered under the same name.'''

        resource1 = Resource(name="app-setting", url="/app-settings")
        resource2 = Resource(name="custom-setting", url="/app-settings")

        self._register_resource_duplicate(resource1, resource2)
