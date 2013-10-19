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
from fantastico.mvc.base_controller import BaseController
from fantastico.mvc.controller_decorators import ControllerProvider, Controller
from fantastico.mvc.model_facade import ModelFacade
from fantastico.roa.resource_json_serializer import ResourceJsonSerializer
from fantastico.roa.resources_registry import ResourcesRegistry
from fantastico.settings import SettingsFacade
from webob.response import Response
import json
from fantastico.roa.query_parser import QueryParser

@ControllerProvider()
class RoaController(BaseController):
    '''This class provides dynamic routes for ROA registered resources. All CRUD operations are supported out of the box. In
    addition error handling is automatically provided by this controller.'''

    SETTINGS_FACADE = SettingsFacade()
    ROA_API = SETTINGS_FACADE.get("roa_api")
    BASE_URL = "%s/(?P<version>[0-9]{1,}\\.[0-9]{1,})(?P<resource_url>.*)" % ROA_API

    OFFSET_DEFAULT = 0
    LIMIT_DEFAULT = 100

    def __init__(self, settings_facade, resources_registry_cls=ResourcesRegistry, model_facade_cls=ModelFacade,
                 conn_manager=mvc.CONN_MANAGER,
                 json_serializer_cls=ResourceJsonSerializer,
                 query_parser_cls=QueryParser):
        super(RoaController, self).__init__(settings_facade)

        self._resources_registry = resources_registry_cls()
        self._model_facade_cls = model_facade_cls
        self._conn_manager = conn_manager
        self._json_serializer_cls = json_serializer_cls
        self._query_parser_cls = query_parser_cls

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

    @Controller(url=BASE_URL + "(/)?$")
    def get_collection(self, request, version, resource_url):
        '''This method provides the route for accessing a resource collection. :doc:`/features/roa/rest_standard` for collections
        are enabled by this method. The typical response format is presented below:

        .. code-block:: javascript

            var response = {"items": [
                                // resources represented as json objects.
                            ],
                            "totalItems": 100}
        '''

        version = float(version)
        params = CollectionParams(request, RoaController.OFFSET_DEFAULT, RoaController.LIMIT_DEFAULT)

        resource = self._resources_registry.find_by_url(version, resource_url)

        json_serializer = self._json_serializer_cls(resource.model)

        filter_expr = self._parse_filter(params.filter_expr)
        sort_expr = self._parse_sort(params.order_expr)

        model_facade = self._model_facade_cls(resource.model, self._conn_manager.get_connection(request.request_id))

        models = model_facade.get_records_paged(start_record=params.offset, end_record=params.limit,
                                                filter_expr=filter_expr,
                                                sort_expr=sort_expr)
        items = [json_serializer.serialize(model) for model in models]

        models_count = model_facade.count_records(filter_expr=filter_expr)

        body = {"items": items,
                "totalItems": models_count}

        return Response(text=json.dumps(body), content_type="application/json", status_code=200)

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

    def __init__(self, request, offset_default, limit_default):
        self._offset = request.params.get("offset", offset_default)

        if isinstance(self._offset, str):
            self._offset = int(self._offset)

        self._limit = request.params.get("limit", limit_default)

        if isinstance(self._limit, str):
            self._limit = int(self._limit)

        self._filter = request.params.get("filter")
        self._order = request.params.get("order")
