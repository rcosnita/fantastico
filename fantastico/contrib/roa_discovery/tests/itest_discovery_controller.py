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
.. py:module:: fantastico.contrib.roa_discovery.tests.itest_discovery_controller
'''
from fantastico.server.tests.itest_dev_server import DevServerIntegration
from urllib.request import Request
import json
import urllib

class RoaDiscoveryControllerIntegration(DevServerIntegration):
    '''This class provides the integration test cases for resources listing.'''

    SAMPLE_RESOURCE_NAME = "Sample Resource"

    _response = None

    def init(self):
        '''This method automatically set common dependencies for all tests.'''

        self._response = None

    def test_listing_contains_resource(self):
        '''This test case ensures that discovery and listing of resources work as expected.'''

        def request_logic(server):
            request = Request(self._get_server_base_url(server, "/roa/resources"))
            self._response = urllib.request.urlopen(request)

        def assert_logic(server):
            self.assertIsNotNone(self._response)
            self.assertEqual(200, self._response.status)
            self.assertEqual("application/json; charset=UTF-8", self._response.info()["Content-Type"])

            body = self._response.read().decode()

            self.assertIsNotNone(body)

            resources = json.loads(body)

            sample = resources.get(RoaDiscoveryControllerIntegration.SAMPLE_RESOURCE_NAME)

            self.assertIsNotNone(sample)
            self.assertEqual(sample.get("1.0"), "/api/1.0/sample-resources")
            self.assertEqual(sample.get("latest"), "/api/latest/sample-resources")

        self._run_test_against_dev_server(request_logic, assert_logic)
