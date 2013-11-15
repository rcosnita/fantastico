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
.. py:module:: fantastico.contrib.tracking_codes.tests.itest_tracking_controller
'''

from fantastico.server.tests.itest_dev_server import DevServerIntegration
from http.client import HTTPConnection
from urllib.request import Request
import json
import urllib

class TrackingControllerIntegration(DevServerIntegration):
    '''This class ensures tracking controller endpoints work as expected.'''

    _exception = None
    _response = None

    def init(self):
        '''This method is invoked automatically in order to set common test dependencies.'''

        self._exception = None
        self._response = None

    def test_tracking_codes_ok(self):
        '''This test case ensures all tracking codes are returned via REST api.'''

        endpoint = "/tracking-codes/codes"

        self._test_tracking_codes_ok_scenario(endpoint)

    def test_tracking_codes_tralingslash_ok(self):
        '''This test case ensures all tracking codes are returned via REST api with trailing slash given.'''

        endpoint = "/tracking-codes/codes/"

        self._test_tracking_codes_ok_scenario(endpoint)

    def test_tracking_codes_ui_ok(self):
        '''This test case ensures tracking codes ui component renders correctly.'''

        endpoint = "/tracking-codes/ui/codes"

        def retrieve_ui(server):
            http_conn = HTTPConnection(server.hostname, server.port)
            http_conn.connect()

            http_conn.request("GET", endpoint, headers={"Content-Type": "text/html"})

            self._response = http_conn.getresponse()

            http_conn.close()

        def assert_logic(server):
            self.assertIsNotNone(self._response)
            self.assertEqual(200, self._response.status)
            self.assertEqual("text/html; charset=UTF-8", self._response.headers["Content-Type"])

            body = self._response.read().decode()

            self.assertEqual("<script>test snippet</script>\n", body)

        self._run_test_against_dev_server(retrieve_ui, assert_logic)

    def _test_tracking_codes_ok_scenario(self, endpoint):
        '''This method provides a template scenario for tracking codes retrieval.'''

        def retrieve_codes(server):
            request = Request(self._get_server_base_url(server, endpoint))

            self._response = urllib.request.urlopen(request)

        def assert_logic(server):
            self.assertIsNotNone(self._response)
            self.assertEqual(200, self._response.getcode())
            self.assertEqual("application/json; charset=UTF-8", self._response.info()["Content-Type"])

            body = self._response.read().decode()

            self.assertIsNotNone(body)

            codes = json.loads(body)

            self.assertEqual(1, len(codes))
            self.assertEqual("Google Analytics", codes[0]["provider"])
            self.assertEqual("<script>test snippet</script>", codes[0]["script"])

        self._run_test_against_dev_server(retrieve_codes, assert_logic)
