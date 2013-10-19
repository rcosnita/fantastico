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
.. py:module:: fantastico.contrib.roa_discovery.tests.test_roa_helper
'''
from fantastico.contrib.roa_discovery import roa_helper
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock

class RoaHelperTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for ensuring roa helper methods work as expected.'''

    def test_calculate_resource_relative_api(self):
        '''This test case ensures an url is correctly built when roa_api is hosted on the same domain as the project.'''

        resource = Mock()
        resource.url = "/sample-resources"

        roa_api = "/api"

        self.assertEqual("/api/1.0%s" % resource.url, roa_helper.calculate_resource_url(roa_api, resource, 1.0))

    def test_calculate_resource_abs_api(self):
        '''This test case ensures an url is correctly built when roa_api is hosted on a separate domain than the project.'''

        resource = Mock()
        resource.url = "/sample-resources"

        roa_api = "https://api.fantastico.com/roa/api"

        self.assertEqual("https://api.fantastico.com/roa/api/2.0%s" % resource.url,
                         roa_helper.calculate_resource_url(roa_api, resource, 2.0))

    def test_normalize_absolute_roa_uri_relative(self):
        '''This test case ensure relative uris are not changed during normalization procedure.'''

        roa_api = "/api"

        self.assertEqual(roa_api, roa_helper.normalize_absolute_roa_uri(roa_api))

    def test_normalize_absolute_roa_uri_abs(self):
        '''This test case ensures an absolute uri is correctly transformed to a relative uri by removing protocol and
        hostname.'''

        roa_api = "https://api.fantastico.com"

        self.assertEqual("/", roa_helper.normalize_absolute_roa_uri(roa_api))

    def test_normalize_absolute_roa_uri_withpath(self):
        '''This test case ensures an absolute uri which also contains a path is transformed correctly to a relative uri by
        removing protocol and hostname.'''

        roa_api = "https://api.fantastico.com/api/sandboxed"

        self.assertEqual("/api/sandboxed", roa_helper.normalize_absolute_roa_uri(roa_api))
