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
.. py:module:: fantastico.contrib.roa_discovery.tests.test_discovery_controller
'''

from fantastico.roa.resource_decorator import Resource
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
import json

class RoaDiscoveryControllerTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for roa discovery controller.'''

    _settings_facade = None
    _registry = None
    _registry_cls = None
    _discovery_ctrl = None

    def init(self):
        '''This test case create a mocked discovery controller.'''

        self._settings_facade = Mock()
        self._registry = Mock()
        self._registry_cls = Mock(return_value=self._registry)

    def _test_resources_listing(self, roa_api):
        '''This method execute resources listing success scenario. It assers generated urls agains a given roa_api.'''

        self._settings_facade.get = Mock(return_value=roa_api)

        from fantastico.contrib.roa_discovery.discovery_controller import RoaDiscoveryController

        self._discovery_ctrl = RoaDiscoveryController(self._settings_facade, self._registry_cls)

        self._registry.all_resources = lambda: [Resource(name="Person", url="/persons", version=1.0),
                                                Resource(name="Person", url="/persons", version=1.0),
                                                Resource(name="Address", url="/addresses", version=1.0),
                                                Resource(name="Address", url="/addresses", version=2.0),
                                                Resource(name="Address", url="/addresses", version=2.0)]

        response = self._discovery_ctrl.list_registered_resources(Mock())

        self.assertIsNotNone(response)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.charset, "UTF-8")

        resources = json.loads(response.body.decode())

        self.assertIsNotNone(resources)

        self.assertEqual(resources["Person"]["1.0"], "%s/1.0/persons" % roa_api)
        self.assertEqual(resources["Person"]["latest"], "%s/latest/persons" % roa_api)

        self.assertEqual(resources["Address"]["1.0"], "%s/1.0/addresses" % roa_api)
        self.assertEqual(resources["Address"]["2.0"], "%s/2.0/addresses" % roa_api)
        self.assertEqual(resources["Address"]["latest"], "%s/latest/addresses" % roa_api)

        self._registry_cls.assert_called_once_with()
        self._settings_facade.get.assert_called_once_with("roa_api")

    def test_resources_listing_samedomain_ok(self):
        '''This test case ensures resources are correctly listed from a given registry when apis are mapped on the same
        domain.'''

        self._test_resources_listing("/api")

    def test_resources_listing_cors_ok(self):
        '''This test case ensures resources are correctly listed from a given registry when apis are mapped on a different
        domain.'''

        self._test_resources_listing("http://roa.fantasticoproject.com")

    def test_discovery_controller_defaultregistry(self):
        '''This test case ensures controller can be instantiated without specifying a registry. It also make sure that exceptions
        are bubbled up from registry instantiation.'''

        from fantastico.roa import resources_registry

        expected_ex = Exception("Unexpected error")

        old_registry_cls = resources_registry.ResourcesRegistry
        new_registry_cls = Mock(side_effect=expected_ex)
        resources_registry.ResourcesRegistry = new_registry_cls

        from fantastico.contrib.roa_discovery.discovery_controller import RoaDiscoveryController

        try:
            with self.assertRaises(Exception) as ctx:
                RoaDiscoveryController(Mock())

            self.assertEqual(ctx.exception, expected_ex)
        finally:
            resources_registry.ResourcesRegistry = old_registry_cls
