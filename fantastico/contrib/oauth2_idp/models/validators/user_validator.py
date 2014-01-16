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
.. py:module:: fantastico.contrib.oauth2_idp.models.validators.user_validator
'''
from fantastico import mvc
from fantastico.contrib.oauth2_idp.models.persons import Person
from fantastico.mvc.model_facade import ModelFacade
from fantastico.oauth2.passwords_hasher_factory import PasswordsHasherFactory
from fantastico.roa.resource_validator import ResourceValidator
from fantastico.roa.roa_exceptions import FantasticoRoaError
from fantastico.utils.dictionary_object import DictionaryObject
from validate_email import validate_email
from fantastico.exceptions import FantasticoDbError

class UserValidator(ResourceValidator):
    '''This class provides the user validator logic.'''

    def __init__(self, password_hasher_factory=PasswordsHasherFactory, model_facade_cls=ModelFacade,
                 conn_manager=None):
        self._passwd_hasher = password_hasher_factory().get_hasher(PasswordsHasherFactory.SHA512_SALT)
        self._model_facade_cls = model_facade_cls
        self._conn_manager = conn_manager or mvc.CONN_MANAGER

    def validate(self, resource, request, existing_resource_id=None):
        '''This method provides the validation logic for a submitted user representation. Additionally it hashes the
        sent password.'''

        self._validate_username(resource)

        self._validate_password(resource, request)

        self._validate_person(resource, request)

    def format_resource(self, resource, request):
        '''This method suppress user password from being sent to GET calls.'''

        resource.password = None

    def _validate_username(self, resource):
        '''This method validates the username from submitted resource.'''

        if not resource.username or len(resource.username.strip()) == 0:
            raise FantasticoRoaError("username attribute is mandatory.")

        if not validate_email(resource.username):
            raise FantasticoRoaError("username attribute must be a valid email address.")

    def _validate_password(self, resource, request):
        '''This method validates the password from submitted resource. Additionally plain text passwords are hashed.'''

        plain_passwd = resource.password

        if request.method.lower() == "post" and (not (plain_passwd or "") or len(plain_passwd.strip()) == 0):
            raise FantasticoRoaError("password attribute is mandatory when creating a new user.")

        if request.method.lower() == "put" and (not (plain_passwd or "") or len(plain_passwd.strip()) == 0):
            raise FantasticoRoaError("password attribute is mandatory when creating a new user.")

        self._hash_password(resource)

    def _hash_password(self, resource):
        '''This method hashes the password from the given resource.'''

        hash_ctx = {"salt": resource.user_id}
        resource.password = self._passwd_hasher.hash_password(resource.password, DictionaryObject(hash_ctx))

    def _validate_person(self, resource, request):
        '''This method ensures person_id attribute is not set for resource. Additionally if the resource is new a default person
        gets created.'''

        if resource.person_id:
            raise FantasticoRoaError("person_id can not be specified when creating / updating an user.")

        if request.method.lower() != "post":
            return

        try:
            person_facade = self._model_facade_cls(Person, self._conn_manager.get_connection(request.request_id))
            person = person_facade.new_model(first_name="-", last_name="-", email_address=resource.username)
            person_id = person_facade.create(person)

            resource.person_id = person_id[0]
        except FantasticoDbError as ex:
            raise FantasticoRoaError("Unable to create default person: %s" % str(ex))
