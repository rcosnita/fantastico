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
.. py:module:: fantastico.contrib.oauth2_idp.models.validators.tests.test_person_validator
'''
from fantastico.contrib.oauth2_idp.models.persons import Person
from fantastico.contrib.oauth2_idp.models.users import User
from fantastico.contrib.oauth2_idp.models.validators.person_validator import PersonValidator
from fantastico.oauth2.exceptions import OAuth2UnauthorizedError
from fantastico.oauth2.security_context import SecurityContext
from fantastico.oauth2.token import Token
from fantastico.roa.roa_exceptions import FantasticoRoaError, FantasticoRoaMethodNotSupportedError
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock

class PersonValidatorTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for person validator.'''

    _model_facade = None
    _model_facade_cls = None
    _conn_manager = None
    _db_conn = None
    _validator = None

    def init(self):
        '''This method is invoked before each test case run in order to set common dependencies.'''

        self._model_facade = Mock()
        self._model_facade_cls = Mock(return_value=self._model_facade)

        self._db_conn = Mock()
        self._conn_manager = Mock()
        self._conn_manager.get_connection = Mock(return_value=self._db_conn)

        self._validator = PersonValidator(model_facade_cls=self._model_facade_cls, conn_manager=self._conn_manager)

    def test_validate_post_notsupported(self):
        '''This test case ensures creation of new persons through api always fails.'''

        request = Mock()
        request.method = "POST"

        with self.assertRaises(FantasticoRoaMethodNotSupportedError):
            self._validator.validate({}, request)

    def test_format_notsupported(self):
        '''This test case ensures retrieval of persons through api always fails.'''

        with self.assertRaises(FantasticoRoaMethodNotSupportedError):
            self._validator.format_resource({}, Mock())

    def test_format_collection_notsupported(self):
        '''This test case ensures retrieval of persons collection through api allways fails.'''

        with self.assertRaises(FantasticoRoaMethodNotSupportedError):
            self._validator.format_collection([{}, {}], Mock())

    def test_validate_missing_firstname(self):
        '''This test case ensures missing first name generates a roa error.'''

        for resource in [None, Person(), Person(first_name=""), Person(first_name="     ")]:
            self._validate_missing_attr("first_name", resource)

    def test_validate_missing_lastname(self):
        '''This test case ensures missing first name generates a roa error.'''

        for resource in [Person(first_name="John", last_name=None),
                         Person(first_name="John", last_name=""),
                         Person(first_name="John", last_name="    ")]:
            self._validate_missing_attr("last_name", resource)

    def test_validate_personid_given(self):
        '''This test case ensures an exception is raised if person id attribut is specified in resource.'''

        resource = Person(first_name="John", last_name="Doe", email_address="john.doe@mail.com")
        resource.person_id = 1

        with self.assertRaises(FantasticoRoaError) as ctx:
            self._validator.validate(resource, Mock(), existing_resource_id=5)

        self.assertTrue(str(ctx.exception).find("person_id") > -1, "person_id is expected in exception message.")

    def test_validate_notowned_by(self):
        '''This test case ensures validate fails if the current person does not have the current logged in user associated with
        it.'''

        resource = Person(first_name="John", last_name="Doe", email_address="john.doe@gmail.com")

        with self.assertRaises(OAuth2UnauthorizedError):
            self._test_validate_owned_by_user(resource, 1, person_id=10)

    def test_validate_ok(self):
        '''This test case ensures validate succeeds if all mandatory fields are provided and person has current logged in user
        associated to it.'''

        resource = Person(first_name="John", last_name="Doe", email_address="john.doe@gmail.com")

        self._test_validate_owned_by_user(resource, 1, person_id=1)

    def _test_validate_owned_by_user(self, resource, user_id, person_id):
        '''This method provides a template for testing validation for scenarios where resource belongs / does not belong to
        expected user.'''

        token = Token({"user_id": user_id, "scopes": []})

        request = Mock()
        request.request_id = 1
        request.context = Mock()
        request.context.security = SecurityContext(token)

        self._model_facade.find_by_pk = Mock(return_value=User(person_id=1))

        self._validator.validate(resource, request, person_id)

        self._conn_manager.get_connection.assert_called_once_with(request.request_id)
        self._model_facade_cls.assert_called_once_with(User, self._db_conn)
        self._model_facade.find_by_pk.assert_called_once_with({User.user_id: token.user_id})

    def test_validate_missing_email(self):
        '''This test case ensures missing email address generates a roa error.'''

        for resource in [Person(first_name="John", last_name="Doe", email_address=None),
                         Person(first_name="John", last_name="Doe", email_address=""),
                         Person(first_name="John", last_name="Doe", email_address="     ")]:
            self._validate_missing_attr("email_address", resource)

    def _validate_missing_attr(self, attr_name, resource):
        '''This method provides a template for asserting missing attributes during validation.'''

        with self.assertRaises(FantasticoRoaError) as ctx:
            self._validator.validate(resource, Mock())

        self.assertTrue(str(ctx.exception).find(attr_name) > -1)
