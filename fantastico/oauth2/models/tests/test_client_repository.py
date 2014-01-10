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
.. py:module:: fantastico.oauth2.models.tests.test_client_repository
'''
from fantastico.exceptions import FantasticoDbNotFoundError
from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.mvc.models.model_filter_compound import ModelFilterAnd
from fantastico.oauth2.models.client_repository import ClientRepository
from fantastico.oauth2.models.clients import Client
from fantastico.oauth2.models.return_urls import ClientReturnUrl
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock

class ClientRepositoryTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for client repository.'''

    _db_conn = None
    _repo = None
    _client_facade = None
    _url_facade = None

    def init(self):
        '''This method is invoked automatically in order to set common dependencies for all test cases.'''

        self._client_facade = Mock()
        self._url_facade = Mock()

        self._db_conn = Mock()
        self._repo = ClientRepository(self._db_conn, model_facade_cls=self._get_facade_instance)

    def _get_facade_instance(self, facade_cls, db_conn):
        '''This method builds a model facade based on given facade cls.'''
        self.assertEqual(self._db_conn, db_conn)

        if facade_cls == Client:
            return self._client_facade
        elif facade_cls == ClientReturnUrl:
            return self._url_facade


    def test_load_ok(self):
        '''This test case ensures a client can be loaded correctly by client_id.'''

        client_id = "abcd"

        client = Client()

        self._client_facade.find_by_pk = Mock(return_value=client)

        result = self._repo.load(client_id)

        self.assertEqual(client, result)

        self._client_facade.find_by_pk.assert_called_once_with({Client.client_id: client_id})

    def test_load_clientnotfound(self):
        '''This test case ensures load raises a concrete exception if the client is not found.'''

        client_id = "abcd"

        ex = FantasticoDbNotFoundError("Client not found.")

        self._client_facade.find_by_pk = Mock(side_effect=ex)

        with self.assertRaises(FantasticoDbNotFoundError) as ctx:
            self._repo.load(client_id)

        self.assertEqual(ex, ctx.exception)

    def test_load_clienturl_ok(self):
        '''This test case ensures client return urls can be loaded correctly using client repository.'''

        return_url = "/abcd"

        self._test_load_clienturl_template(return_url)

    def test_load_clienturl_withqparams(self):
        '''This test case ensures only base url (without query parameters) is used for loading the client.'''

        return_url = "/abcd?q=1#x=a"
        base_url = "/abcd"

        self._test_load_clienturl_template(return_url, base_url)

    def _test_load_clienturl_template(self, return_url, base_url=None, client_id="abc"):
        '''This method provides a template for testing load_client_by_returnurl success scenarios.'''

        base_url = base_url or return_url

        client = Client(client_id=client_id)

        url = ClientReturnUrl()
        url.client = client

        self._url_facade.get_records_paged = Mock(return_value=[url])

        result = self._repo.load_client_by_returnurl(return_url)

        self.assertEqual(client, result)

        self._url_facade.get_records_paged.assert_called_once_with(
                    start_record=0, end_record=1,
                    filter_expr=ModelFilter(ClientReturnUrl.return_url, base_url, ModelFilter.EQ))

    def test_load_clienturl_notfound(self):
        '''This test case ensures None is returned when given return url is not found.'''

        self._url_facade.get_records_paged = Mock(return_value=[])

        self.assertIsNone(self._repo.load_client_by_returnurl("/abc"))
