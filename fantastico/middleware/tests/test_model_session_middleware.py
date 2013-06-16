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
.. py:module:: fantastico.middleware.tests.test_model_session_middleware
'''

from fantastico import mvc
from fantastico.exceptions import FantasticoError
from fantastico.middleware.model_session_middleware import ModelSessionMiddleware
from fantastico.mvc import DbSessionManager
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
import uuid

class ModelSessionMiddlewareTests(FantasticoUnitTestsCase):
    '''This class provides the test cases for db session manager.'''
    
    def init(self):
        self._normal_response = Mock()
        self._settings_facade = Mock()
        self._settings_facade_cls = Mock(return_value=self._settings_facade)
        self._environ = {}
        self._app = Mock(return_value=self._normal_response)
        self._middleware = ModelSessionMiddleware(self._app, self._settings_facade_cls)

        mvc.CONN_MANAGER = None

    def _get_db_config(self, key):
        '''This method is used to return a valid db mocked config.'''
        
        if key != "database_config":
            raise NotImplementedError()
        
        return {"drivername": "mysql+mysqlconnector",
                "username": "fantastico",
                "password": "12345",
                "port": 3306,
                "host": "localhost",
                "database": "fantastico",
                "additional_params": {"charset": "utf8"}}
    
    def test_model_session_init_ok(self):
        '''This test case ensures model session middleware correctly initialize a db session when executed.'''
                
        self._settings_facade.get = self._get_db_config
        
        engine = Mock()
        create_engine = Mock(return_value=engine)
        
        session = Mock()
        create_session = Mock(return_value=session)

        self.assertIsNone(mvc.CONN_MANAGER)
                
        response = self._middleware(self._environ, Mock(), create_engine=create_engine, 
                                    create_session=create_session)
        
        self.assertEqual(self._normal_response, response)
        self.assertIsInstance(mvc.CONN_MANAGER, DbSessionManager)

    def test_init_session_scoped_cache(self):
        '''This test case ensures a session is cached correctly across multiple requests.'''
        
        request_id = 1
        
        self._settings_facade.get = self._get_db_config
        
        engine = Mock()
        create_engine = Mock(return_value=engine)
        
        session = Mock()
        create_session = Mock(return_value=session)

        self.assertIsNone(mvc.CONN_MANAGER)
                
        response = self._middleware(self._environ, Mock(), create_engine=create_engine, 
                                    create_session=create_session)
        
        self.assertEqual(self._normal_response, response)
        self.assertIsInstance(mvc.CONN_MANAGER, DbSessionManager)
        self.assertEqual(session, mvc.CONN_MANAGER.get_connection(request_id))
        
        response = self._middleware(self._environ, Mock(), create_engine=create_engine, 
                            create_session=create_session)

        self.assertEqual(self._normal_response, response)
        self.assertIsInstance(mvc.CONN_MANAGER, DbSessionManager)
        self.assertEqual(session, mvc.CONN_MANAGER.get_connection(request_id))
    
    def test_session_init_exception_unhandled(self):
        '''This test case ensures unhandled exception raised during initialization are gracefully transformed
        to fantastico errors.'''

        self.assertIsNone(mvc.CONN_MANAGER)

        with self.assertRaises(FantasticoError):
            self._middleware(self._environ, Mock())
        
        self.assertIsNone(mvc.CONN_MANAGER)
        
        self._settings_facade.get = self._get_db_config
        create_session = Mock(side_effect=Exception("Unhandled exception"))
        
        with self.assertRaises(FantasticoError):
            self._middleware(self._environ, Mock(), create_engine=Mock(), create_session=create_session)
            mvc.CONN_MANAGER.get_connection(uuid.uuid4())
        
        self.assertIsNotNone(mvc.CONN_MANAGER)