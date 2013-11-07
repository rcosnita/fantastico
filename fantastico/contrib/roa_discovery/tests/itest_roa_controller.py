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
.. py:module:: fantastico.contrib.roa_discovery.tests.itest_roa_controller
'''
from fantastico.server.tests.itest_dev_server import DevServerIntegration
from urllib.request import Request
import http
import json
import urllib

class RoaControllerIntegration(DevServerIntegration):
    '''This class provides the integration tests for ROA architecture implemented into Fantastico. The test cases cover
    success scenarios for sample resource provided as example.'''

    _expected_resources = [{"name": "Simple resource 1",
                           "description": "A very long description which must be saved correctly to database.",
                           "total": 50.0,
                           "vat": 0.24},
                          {"name": "Resource 2",
                           "description": "Resource 2 description which must be saved correctly to database.",
                           "total": 22.59,
                           "vat": 0.24},
                          {"name": "Resource -11",
                           "description": "Resource -11 description which must be saved correctly to database.",
                           "total": 19.99,
                           "vat": 0.19}]

    _locations_delete = []

    _response = None
    _exception = None

    def init(self):
        '''This method is invoked automatically in order to setup test cases dependencies correctly.'''

        for resource_body in self._expected_resources:
            self._response = None
            self._exception = None

            self._create_resource(json.dumps(resource_body))

    def cleanup(self):
        '''This method is invoked after each test case in order to delete all resources that were added in the setup of this
        test suite.'''

        self.assertEqual(len(self._expected_resources), len(self._locations_delete))

        for location in self._locations_delete:
            self._response = None
            self._exception = None
            self._delete_resource(location)

    def _create_resource(self, resource_body):
        '''This method tries to create the given resource body and asserts for successful response.'''

        resource_body = resource_body.encode()

        endpoint = "/api/1.0/sample-resources"

        def create_resource(server):
            request = Request(self._get_server_base_url(server, endpoint))
            request.add_header("Content-Type", "application/json")
            request.add_header("Content-Length", len(resource_body))
            request.add_data(resource_body)

            self._response = urllib.request.urlopen(request)

        def assert_creation(server):
            self.assertIsNotNone(self._response)
            self.assertEqual(201, self._response.getcode())

            headers = self._response.info()

            self.assertIsNotNone(headers)

            self.assertEqual("application/json; charset=UTF-8", headers["Content-Type"])
            self.assertEqual("0", headers["Content-Length"])
            self.assertTrue(headers.get("Location").startswith(endpoint))

            self._locations_delete.append(headers["Location"])

        self._run_test_against_dev_server(create_resource, assert_creation)

    def _delete_resource(self, location):
        '''This method removes the given resource by location.'''

        def delete_resource(server):
            conn = http.client.HTTPConnection(host=server.hostname, port=server.port)
            conn.request("DELETE", location)

            self._response = conn.getresponse()

            conn.close()

        def assert_deletion(server):
            self.assertIsNotNone(self._response)
            self.assertEqual(204, self._response.status)
            self.assertEqual("application/json; charset=UTF-8", self._response.getheader("Content-Type"))
            self.assertEqual("0", self._response.getheader("Content-Length"))

        self._run_test_against_dev_server(delete_resource, assert_deletion)

    def test_retrieve_items_paginated(self):
        '''This test case retrieves the first two items of sample resources.'''
