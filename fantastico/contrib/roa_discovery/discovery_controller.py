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
.. py:module:: fantastico.contrib.roa_discovery.discovery_controller
'''
from fantastico.mvc.base_controller import BaseController
from fantastico.mvc.controller_decorators import Controller
from fantastico.roa import resources_registry
from webob.response import Response
import json

class RoaDiscoveryController(BaseController):
    '''This class provides the routes for introspecting Fantastico registered resources through ROA. It is extremely useful
    to surf using your browser and to not be required to hardcode links in your code. Typically, you will want to code your
    client side applications against resources name and you are going to use this controller to find the location of those
    records.

    By default, all ROA resources are mapped on **/api/** relative to current project root. You can easily change this behavior
    by modifying the settings of your application (:py:class:`fantastico.settings.BasicSettings` - property **roa_api_url**)'''

    def __init__(self, settings_facade, registry_cls=None):
        super(RoaDiscoveryController, self).__init__(settings_facade)

        registry_cls = registry_cls or resources_registry.ResourcesRegistry

        self._registry = registry_cls()
        self._roa_api = self._settings_facade.get("roa_api")

    @Controller(url="/roa/resources(/)?$", method="GET")
    def list_registered_resources(self, request):
        '''This method list all registered resources as well as a link to their entry point.

        .. code-block:: javascript

            // ROA api is mapped on a subdomain: roa.fantasticoproject.com
            // listing is done by GET http://fantasticoproject.com/roa/resources HTTP/1.1

            {
                "Person": {1.0 : "http://roa.fantasticoproject.com/1.0/persons",
                           "latest": "http://roa.fantasticoproject.com/latest/persons"},
                "Address": {1.0 : "http://roa.fantasticoproject.com/1.0/addresses",
                            2.0 : "http://roa.fantasticoproject.com/2.0/addresses",
                            "latest": "http://roa.fantasticoproject.com/latest/addresses"}
            }

        .. code-block:: javascript

            // ROA api is mapped on a relative path of the project: http://fantasticoproject.com/api/
            // listing is done by GET http://fantasticoproject.com/roa/resources HTTP/1.1

            {
                "Person": {1.0 : "http://fantasticoproject.com/api/1.0/persons",
                           "latest": "http://roa.fantasticoproject.com/api/latest/persons"},
                "Address": {1.0 : "http://roa.fantasticoproject.com/api/1.0/addresses",
                            2.0 : "http://roa.fantasticoproject.com/api/2.0/addresses",
                            "latest": "http://roa.fantasticoproject.com/api/latest/addresses"}
            }'''

        body = {}
        resources = self._registry.all_resources()

        for resource in resources:
            if not body.get(resource.name):
                body[resource.name] = {}

            body[resource.name][resource.version] = self._calculate_resource_url(resource, resource.version)
            body[resource.name]["latest"] = self._calculate_resource_url(resource, "latest")

        body = json.dumps(body).encode()

        return Response(body=body, content_type="application/json", charset="UTF-8")

    def _calculate_resource_url(self, resource, version):
        '''This method calculates resource API url based on the given resource object and version.'''

        url = "%(api_url)s/%(version)s%(url)s" % \
                {"api_url": self._roa_api,
                 "version": version,
                 "url": resource.url}

        return url
