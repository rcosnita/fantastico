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
.. py:module:: fantastico.oauth2.models.client_repository
'''
from fantastico.mvc.model_facade import ModelFacade
from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.oauth2.models.clients import Client
from fantastico.oauth2.models.return_urls import ClientReturnUrl

class ClientRepository(object):
    '''This class provides data access methods which can be used when working with Client objects.'''

    def __init__(self, db_conn, model_facade_cls=ModelFacade):
        self._db_conn = db_conn
        self._client_facade = model_facade_cls(Client, self._db_conn)
        self._url_facade = model_facade_cls(ClientReturnUrl, self._db_conn)

    def load(self, client_id):
        '''This method is used to load a client by primary key.'''

        client = self._client_facade.find_by_pk({Client.client_id: client_id})

        return client

    def load_client_by_returnurl(self, return_url):
        '''This method load the first available client descriptor which has the specified return url. Please make sure
        return url is decoded before invoking this method or it will not work otherwise.'''

        qmark_pos = return_url.find("?")
        if qmark_pos == -1:
            qmark_pos = len(return_url)

        return_url = return_url[:qmark_pos]

        results = self._url_facade.get_records_paged(
                                    start_record=0, end_record=1,
                                    filter_expr=ModelFilter(ClientReturnUrl.return_url, return_url, ModelFilter.EQ))

        if not results:
            return None

        return results[0].client
