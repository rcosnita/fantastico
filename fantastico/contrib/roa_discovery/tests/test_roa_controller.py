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

from fantastico.mvc import BASEMODEL
from fantastico.roa.resource_decorator import Resource
from fantastico.roa.resource_validator import ResourceValidator
from fantastico.roa.roa_exceptions import FantasticoRoaError
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text
import json

class RoaControllerTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for roa controller.'''

    _settings_facade = None
    _resources_registry = None
    _model_facade = None
    _conn_manager = None
    _json_serializer_cls = None
    _json_serializer = None
    _query_parser_cls = None
    _query_parser = None
    _controller = None

    def init(self):
        '''This method setup all test cases common dependencies.'''

        from fantastico.contrib.roa_discovery.roa_controller import RoaController

        self._settings_facade = Mock()
        self._resources_registry = Mock()
        self._model_facade = Mock()
        self._conn_manager = Mock()
        self._json_serializer = Mock()
        self._query_parser = Mock()
        self._doc_base = "https://fantastico/html/"

        resources_registry_cls = Mock(return_value=self._resources_registry)
        model_facade_cls = Mock(return_value=self._model_facade)
        self._json_serializer_cls = Mock(return_value=self._json_serializer)

        self._settings_facade.get = self._mock_settings_get

        self._query_parser_cls = Mock(return_value=self._query_parser)

        self._controller = RoaController(settings_facade=self._settings_facade,
                                         resources_registry_cls=resources_registry_cls,
                                         model_facade_cls=model_facade_cls,
                                         conn_manager=self._conn_manager,
                                         json_serializer_cls=self._json_serializer_cls,
                                         query_parser_cls=self._query_parser_cls)

    def _mock_settings_get(self, setting_name):
        if setting_name == "doc_base":
            return self._doc_base

        if setting_name == "roa_api":
            return "/api"

        raise Exception("Unexpected setting %s." % setting_name)

    def _mock_model_facade(self, records, records_count):
        '''This method mocks the current model facade object in order to return the specified values.'''

        self._model_facade.get_records_paged = Mock(return_value=records)
        self._model_facade.count_records = Mock(return_value=records_count)

    def _assert_get_collection_response(self, response, records, records_count, offset, limit,
                                        expected_filter=None,
                                        expected_sort=None):
        '''This test case assert the given response against expected values.'''

        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.content_type)

        self.assertIsNotNone(response.body)

        body = json.loads(response.body.decode())

        self.assertEqual(len(records), len(body["items"]))
        self.assertEqual(records_count, body["totalItems"])

        self._model_facade.get_records_paged.assert_called_once_with(start_record=offset, end_record=limit,
                                                                     filter_expr=expected_filter,
                                                                     sort_expr=expected_sort)
        self._model_facade.count_records.assert_called_once_with(filter_expr=expected_filter)

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

        self._resources_registry.find_by_url.assert_called_once_with(resource_url, float(version))
        self._json_serializer_cls.assert_called_once_with(resource)

    def test_get_collection_first_page(self):
        '''This test case ensures get collection can return first page populated with items. In addition it ensures
        filtering and sorting is supported.'''

        expected_fields = "name,description"
        expected_records = [{"name": "Resource 1", "description": ""},
                            {"name": "Resource 2", "description": ""}]
        expected_records_count = 3
        expected_filter = Mock()
        expected_sort = Mock()

        version = "latest"
        resource_url = "/sample-resources"

        request = Mock()
        request.params = {"offset": "0", "limit": "2",
                          "filter": "like(name, \"resource 1\")",
                          "order": "asc(name)",
                          "fields": expected_fields}

        resource = Mock()
        resource.model = Mock()

        self._query_parser.parse_filter = Mock(return_value=expected_filter)
        self._query_parser.parse_sort = Mock(return_value=expected_sort)

        self._mock_model_facade(records=expected_records, records_count=expected_records_count)
        self._model_facade.get_records_paged = Mock(return_value=expected_records)
        self._model_facade.count_records = Mock(return_value=expected_records_count)

        self._resources_registry.find_by_url = Mock(return_value=resource)

        def mock_serialize(model, fields):
            self.assertEqual(expected_fields, fields)

            return model

        self._json_serializer.serialize = mock_serialize

        response = self._controller.get_collection(request, version, resource_url)

        self._assert_get_collection_response(response,
                                             records=expected_records,
                                             records_count=expected_records_count,
                                             offset=0,
                                             limit=2,
                                             expected_filter=expected_filter,
                                             expected_sort=expected_sort)

        self._resources_registry.find_by_url.assert_called_once_with(resource_url, version)
        self._json_serializer_cls.assert_called_once_with(resource)
        self._query_parser.parse_filter.assert_called_once_with(request.params["filter"])
        self._query_parser.parse_sort.assert_called_once_with(request.params["order"])

    def _assert_resource_error(self, response, http_code, error_code, version, url):
        '''This method asserts a given error response against expected resource error format.'''

        self.assertIsNotNone(response)
        self.assertEqual(http_code, response.status_code)
        self.assertEqual("application/json", response.content_type)

        self.assertIsNotNone(response.body)

        body = json.loads(response.body.decode())

        self.assertEqual(error_code, body["error_code"])
        self.assertTrue(body["error_description"].find(version) > -1)
        self.assertTrue(body["error_description"].find(url) > -1)
        self.assertEqual("%sfeatures/roa/errors/error_%s.html" % (self._doc_base, error_code), body["error_details"])

    def test_get_collection_resource_notfound(self):
        '''This test case ensures 404 is returned if we try to access a resource which does not exist.'''

        url = "/resource-not-found"
        version = "1.0"

        request = Mock()
        request.params = {}

        self._settings_facade.get = Mock(return_value=self._doc_base)

        self._resources_registry.find_by_url = Mock(return_value=None)

        response = self._controller.get_collection(request, version, url)

        self._assert_resource_error(response, 404, 10000, version, url)

        self._resources_registry.find_by_url.assert_called_once_with(url, float(version))

    def test_roa_cors_support(self):
        '''This test case ensures CORS is enabled on all ROA dynamic generated apis.'''

        url = "/simple-resource"
        version = "1.0"

        self._resources_registry.find_by_url = Mock(return_value=Mock())

        request = Mock()
        request.headers = {"Access-Control-Request-Headers": "header1,header2"}

        response = self._controller.handle_resource_options(request, version, url)

        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.content_type)
        self.assertEqual(0, response.content_length)

        self.assertEqual("private", response.headers["Cache-Control"])
        self.assertEqual("*", response.headers["Access-Control-Allow-Origin"])
        self.assertEqual("OPTIONS,GET,POST,PUT,DELETE", response.headers["Access-Control-Allow-Methods"])
        self.assertEqual(request.headers["Access-Control-Request-Headers"], response.headers["Access-Control-Allow-Headers"])

        self.assertEqual(0, len(response.body))

        self._resources_registry.find_by_url.assert_called_once_with(url, float(version))

    def test_roa_cors_support_resourcenotfound(self):
        '''This test case ensures an error is returned if an options http request is done for a resource which is not
        registered.'''

        url = "/resource-not-found"
        version = "1.0"

        self._resources_registry.find_by_url = Mock(return_value=None)

        response = self._controller.handle_resource_options(Mock(), version, url)

        self._assert_resource_error(response, 404, 10000, version, url)

        self._resources_registry.find_by_url.assert_called_once_with(url, float(version))

    def test_create_item_noresourcefound(self):
        '''This test case ensures we can not add items to an inexistent resource.'''

        url = "/sample-resource"
        version = "1.0"

        request = Mock()

        self._resources_registry.find_by_url = Mock(return_value=None)

        response = self._controller.create_item(request, version, url)

        self._assert_resource_error(response, 404, 10000, version, url)

        self._resources_registry.find_by_url.assert_called_once_with(url, float(version))

    def test_create_item_empty_body(self):
        '''This test case ensures an item can not be created if no body is given.'''

        url = "/sample-resources"
        version = "1.0"

        resource = Mock()
        resource.url = url
        resource.version = version

        request = Mock()
        request.body = None

        self._resources_registry.find_by_url = Mock(return_value=resource)

        response = self._controller.create_item(request, version, url)

        self._assert_resource_error(response, 400, 10020, version, url)

        self._resources_registry.find_by_url.assert_called_once_with(url, float(version))

    def test_create_item_invalidresource(self):
        '''This test case ensures an item can not be created if it's invalid.'''

        resource = Resource(name="Mock Simple Resource", url="/mock-simple-resources",
                            version=1.0,
                            validator=MockSimpleResourceValidator)
        resource(MockSimpleResourceRoa, self._resources_registry)

        request_body = {"description": "Simple resource description."}

        request = Mock()
        request.body = json.dumps(request_body).encode()

        self._resources_registry.find_by_url = Mock(return_value=resource)
        self._json_serializer.deserialize = Mock(return_value=MockSimpleResourceRoa(description=request_body.get("description")))

        response = self._controller.create_item(request, version=str(resource.version), resource_url=resource.url)

        self._assert_resource_error(response, 400, 10010, str(resource.version), resource.url)

        self._resources_registry.find_by_url.assert_called_once_with(resource.url, resource.version)
        self._json_serializer.deserialize.assert_called_once_with(request.body.decode())

    def test_create_item_ok(self):
        '''This test case ensures a valid resource can be created correctly.'''

        resource = Resource(name="Mock Simple Resource", url="/mock-simple-resources",
                            version=1.0)
        resource(MockSimpleResourceRoa, self._resources_registry)

        request_body = {"name": "simple-resource1",
                        "description": "Simple resource description."}

        expected_model = MockSimpleResourceRoa(name=request_body.get("name"),
                                               description=request_body.get("description"))

        expected_id = 123

        request = Mock()
        request.body = json.dumps(request_body).encode()

        self._resources_registry.find_by_url = Mock(return_value=resource)
        self._json_serializer.deserialize = Mock(return_value=expected_model)
        self._model_facade.create = Mock(return_value=expected_id)

        response = self._controller.create_item(request, str(resource.version), resource.url)

        self.assertIsNotNone(resource)
        self.assertEqual(201, response.status_code)
        self.assertEqual("application/json", response.content_type)
        self.assertEqual("0", response.headers["Content-Length"])
        self.assertEqual("/api/%s%s/%s" % (resource.version, resource.url, expected_id),
                         response.headers["Location"])

        self._resources_registry.find_by_url.assert_called_once_with(resource.url, resource.version)
        self._json_serializer.deserialize.assert_called_once_with(request.body.decode())
        self._model_facade.create.assert_called_once_with(expected_model)

class MockSimpleResourceRoa(object):
    '''This class provides a very simple used in tests.'''

    id = Column("id", Integer)
    name = Column("name", String(50))
    description = Column("description", Text)

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

class MockSimpleResourceValidator(ResourceValidator):
    '''This is a very simple validator used for testing purposes.'''

    def validate(self, resource):
        if not resource.name:
            raise FantasticoRoaError("Name must be provided.")

        return True
