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
.. py:module:: fantastico.mvc.tests.itest_dbsession_manager
'''
from fantastico import mvc
from fantastico.settings import SettingsFacade
from fantastico.tests.base_case import FantasticoIntegrationTestCase

class DbSessionManagerntegration(FantasticoIntegrationTestCase):
    '''This class provides the test suite for checking correct behavior of session management layer.'''

    def init(self):
        '''This method is responsible for initializing a new connection manager before each test case.'''

        mvc.CONN_MANAGER = mvc.init_dm_db_engine(db_config=SettingsFacade().get("database_config"), echo=True)

    def cleanup(self):
        mvc.CONN_MANAGER = None

    def test_dbsession_per_request(self):
        '''This test case makes sure db connections are persistent per http request.'''

        request_id = 1
        request_id2 = 2

        conn = mvc.CONN_MANAGER.get_connection(request_id)
        conn2 = mvc.CONN_MANAGER.get_connection(request_id)
        conn3 = mvc.CONN_MANAGER.get_connection(request_id2)

        self.assertIsNotNone(conn)
        self.assertIsNotNone(conn2)
        self.assertIsNotNone(conn3)

        self.assertEqual(conn, conn2)
        self.assertNotEqual(conn, conn3)

    def test_dbsession_close(self):
        '''This test case makes sure db connections can be correctly closed on demand.'''

        request_id = 1

        conn = mvc.CONN_MANAGER.get_connection(request_id)

        mvc.CONN_MANAGER.close_connection(request_id)

        conn2 = mvc.CONN_MANAGER.get_connection(request_id)

        self.assertIsNotNone(conn)
        self.assertIsNotNone(conn2)

        self.assertNotEqual(conn, conn2)

    def test_dbsession_close_invalidrequest(self):
        '''This test case makes sure no exception is raise when we try to close an inexistent request session.'''

        mvc.CONN_MANAGER.close_connection(-1)
