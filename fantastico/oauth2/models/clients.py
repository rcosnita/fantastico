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
.. py:module:: fantastico.oauth2.models.clients
'''

from fantastico.mvc import BASEMODEL
from fantastico.oauth2.models.scopes import Scope
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, Table, ForeignKey
from sqlalchemy.types import String, Boolean, Text, Integer

CLIENT_SCOPES_ASSOC = Table("oauth2_client_scopes", BASEMODEL.metadata,
                            Column("client_id", Integer, ForeignKey("oauth2_clients.client_id")),
                            Column("scope_id", Integer, ForeignKey("oauth2_scopes.scope_id")))

class Client(BASEMODEL):
    '''This class provides the model for oauth2 clients.'''

    __tablename__ = "oauth2_clients"

    client_id = Column("client_id", String(36), primary_key=True)
    name = Column("name", String(100), nullable=False)
    description = Column("description", Text, nullable=False)
    grant_types = Column("grant_types", String(200), nullable=False)
    token_iv = Column("token_iv", String(256), nullable=False)
    token_key = Column("token_key", String(256), nullable=False)
    revoked = Column("revoked", Boolean, nullable=False)

    scopes = relationship(Scope, secondary="oauth2_client_scopes")

    def __init__(self, client_id=None, name=None, description=None, grant_types=None, token_iv=None, token_key=None,
                 revoked=None):
        self.client_id = client_id
        self.name = name
        self.description = description
        self.grant_types = grant_types
        self.token_iv = token_iv
        self.token_key = token_key
        self.revoked = revoked
