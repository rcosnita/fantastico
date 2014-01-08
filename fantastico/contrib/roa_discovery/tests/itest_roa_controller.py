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
from http.client import HTTPConnection
import copy
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

    _expected_subresources = [{"name": "subresource-1-resource-1",
                               "description": "simple description"},
                              {"name": "subresource-2-resource-1",
                               "description": "simple description 2"}]

    _locations_delete = None
    _locations_subresource_delete = None

    _endpoint = "/api/1.0/sample-resources"
    _endpoint_latest = "/api/latest/sample-resources"
    _endpoint_subresource_latest = "/api/latest/sample-subresources"

    def init(self):
        '''This method is invoked automatically in order to setup test cases dependencies correctly.'''

        self._locations_delete = []
        self._locations_subresource_delete = []

        self._create_resources(self._expected_resources)

    def cleanup(self):
        '''This method is invoked after each test case in order to delete all resources that were added in the setup of this
        test suite.'''

        self.assertEqual(len(self._expected_resources), len(self._locations_delete))

        self._locations_delete.extend(self._locations_subresource_delete)

        self._delete_resources(self._locations_delete)

    def _create_resources(self, expected_resources):
        '''This method tries to create the given resources and asserts for successful response.'''

        results = {"response": None}

        def create_resource(server):
            for resource_body in expected_resources:
                results["response"] = None

                http_conn = HTTPConnection(server.hostname, server.port)

                create_subresources = resource_body == expected_resources[0]

                resource_body = json.dumps(resource_body).encode()

                http_conn.request("POST", self._endpoint, resource_body,
                                  headers={"Content-Type": "application/json",
                                           "Content-Length": len(resource_body)})
                results["response"] = http_conn.getresponse()

                http_conn.close()

                location = results["response"].headers["Location"]
                self._locations_delete.append(location)

                resource_id = int(location.split("/")[-1])
                self._expected_resources[len(self._locations_delete) - 1]["id"] = resource_id

                if not create_subresources:
                    continue

                for subresource_body in self._expected_subresources:
                    self._create_subresource_for_resource(subresource_body, resource_id, server)

        def assert_creation(server):
            response = results["response"]

            self.assertIsNotNone(response)
            self.assertEqual(201, response.status)

            headers = response.headers

            self.assertIsNotNone(headers)

            self.assertEqual("application/json; charset=UTF-8", headers["Content-Type"])
            self.assertEqual("0", headers["Content-Length"])
            self.assertTrue(headers.get("Location").startswith(self._endpoint))

        self._run_test_against_dev_server(create_resource, assert_creation)

    def _create_subresource_for_resource(self, subresource_body, resource_id, server):
        '''This method creates the given subresource and assign it to the given resource unique identifier.'''

        subresource_body["resource_id"] = resource_id

        http_conn = HTTPConnection(server.hostname, server.port)
        http_conn.connect()

        http_conn.request("POST", self._endpoint_subresource_latest, json.dumps(subresource_body).encode(),
                          headers={"Content-Type": "application/json"})

        response = http_conn.getresponse()

        http_conn.close()

        self.assertEqual(201, response.status)
        self.assertEqual("application/json; charset=UTF-8", response.headers["Content-Type"])
        self.assertEqual("0", response.headers["Content-Length"])

        location = response.headers["Location"]
        self.assertIsNotNone(location)

        self._locations_subresource_delete.insert(0, location)

        subresource_id = int(location.split("/")[-1])
        subresource_body["id"] = subresource_id

    def _delete_resources(self, locations):
        '''This method removes the given resource by location.'''

        results = {"response": None}

        def delete_resource(server):
            http_conn = http.client.HTTPConnection(host=server.hostname, port=server.port)

            for location in reversed(self._locations_delete):
                results["response"] = None

                http_conn.request("DELETE", location)

                results["response"] = http_conn.getresponse()

            http_conn.close()

        def assert_deletion(server):
            response = results["response"]

            self.assertIsNotNone(response)
            self.assertEqual(204, response.status)
            self.assertEqual("application/json; charset=UTF-8", response.getheader("Content-Type"))
            self.assertEqual("0", response.getheader("Content-Length"))

        self._run_test_against_dev_server(delete_resource, assert_deletion)

    def _test_retrieve_items(self, offset, limit, expected_resources, fields=None, order_expr=None,
                             filter_expr=None, total_items=None):
        '''This test case retrieves the first two items of sample resources.'''

        total_items = total_items or len(self._expected_resources)
        fields = fields or []

        results = {"response": None}

        def get_resources(server):
            url = "%s?offset=%s&limit=%s" % \
                    (self._get_server_base_url(server, self._endpoint_latest),
                     offset, limit)

            if fields:
                url += "&fields=%s" % ",".join(fields)

            if order_expr:
                url += "&order=%s" % order_expr

            if filter_expr:
                url += "&filter=%s" % filter_expr

            request = urllib.request.Request(url)

            results["response"] = urllib.request.urlopen(request)

        def assert_resources(server):
            response = results["response"]

            self.assertIsNotNone(response)
            self.assertEqual(200, response.getcode())

            headers = response.info()

            self.assertIsNotNone(headers)
            self.assertEqual("application/json; charset=UTF-8", headers["Content-Type"])

            body = response.read().decode()

            self.assertGreater(len(body), 0)

            body = json.loads(body)

            self.assertEqual(limit, len(body.get("items")))
            self.assertEqual(total_items, body.get("totalItems"))

            items = body.get("items")

            for idx in range(0, limit):
                self._assert_resources_equal(expected_resources[idx], items[idx], fields)

        self._run_test_against_dev_server(get_resources, assert_resources)

    def test_retrieve_items_first(self):
        '''This test case ensures get collection can retrieve only the first item.'''

        self._test_retrieve_items(0, 1, self._expected_resources[0:1])

    def test_retrieve_items_first_two(self):
        '''This test case ensures get collection can retrieve only the first two items.'''

        self._test_retrieve_items(0, 2, self._expected_resources[0:2])

    def test_retrieve_items_last_two_partial(self):
        '''This test case ensures last two items from a collection can be partially retrieved.'''

        fields = ["name", "description"]

        self._test_retrieve_items(1, 2, self._expected_resources[1:3], fields)

    def test_retrieve_items_orderby_name(self):
        '''This test case ensures items are correctly ordered by name.'''

        order_expr = "asc(name)"

        expected_resources = [resource_body for resource_body in reversed(self._expected_resources)]

        self._test_retrieve_items(0, 3, expected_resources, order_expr=order_expr)

    def test_retrieve_items_filterby_name(self):
        '''This test case ensures items can be correctly filtered using like expressions.'''

        filter_expr = urllib.parse.quote("like(name,\"resource %\")")

        expected_resources = self._expected_resources[1:]

        self._test_retrieve_items(0, 2, expected_resources, filter_expr=filter_expr, total_items=2)

    def test_retrieve_items_filterby_and(self):
        '''This test case ensures compound **and** filter works as expected.'''

        filter_expr = urllib.parse.quote('and(in(name,["Resource 2","Resource -11"]),lt(vat,0.25))')

        expected_resources = self._expected_resources[1:]

        self._test_retrieve_items(0, 2, expected_resources, filter_expr=filter_expr, total_items=2)

    def test_retrieve_item(self):
        '''This test case covers scenario of individual item retrieval from a given collection.'''

        endpoint = self._locations_delete[-1]
        results = {"response": None}

        def retrieve_item(server):
            http_conn = HTTPConnection(server.hostname, server.port)
            http_conn.connect()

            http_conn.request("GET", endpoint, headers={"Content-Type": "application/json"})

            results["response"] = http_conn.getresponse()

            http_conn.close()

        def assert_item(server):
            response = results["response"]

            self.assertIsNotNone(response)
            self.assertEqual(200, response.status)
            self.assertEqual("application/json; charset=UTF-8", response.headers["Content-Type"])

            body = response.read()

            self.assertIsNotNone(body)

            body = json.loads(body.decode())

            self._assert_resources_equal(self._expected_resources[-1], body)

        self._run_test_against_dev_server(retrieve_item, assert_item)

    def test_update_item(self):
        '''This test case covers scenario of item update.'''

        endpoint = self._locations_delete[-1]
        expected_body = copy.copy(self._expected_resources[-1])
        expected_body["name"] = "Cool resource"
        expected_body["description"] = "Cool description"
        expected_body["total"] = 12.99
        expected_body["vat"] = 0.05

        results = {"response": None}

        def update_item(server):
            http_conn = HTTPConnection(server.hostname, server.port)
            http_conn.connect()

            http_conn.request("PUT", endpoint, json.dumps(expected_body).encode(), {"Content-Type": "application/json"})

            results["response"] = http_conn.getresponse()

            http_conn.request("GET", endpoint, headers={"Content-Type": "application/json"})

            results["response"] = http_conn.getresponse()

            http_conn.close()

        def assert_update(server):
            response = results["response"]

            self.assertIsNotNone(response)
            self.assertEqual(200, response.status)
            self.assertEqual("application/json; charset=UTF-8", response.headers["Content-Type"])

            body = response.read()

            self.assertIsNotNone(body)

            body = json.loads(body.decode())

            self._assert_resources_equal(expected_body, body)

        self._run_test_against_dev_server(update_item, assert_update)

    def test_roa_cors(self):
        '''This test case ensures CORS is enabled for ROA apis.'''

        endpoint = self._endpoint_latest

        results = {"response": None}

        def request_options(server):
            http_conn = HTTPConnection(server.hostname, server.port)

            http_conn.request("OPTIONS", endpoint, headers={"Access-Control-Request-Headers": "Header2"})
            results["response"] = http_conn.getresponse()

            http_conn.close()

        def assert_options(server):
            response = results["response"]

            self.assertIsNotNone(response)
            self.assertEqual(200, response.status)
            self.assertEqual("application/json; charset=UTF-8", response.headers["Content-Type"])
            self.assertEqual("0", response.headers["Content-Length"])
            self.assertEqual("private", response.headers["Cache-Control"])
            self.assertEqual("*", response.headers["Access-Control-Allow-Origin"])
            self.assertEqual("OPTIONS,GET,POST,PUT,DELETE", response.headers["Access-Control-Allow-Methods"])
            self.assertEqual("Header2", response.headers["Access-Control-Allow-Headers"])

        self._run_test_against_dev_server(request_options, assert_options)

    def test_get_collection_with_fields_included(self):
        '''This test case ensures retrieve collection can correctly fetch subresources.'''

        endpoint = "/api/latest/sample-resources?offset=0&limit=1&fields=id,name,description,total,vat,subresources(id,name)"
        results = {"response": None}

        def retrieve_resources(server):
            http_conn = HTTPConnection(server.hostname, server.port)

            http_conn.request("GET", endpoint, headers={"Content-Type": "application/json"})
            results["response"] = http_conn.getresponse()

            http_conn.close()

        def assert_resources(server):
            response = results["response"]

            self.assertIsNotNone(response)
            self.assertEqual(200, response.status)
            self.assertEqual("application/json; charset=UTF-8", response.headers["Content-Type"])

            body = response.read()

            self.assertIsNotNone(body)

            body = json.loads(body.decode())
            items = body.get("items")

            self.assertEqual(len(self._expected_resources), body.get("totalItems"))
            self.assertEqual(1, len(items))

            self._assert_resources_equal(self._expected_resources[0], items[0], ignore_fieldscount=True)

            idx = 0
            for subresource in items[0]["subresources"]:
                self._assert_resources_equal(self._expected_subresources[idx], subresource,
                                             fields=["id", "name"], ignore_fieldscount=False)

                idx += 1

        self._run_test_against_dev_server(retrieve_resources, assert_resources)

    def _assert_resources_equal(self, expected, actual, fields=None, ignore_fieldscount=False):
        '''This method ensures two given resource bodies are equal (only specified fields). Besides equality of specified
        of given fields this method also ensures only requested fields are part of the actual response.'''

        fields = fields or ["id", "name", "description", "total", "vat"]

        if not ignore_fieldscount:
            returned_fields = actual.keys()

            self.assertEqual(0, len(fields) - len(returned_fields))

        for field in fields:
            self.assertEqual(expected[field], actual[field])
