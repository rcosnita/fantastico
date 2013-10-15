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
                 json_serializer_cls=ResourceJsonSerializer):
        super(RoaController, self).__init__(settings_facade)

        self._resources_registry = resources_registry_cls()
        self._model_facade_cls = model_facade_cls
        self._conn_manager = conn_manager
        self._json_serializer_cls = json_serializer_cls

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
        offset = request.params.get("offset", RoaController.OFFSET_DEFAULT)
        limit = request.params.get("limit", RoaController.LIMIT_DEFAULT)

        resource = self._resources_registry.find_by_url(version, resource_url)

        json_serializer = self._json_serializer_cls(resource.model)

        model_facade = self._model_facade_cls(resource.model, self._conn_manager.get_connection(request.request_id))

        models = model_facade.get_records_paged(start_record=offset, end_record=limit)
        items = [json_serializer.serialize(model) for model in models]

        models_count = model_facade.count_records()

        body = {"items": items,
                "totalItems": models_count}

        return Response(text=json.dumps(body), content_type="application/json", status_code=200)
