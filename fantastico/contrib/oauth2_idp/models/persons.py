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
.. py:module::
'''
from fantastico.mvc import BASEMODEL
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

class Person(BASEMODEL):
    '''This class provides the entity for a person supported by the OAuth2 default Identity provider. A person can have one or
    more users associated.'''

    __tablename__ = "oauth2_idp_persons"

    person_id = Column("person_id", Integer, primary_key=True, autoincrement=True)
    first_name = Column("first_name", String(100), nullable=False)
    last_name = Column("last_name", String(50), nullable=False)
    email_address = Column("email_address", String(100), nullable=False)
    cell_number = Column("cell_number", String(30))
    phone_number = Column("phone_number", String(30))

    def __init__(self, first_name=None, last_name=None, email_address=None, cell_number=None, phone_number=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.cell_number = cell_number
        self.phone_number = phone_number
