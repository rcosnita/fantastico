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
.. py:module:: fantastico.contrib.oauth2_idp.models.validators.person_validator
'''

from fantastico import mvc
from fantastico.mvc.model_facade import ModelFacade
from fantastico.oauth2.exceptions import OAuth2UnauthorizedError
from fantastico.roa.resource_validator import ResourceValidator
from fantastico.roa.roa_exceptions import FantasticoRoaMethodNotSupportedError, FantasticoRoaError

class PersonValidator(ResourceValidator):
    '''This class provides the validation logic for person objects submitted through API. Moreover, it raises Method not allowed
    exceptions for GET / POST / DELETE operations.'''

    def __init__(self, model_facade_cls=ModelFacade, conn_manager=None):
        self._model_facade_cls = model_facade_cls
        self._conn_manager = conn_manager or mvc.CONN_MANAGER

    def validate(self, resource, request, existing_resource_id=None):
        '''This method validates the given resource to ensure it has all mandatory fields and that it belongs to the currently
        logged in user.'''

        if request.method.lower() == "post":
            raise FantasticoRoaMethodNotSupportedError("Method %s is not supported by Person resource." % request.method)

        self.validate_missing_attr(resource, "first_name")
        self.validate_missing_attr(resource, "last_name")
        self.validate_missing_attr(resource, "email_address")

        if resource.person_id:
            raise FantasticoRoaError("You can not specify person_id for update operations.")

        self._is_owned_by(request.context.security.access_token.user_id, existing_resource_id, request.request_id)

    def _is_owned_by(self, user_id, existing_resource_id, request_id):
        '''This method raises an exception if the resource is not owned by the expected user id.'''

        from fantastico.contrib.oauth2_idp.models.users import User

        user_facade = self._model_facade_cls(User, self._conn_manager.get_connection(request_id))

        user = user_facade.find_by_pk({User.user_id: user_id})

        if user.person_id != int(existing_resource_id):
            raise OAuth2UnauthorizedError("Insufficient privileges to update person.")

    def format_resource(self, resource, request):
        '''This method ensures GET operations will fail on Persons.'''

        raise FantasticoRoaMethodNotSupportedError("Method GET is not supported by Person resource.")
