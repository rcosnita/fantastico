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
from fantastico.oauth2.passwords_hasher_factory import PasswordsHasherFactory
from fantastico.roa.resource_validator import ResourceValidator
from fantastico.roa.roa_exceptions import FantasticoRoaError
from fantastico.utils.dictionary_object import DictionaryObject
from validate_email import validate_email

class UserValidator(ResourceValidator):
    '''This class provides the user validator logic.'''

    def __init__(self, password_hasher_factory=PasswordsHasherFactory):
        self._passwd_hasher = password_hasher_factory().get_hasher(PasswordsHasherFactory.SHA512_SALT)

    def validate(self, resource, request):
        '''This method provides the validation logic for a submitted user representation. Additionally it hashes the
        sent password.'''

        self._validate_username(resource)

        self._validate_password(resource, request)

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
