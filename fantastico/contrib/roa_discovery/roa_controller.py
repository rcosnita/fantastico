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
.. py:module:: fantastico.contrib.roa_discovery.roa_controller
'''
from fantastico import mvc
from fantastico.contrib.roa_discovery import roa_helper
from fantastico.mvc.base_controller import BaseController
from fantastico.mvc.controller_decorators import ControllerProvider, Controller
from fantastico.mvc.model_facade import ModelFacade
from fantastico.roa.query_parser import QueryParser
from fantastico.roa.resource_json_serializer import ResourceJsonSerializer
from fantastico.roa.resources_registry import ResourcesRegistry
from fantastico.roa.roa_exceptions import FantasticoRoaError
from fantastico.settings import SettingsFacade
from webob.response import Response
import json
from fantastico.exceptions import FantasticoDbError

@ControllerProvider()
class RoaController(BaseController):
    '''This class provides dynamic routes for ROA registered resources. All CRUD operations are supported out of the box. In
    addition error handling is automatically provided by this controller.'''

    SETTINGS_FACADE = SettingsFacade()
    ROA_API = roa_helper.normalize_absolute_roa_uri(SETTINGS_FACADE.get("roa_api"))
    BASE_URL = "%s/(?P<version>[0-9]{1,}\\.[0-9]{1,})(?P<resource_url>.*)" % ROA_API
    BASE_LATEST_URL = "%s/latest/(?P<resource_url>.*)" % ROA_API

    OFFSET_DEFAULT = 0
    LIMIT_DEFAULT = 100

    def __init__(self, settings_facade, resources_registry_cls=ResourcesRegistry, model_facade_cls=ModelFacade,
                 conn_manager=mvc,
                 json_serializer_cls=ResourceJsonSerializer,
                 query_parser_cls=QueryParser):
        super(RoaController, self).__init__(settings_facade)

        self._resources_registry = resources_registry_cls()
        self._model_facade_cls = model_facade_cls
        self._conn_manager = conn_manager
        self._json_serializer_cls = json_serializer_cls
        self._query_parser_cls = query_parser_cls

        doc_base = "%sfeatures/roa/errors/" % self._settings_facade.get("doc_base")
        self._errors_url = doc_base + "error_%s.html"
        self._roa_api = self._settings_facade.get("roa_api")

    def _parse_filter(self, filter_expr):
        '''This method parse a string filter expression and builds a compatible ModelFilter.'''

        if not filter_expr:
            return None

        query_parser = self._query_parser_cls()

        return query_parser.parse_filter(filter_expr)

    def _parse_sort(self, sort_expr):
        '''This method parse a string sort expression and builds a compatible ModelSort.'''

        if not sort_expr:
            return None

        query_parser = self._query_parser_cls()

        return query_parser.parse_sort(sort_expr)

    def _build_error_response(self, http_code, error_code, error_description, error_details):
        '''This method builds an error response compliant with :doc:`/features/roa/rest_responses` specification.'''

        error = {"error_code": error_code,
                 "error_description": error_description,
                 "error_details": error_details}

        return Response(text=json.dumps(error), status_code=http_code, content_type="application/json")

    def _handle_resource_notfound(self, version, url):
        '''This method build a resource not found response which is sent to the client. You can find more information about error
        responses format on :doc:`/features/roa/rest_responses`'''

        error_code = 10000

        return self._build_error_response(http_code=404,
                                          error_code=error_code,
                                          error_description="Resource %s version %s does not exist." % (url, version),
                                          error_details=self._errors_url % error_code)

    def _handle_resource_item_notfound(self, version, url, resource_id):
        '''This method build a resource not found response which is sent to the client. You can find more information about error
        responses format on :doc:`/features/roa/rest_responses`. In the error description it also contains resource id.'''

        error_code = 10040

        return self._build_error_response(http_code=404,
                                          error_code=error_code,
                                          error_description="Resource %s version %s id %s does not exist." % \
                                            (url, version, resource_id),
                                          error_details=self._errors_url % error_code)

    def _handle_resource_invalid(self, version, url, ex):
        '''This method builds a resource invalid response which is sent to the client.'''

        error_code = 10010

        return self._build_error_response(http_code=ex.http_code,
                                          error_code=error_code,
                                          error_description="Resource %s version %s is invalid: %s" % \
                                                    (url, version, str(ex)),
                                          error_details=self._errors_url % error_code)

    def _handle_resource_nobody(self, version, url):
        '''This method builds a resource nobody given response which is sent to the client.'''

        error_code = 10020

        return self._build_error_response(http_code=400,
                                          error_code=error_code,
                                          error_description="Resource %s version %s can not be created: no body given." % \
                                                    (url, version),
                                          error_details=self._errors_url % error_code)

    def _handle_resource_dberror(self, version, url, dbex):
        '''This method builds a resource dberror response which is sent to the client.'''

        error_code = 10030

        return self._build_error_response(http_code=400,
                                          error_code=error_code,
                                          error_description="Resource %s version %s can not be created: %s." % \
                                                    (url, version, str(dbex)),
                                          error_details=self._errors_url % error_code)

    def _get_current_connection(self, request):
        '''This method returns the current db connection for this request.'''

        return self._conn_manager.CONN_MANAGER.get_connection(request.request_id)

    @Controller(url=BASE_URL + "(/)?$", method="GET")
    def get_collection(self, request, version, resource_url):
        '''This method provides the route for accessing a resource collection. :doc:`/features/roa/rest_standard` for collections
        are enabled by this method. The typical response format is presented below:

        .. code-block:: javascript

            var response = {"items": [
                                // resources represented as json objects.
                            ],
                            "totalItems": 100}

        If a resource is not found or the resource version does not exist the following response is returned:

        .. code-block:: javascript

            {"error_code": 10000,
             "error_description": "Resource %s version %s does not exist.",
             "error_details": "http://rcosnita.github.io/fantastico/html/features/roa/errors/error_10000.html"}
        '''

        if version != "latest":
            version = float(version)

        params = CollectionParams(request, RoaController.OFFSET_DEFAULT, RoaController.LIMIT_DEFAULT)

        resource = self._resources_registry.find_by_url(resource_url, version)

        if not resource:
            return self._handle_resource_notfound(version, resource_url)

        json_serializer = self._json_serializer_cls(resource)

        filter_expr = self._parse_filter(params.filter_expr)
        sort_expr = self._parse_sort(params.order_expr)

        model_facade = self._model_facade_cls(resource.model, self._get_current_connection(request))

        models = model_facade.get_records_paged(start_record=params.offset, end_record=params.limit,
                                                filter_expr=filter_expr,
                                                sort_expr=sort_expr)
        items = [json_serializer.serialize(model, params.fields) for model in models]

        models_count = model_facade.count_records(filter_expr=filter_expr)

        body = {"items": items,
                "totalItems": models_count}

        return Response(text=json.dumps(body), content_type="application/json", status_code=200)

    @Controller(url=BASE_LATEST_URL + "(/)?$", method="GET")
    def get_collection_latest(self, request, resource_url):
        '''This method retrieves a resource collection using the latest version of the api.'''

        return self.get_collection(request, "latest", resource_url)

    @Controller(url=BASE_URL + "(/)?$", method="OPTIONS")
    def handle_resource_options(self, request, version, resource_url):
        '''This method enables support for http ajax CORS requests. This is mandatory if we want to host apis on different
        domains than project host.'''

        resource = self._resources_registry.find_by_url(resource_url, float(version))

        if not resource:
            return self._handle_resource_notfound(version, resource_url)

        response = Response(content_type="application/json", status_code=200)
        response.headers["Content-Length"] = "0"
        response.headers["Cache-Control"] = "private"
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "OPTIONS,GET,POST,PUT,DELETE"
        response.headers["Access-Control-Allow-Headers"] = request.headers.get("Access-Control-Request-Headers", "")

        return response

    def _validate_resource(self, resource, request_body):
        '''This method is used to validate the resource. If the resource validation fails an error response is sent. Otherwise
        the newly validated model is returned.'''

        if not request_body:
            return self._handle_resource_nobody(resource.version, resource.url)

        model = self._json_serializer_cls(resource.model).deserialize(request_body.decode())

        if not resource.validator:
            return model

        try:
            resource.validator().validate(model)
        except FantasticoRoaError as ex:
            return self._handle_resource_invalid(resource.version, resource.url, ex)

        return model

    @Controller(url=BASE_URL + "/(?<resource_id>.*?)(/)?$", method="GET")
    def get_item(self, request, version, resource_url, resource_id):
        '''This method provides the API for retrieving a single item from a collection. The item is uniquely identified by
        resource_id. Below you can find a success response example:

        .. code-block:: html

            GET - /api/1.0/simple-resources/1 HTTP/1.1

            200 OK
            Content-Type: application/json
            Content-Length: ...

            {
                "id": 1,
                "name": "Test resource",
                "description": "Simple description"
            }

        Of course there are cases when exceptions might occur. Below, you can find a list of error response retrieved from
        get_item API:

            * **10000** - Whenever we try to retrieve a resource with unknown type. (Not registered to ROA).
            * **10030** - Whenever we try to retrieve a resource and an unexpected database exception occurs.
            * **10040** - Whenever we try to retrieve a resource which does not exist.
        '''

        version = float(version)
        fields = request.params.get("fields")

        resource = self._resources_registry.find_by_url(resource_url, version)

        if not resource:
            return self._handle_resource_notfound(version, resource_url)

        model_facade = self._model_facade_cls(resource.model, self._get_current_connection(request))

        try:
            model = model_facade.find_by_pk({model_facade.model_pk_cols[0]: resource_id})
        except FantasticoDbError as dbex:
            return self._handle_resource_dberror(version, resource_url, dbex)

        if not model:
            return self._handle_resource_item_notfound(version, resource_url, resource_id)

        json_serializer = self._json_serializer_cls(resource)

        resource_body = json_serializer.serialize(model, fields)
        resource_body = json.dumps(resource_body)

        return Response(body=resource_body.encode(), content_type="application/json", status_code=200)

    @Controller(url=BASE_URL + "(/)?$", method="POST")
    def create_item(self, request, version, resource_url):
        '''This method provides the route for adding new resources into an existing collection. The API is json only and invoke
        the validator as described in ROA spec. Usually, when a resource is created successfully a similar answer is returned to
        the client:

        .. code-block:: html

            201 Created
            Content-Type: application/json
            Content-Length: 0
            Location: /api/2.0/app-settings/123

        Below you can find all error response codes which might be returned when creating a new resource:

            * **10000** - Whenever we try to create a resource with unknown type. (Not registered to ROA).
            * **10010** - Whenever we try to create a resource which fails validation.
            * **10020** - Whenever we try to create a resource without passing a valid body.
            * **10030** - Whenever we try to create a resource and an unexpected database exception occurs.

        You can find more information about typical REST ROA APIs response on :doc:`/features/roa/rest_responses`.'''

        if version != "latest":
            version = float(version)

        resource = self._resources_registry.find_by_url(resource_url, version)

        if not resource:
            return self._handle_resource_notfound(version, resource_url)

        model = self._validate_resource(resource, request.body)

        if isinstance(model, Response):
            return model

        try:
            model_facade = self._model_facade_cls(resource.model, self._get_current_connection(request))
            model_id = model_facade.create(model)
        except FantasticoDbError as dbex:
            return self._handle_resource_dberror(resource.version, resource.url, dbex)

        model_location = roa_helper.calculate_resource_url(self._roa_api, resource, version)
        model_location += "/%s" % model_id

        response = Response(status_code=201, content_type="application/json")
        response.headers["Location"] = model_location

        return response

    @Controller(url=BASE_LATEST_URL + "(/)?$", method="POST")
    def create_item_latest(self, request, resource_url):
        '''This method provides create item latest API version.'''

        return self.create_item(request, "latest", resource_url)

class CollectionParams(object):
    '''This object defines the structure for get_collection supported query parameters.'''

    @property
    def offset(self):
        '''This property returns offset provided in the request.'''

        return self._offset

    @property
    def limit(self):
        '''This property returns limit provided in the request.'''

        return self._limit

    @property
    def filter_expr(self):
        '''This property returns **filter** query parameter received by collection.'''

        return self._filter

    @property
    def order_expr(self):
        '''This property returns **order** query parameter received by collection.'''

        return self._order

    @property
    def fields(self):
        '''This property returns **fields** query parameter received by collection.'''

        return self._fields

    def __init__(self, request, offset_default, limit_default):
        self._offset = request.params.get("offset", offset_default)

        if isinstance(self._offset, str):
            self._offset = int(self._offset)

        self._limit = request.params.get("limit", limit_default)

        if isinstance(self._limit, str):
            self._limit = int(self._limit)

        self._filter = request.params.get("filter")
        self._order = request.params.get("order")
        self._fields = request.params.get("fields")