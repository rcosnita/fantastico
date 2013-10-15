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
.. py:module:: fantastico.contrib.roa_discovery.tests.test_roa_controller
'''

from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
import json

class RoaControllerTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for roa controller.'''

    _settings_facade = None
    _resources_registry = None
    _model_facade = None
    _conn_manager = None
    _json_serializer_cls = None
    _json_serializer = None
    _controller = None

    def init(self):
        '''This method setup all test cases common dependencies.'''

        from fantastico.contrib.roa_discovery.roa_controller import RoaController

        self._settings_facade = Mock()
        self._resources_registry = Mock()
        self._model_facade = Mock()
        self._conn_manager = Mock()
        self._json_serializer = Mock()

        resources_registry_cls = Mock(return_value=self._resources_registry)
        model_facade_cls = Mock(return_value=self._model_facade)
        self._json_serializer_cls = Mock(return_value=self._json_serializer)

        self._settings_facade = Mock(return_value=self._settings_facade)

        self._controller = RoaController(settings_facade=self._settings_facade,
                                         resources_registry_cls=resources_registry_cls,
                                         model_facade_cls=model_facade_cls,
                                         conn_manager=self._conn_manager,
                                         json_serializer_cls=self._json_serializer_cls)

    def _mock_model_facade(self, records, records_count):
        '''This method mocks the current model facade object in order to return the specified values.'''

        self._model_facade.get_records_paged = Mock(return_value=records)
        self._model_facade.count_records = Mock(return_value=records_count)

    def _assert_get_collection_response(self, response, records, records_count, offset, limit):
        '''This test case assert the given response against expected values.'''

        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.content_type)

        self.assertIsNotNone(response.body)

        body = json.loads(response.body.decode())

        self.assertEqual(len(records), len(body["items"]))
        self.assertEqual(records_count, body["totalItems"])

        self._model_facade.get_records_paged.assert_called_once_with(start_record=offset, end_record=limit)
        self._model_facade.count_records.assert_called_once_with()

    def test_get_collection_default_values_emptyresult(self):
        '''This test case ensures get collection works as expected without any query parameters passed. It ensures
        empty items returns correct '''

        expected_records = []
        expected_records_count = 0

        version = "1.0"
        resource_url = "/sample-resources"

        request = Mock()
        request.params = {}

        resource = Mock()
        resource.model = Mock()

        self._mock_model_facade(records=expected_records, records_count=expected_records_count)

        self._resources_registry.find_by_url = Mock(return_value=resource)

        response = self._controller.get_collection(request, version, resource_url)

        self._assert_get_collection_response(response,
                                             records=expected_records,
                                             records_count=expected_records_count,
                                             offset=self._controller.OFFSET_DEFAULT,
                                             limit=self._controller.LIMIT_DEFAULT)

        self._resources_registry.find_by_url.assert_called_once_with(float(version), resource_url)
        self._json_serializer_cls.assert_called_once_with(resource.model)
