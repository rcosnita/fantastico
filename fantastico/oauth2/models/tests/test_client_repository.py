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
from fantastico.oauth2.models.client_repository import ClientRepository
from fantastico.oauth2.models.clients import Client
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from fantastico.exceptions import FantasticoDbNotFoundError

class ClientRepositoryTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for client repository.'''

    _db_conn = None
    _repo = None
    _client_facade = None

    def init(self):
        '''This method is invoked automatically in order to set common dependencies for all test cases.'''

        self._client_facade = Mock()
        model_facade_cls = Mock(return_value=self._client_facade)

        self._db_conn = Mock()
        self._repo = ClientRepository(self._db_conn, model_facade_cls=model_facade_cls)

        model_facade_cls.assert_called_once_with(Client, self._db_conn)

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
