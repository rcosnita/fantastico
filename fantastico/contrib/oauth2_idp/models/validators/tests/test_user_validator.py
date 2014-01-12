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
.. py:module:: fantastico.oauth2_idp.models.tests.test_user_validator
'''
from fantastico.contrib.oauth2_idp.models.persons import Person
from fantastico.contrib.oauth2_idp.models.users import User
from fantastico.contrib.oauth2_idp.models.validators.user_validator import UserValidator
from fantastico.oauth2.passwords_hasher_factory import PasswordsHasherFactory
from fantastico.roa.roa_exceptions import FantasticoRoaError
from fantastico.tests.base_case import FantasticoUnitTestsCase
from fantastico.utils.dictionary_object import DictionaryObject
from mock import Mock
from webob.request import Request

class UserValidatorTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for UserValidator.'''

    _validator = None
    _hasher = None
    _model_facade_cls = None
    _person_facade = None
    _conn_manager = None
    _db_conn = None

    def init(self):
        self._hasher = Mock()
        self._hasher.get_hasher = Mock(return_value=self._hasher)
        hasher_factory = Mock(return_value=self._hasher)

        self._person_facade = Mock()
        self._model_facade_cls = Mock(return_value=self._person_facade)

        self._conn_manager = Mock()
        self._db_conn = Mock()
        self._conn_manager.get_connection = Mock(return_value=self._db_conn)

        self._validator = UserValidator(password_hasher_factory=hasher_factory, model_facade_cls=self._model_facade_cls,
                                        conn_manager=self._conn_manager)

        hasher_factory.assert_called_once_with()
        self._hasher.get_hasher.assert_called_once_with(PasswordsHasherFactory.SHA512_SALT)

    def test_format_resource_ok(self):
        '''This test case ensures format_resource works correctly for an expected resource.'''

        desc = {"username": "abcd", "password": "1234567"}
        resource = DictionaryObject(desc, immutable=False)

        self._validator.format_resource(resource, None)

        self.assertEqual(desc["username"], resource.username)
        self.assertTrue("password" not in desc)

    def test_format_resource_none_ok(self):
        '''This test case ensures validation works correctly even when resource does not contain keys.'''

        desc = {}
        resource = DictionaryObject(desc, immutable=False)

        self._validator.format_resource(resource, None)

        self.assertEqual(desc, {})

    def test_validate_user_new(self):
        '''This test case ensures validation works correctly when the user is new (user_id is not known) - POST.'''

        request = Request.blank("/test", {})
        request.method = 'POST'

        resource = User(username="john.doe@gmail.com", password="123abcd")

        self._test_validate_user_template(resource, request)

    def test_validate_user_update(self):
        '''This test case ensures validation works correctly for existing users.'''

        request = Request.blank("/test", {})
        request.method = 'PUT'

        resource = User(username="john.doe@gmail.com", password="123abcd")
        resource.user_id = 55

        self._test_validate_user_template(resource, request)

    def test_validate_user_missingusername(self):
        '''This test case ensures an exception is raised if username is attribute is not sent.'''

        for resource in [User(), User(username=None), User(username=""), User(username="    ")]:
            with self.assertRaises(FantasticoRoaError) as ctx:
                self._validator.validate(resource, Mock())

            self.assertTrue(str(ctx.exception).find("username") > -1, "Username not found in exception text.")

    def test_validate_user_usernamenotemail(self):
        '''This test case ensures an exception is raised if username attribute is not a valid email address.'''

        resource = User(username="john.doe")

        with self.assertRaises(FantasticoRoaError) as ctx:
            self._validator.validate(resource, Mock())

        msg = str(ctx.exception)

        self.assertTrue(msg.find("username") > -1, "Username not found in exception text.")
        self.assertTrue(msg.find("email") > -1, "Email not found in exception text.")

    def test_validate_user_missingpasswd_create(self):
        '''This test case ensures an exception is raised if password is empty on create.'''

        request = Request.blank("/test", {})
        request.method = "POST"

        for resource in [User(username="admin@fantastico.com"),
                         User(username="admin@fantastico.com"),
                         User(username="admin@fantastico.com", password="   ")]:
            with self.assertRaises(FantasticoRoaError) as ctx:
                self._validator.validate(resource, request)

            self.assertTrue(str(ctx.exception).find("password") > -1, "Password not found in exception text.")

    def test_validate_user_missingpasswd_update(self):
        '''This test case ensures an exception is raised if passowrd is not present in dictionary when trying to update
        an existing user.'''

        request = Request.blank("/test", {})
        request.method = "PUT"

        for resource in [User(username="admin@fantastico.com"), User(username="admin@fantastico.com", password="   ")]:
            with self.assertRaises(FantasticoRoaError) as ctx:
                self._validator.validate(resource, request)

            self.assertTrue(str(ctx.exception).find("password") > -1, "Password not found in exception text.")

    def test_validate_personid_error(self):
        '''This test case ensures that an exception is raised if for create / update operations body contains person id.'''

        request = Request.blank("/test", {})

        for method in ["POST", "PUT"]:
            resource = User(username="john.doe@gmail.com", password="123456", person_id=5)

            request.method = method

            with self.assertRaises(FantasticoRoaError) as ctx:
                self._validator.validate(resource, request)

            self.assertTrue(str(ctx.exception).find("person_id") > -1)

    def _test_validate_user_template(self, resource, request):
        '''This method provides a template for validate user test cases.'''

        request.request_id = 9876

        default_person = Person(first_name="-", last_name="-", email_address=resource.username)
        person_id = 1

        plain_passwd = resource.password
        user_id = resource.user_id

        hashed_passwd = "123"

        self._hasher.hash_password = Mock(return_value=hashed_passwd)

        if request.method.lower() == "post":
            self._person_facade.new_model = Mock(return_value=default_person)
            self._person_facade.create = Mock(return_value=[person_id])

        self._validator.validate(resource, request)

        self.assertEqual(hashed_passwd, resource.password)
        self._hasher.hash_password.assert_called_once_with(plain_passwd, DictionaryObject({"salt": user_id}))

        if request.method.lower() == "post":
            self.assertEqual(person_id, resource.person_id)

            self._model_facade_cls.assert_called_once_with(Person, self._db_conn)
            self._conn_manager.get_connection.assert_called_once_with(request.request_id)
            self._person_facade.new_model.assert_called_once_with(first_name="-", last_name="-", email_address=resource.username)
            self._person_facade.create.assert_called_once_with(default_person)
