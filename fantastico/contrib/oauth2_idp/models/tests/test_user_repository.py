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
.. py:module:: fantastico.contrib.oauth2_idp.models.tests.test_user_repository
'''
from fantastico.contrib.oauth2_idp.models.user_repository import UserRepository
from fantastico.contrib.oauth2_idp.models.users import User
from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from fantastico.exceptions import FantasticoDbNotFoundError

class UserRepositoryTests(FantasticoUnitTestsCase):
    '''This class provides tests suite for user repository.'''

    _db_conn = None
    _repo = None
    _user_facade = None

    def init(self):
        '''This method is invoked automatically in order to setup common dependencies for all test cases.'''

        self._db_conn = Mock()
        self._user_facade = Mock()

        model_facade_cls = Mock(return_value=self._user_facade)

        self._repo = UserRepository(self._db_conn, model_facade_cls=model_facade_cls)

        model_facade_cls.assert_called_once_with(User, self._db_conn)

    def test_load_by_username(self):
        '''This test case ensures a user can be loaded by username.'''

        user = User(username="john.doe@gmail.com", password="abcd", person_id=1)

        self._user_facade.get_records_paged = Mock(return_value=[user])

        result = self._repo.load_by_username(user.username)

        self.assertEqual(user, result)

        self._user_facade.get_records_paged.assert_called_once_with(
                                                start_record=0, end_record=1,
                                                filter_expr=ModelFilter(User.username, user.username, ModelFilter.EQ))

    def test_load_by_username_notfound(self):
        '''This test case ensures a concrete db exception is raised if the given username is not found.'''

        self._user_facade.get_records_paged = Mock(return_value=[])

        with self.assertRaises(FantasticoDbNotFoundError):
            self._repo.load_by_username("john.doe")
