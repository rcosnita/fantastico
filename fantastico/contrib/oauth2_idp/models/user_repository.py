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
.. py:module:: fantastico.contrib.oauth2_idp.models.user_repository
'''
from fantastico.contrib.oauth2_idp.models.users import User
from fantastico.mvc.model_facade import ModelFacade
from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.exceptions import FantasticoDbNotFoundError

class UserRepository(object):
    '''This class provides a repository for facilitating easy access to users and persons.'''

    def __init__(self, db_conn, model_facade_cls=ModelFacade):
        self._db_conn = db_conn
        self._user_facade = model_facade_cls(User, self._db_conn)

    def load_by_username(self, username):
        '''This method tries to load a user by username. If it does not exist a FantasticoDbNotFoundError is raised.'''

        users = self._user_facade.get_records_paged(start_record=0, end_record=1,
                                                    filter_expr=ModelFilter(User.username, username, ModelFilter.EQ))

        if not users:
            raise FantasticoDbNotFoundError("User %s does not exist." % username)

        return users[0]
