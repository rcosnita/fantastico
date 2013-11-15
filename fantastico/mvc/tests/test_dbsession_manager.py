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
.. py:module:: fantastico.mvc.tests.test_dbsession_manager
'''
from fantastico.exceptions import FantasticoDbError
from fantastico.mvc import DbSessionManager
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock

class DbSessionManagerTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for db session manager class. It is extremely important to kkep this running so that
    db connections are correctly managed by fantastico.'''

    _db_config = None
    _create_engine_fn = None
    _create_session_fn = None
    _db_manager = None
    _session = None
    _old_conn_data = None

    def init(self):
        '''This method setup common dependencies used within test cases.'''
        self._db_config = {"drivername": "blabla",
                          "username": "john.doe",
                          "password": "12345",
                          "host": "test_host",
                          "port": 3306,
                          "database": "mydb",
                          "additional_params": {}}

        self._create_engine_fn = Mock()

        self._session = Mock()
        self._session.remove = Mock()
        self._create_session_fn = Mock(return_value=self._session)

        DbSessionManager.ENGINE = None
        self._db_manager = DbSessionManager(self._db_config,
                                            create_engine_fn=self._create_engine_fn,
                                            create_session_fn=self._create_session_fn)

    def test_wrong_dbconfig(self):
        '''This test case ensures an exception is raised whenever dbconfig is incomplete or empty.'''

        db_config = {}

        with self.assertRaises(FantasticoDbError):
            DbSessionManager(db_config,
                             create_engine_fn=self._create_engine_fn,
                             create_session_fn=self._create_session_fn)

    def test_get_connection_ok(self):
        '''This test case ensure get connection is retrieved and cached accordingly.'''

        request_id = 1

        session = self._db_manager.get_connection(request_id)
        session2 = self._db_manager.get_connection(request_id)

        self.assertIsNotNone(session)
        self.assertIsNotNone(session2)
        self.assertEqual(session, session2)

        self.assertEqual(1, self._create_engine_fn.call_count)
        self.assertEqual(1, self._create_session_fn.call_count)

        return request_id

    def test_get_connection_close_onexception(self):
        '''This test case ensure cached session / request is closed in case an exception is raised while opening the session.'''

        create_session_fn = Mock(side_effect=Exception("Unexpected error"))

        self._db_manager = DbSessionManager(self._db_config,
                                            create_engine_fn=self._create_engine_fn,
                                            create_session_fn=create_session_fn)

        request_id = 1

        with self.assertRaises(FantasticoDbError) as ex:
            self._db_manager.get_connection(request_id)

        self.assertTrue(str(ex).find("Unexpected error"))

    def test_close_connection_ok(self):
        '''This method test close connection behavior for an existing request identifier cached connection.'''

        request_id = self.test_get_connection_ok()

        session = self._db_manager.get_connection(request_id)

        self.assertIsNotNone(session)

        self._db_manager.close_connection(request_id)
        self.assertEqual(1, self._session.remove.call_count)
