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
.. py:module:: fantastico.contrib.oauth2_idp.models.users
'''
from fantastico.contrib.oauth2_idp.models.persons import Person
from fantastico.contrib.oauth2_idp.models.validators.user_validator import UserValidator
from fantastico.mvc import BASEMODEL
from fantastico.oauth2.oauth2_decorators import RequiredScopes
from fantastico.roa.resource_decorator import Resource
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String

@Resource(name="User", url="/oauth-idp-profile", version=1.0, user_dependent=True,
          subresources={"person": ["person_id"]},
          validator=UserValidator)
@RequiredScopes(read=["user.profile.read"],
                update=["user.profile.update"],
                delete=["user.profile.delete"])
class User(BASEMODEL):
    '''This class provides the entity for describing a user supported by OAuth2 default Identity provider. A user is assigned
    complements information found in person entity.'''

    __tablename__ = "oauth2_idp_users"

    user_id = Column("user_id", Integer, primary_key=True, autoincrement=True)
    username = Column("username", String(100), nullable=False)
    password = Column("password", String(256), nullable=False)

    person_id = Column("person_id", ForeignKey("oauth2_idp_persons.person_id"), nullable=False)
    person = relationship(Person, primaryjoin=person_id == Person.person_id)

    def __init__(self, username=None, password=None, person_id=None):
        self.username = username
        self.password = password
        self.person_id = person_id
