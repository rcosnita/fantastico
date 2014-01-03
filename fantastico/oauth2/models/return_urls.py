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
.. py:module:: fantastico.oauth2.models.return_urls
'''
from fantastico.mvc import BASEMODEL
from fantastico.oauth2.models.clients import Client
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String

class ClientReturnUrl(BASEMODEL):
    '''This class provides the return urls entity used to describe valid return urls of a client.'''

    __tablename__ = "oauth2_client_returnurls"

    url_id = Column("url_id", Integer, primary_key=True, autoincrement=True)
    client_id = Column("client_id", String(32), ForeignKey("oauth2_clients.client_id"))
    client = relationship(Client, primaryjoin=client_id == Client.client_id, backref="return_urls")
    return_url = Column("return_url", String(255), nullable=False)

    def __init__(self, client_id=None, return_url=None):
        self.client_id = client_id
        self.return_url = return_url
