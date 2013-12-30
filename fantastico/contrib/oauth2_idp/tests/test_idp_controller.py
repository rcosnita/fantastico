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
.. py:module:: fantastico.contrib.oauth2_idp.tests.test_idp_controller
'''

from fantastico.contrib.oauth2_idp.models.users import User
from fantastico.mvc.models.model_filter import ModelFilter
from fantastico.oauth2.exceptions import OAuth2MissingQueryParamError
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
import base64
import hashlib
import urllib

class IdpControllerTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for oauth2 fantastico identity provider controller.'''

    _IDP_CLIENTID = "11111111-1111-1111-1111-111111111111"
    _TPL_LOGIN = "/mock/location/views/login.html"

    _idp_controller = None

    def init(self):
        '''This method is invoked automatically in order to setup dependencies common to all test cases.'''

        from fantastico.contrib.oauth2_idp.idp_controller import IdpController

        oauth2_idp = {"client_id": self._IDP_CLIENTID,
                      "template": self._TPL_LOGIN}

        settings_facade = Mock()
        settings_facade.get = Mock(return_value=oauth2_idp)
        self._idp_controller = IdpController(settings_facade)

        settings_facade.get.assert_called_once_with("oauth2_idp")

    def test_show_login_ok(self):
        '''This test case ensures login screen is displayed correctly when all required parameters are passed.'''

        request = Mock()
        request.params = {"return_url": "/simple/test"}

        self._idp_controller.load_template = Mock(return_value="cool result")

        response = self._idp_controller.show_login(request)

        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)

        self.assertIsNotNone(response.body)
        body = response.body.decode()

        self.assertEqual("cool result", body)

        self._idp_controller.load_template.assert_called_once_with(
                                        self._TPL_LOGIN,
                                        {"return_url": urllib.parse.quote(request.params["return_url"])})

    def test_show_login_missingreturn(self):
        '''This test case ensures login screen is not displayed if return_url query parameter is not provided.'''

        request = Mock()
        request.params = {}

        for return_url in [None, "", "    "]:
            request.params["return_url"] = return_url

            with self.assertRaises(OAuth2MissingQueryParamError) as ctx:
                self._idp_controller.show_login(request)

            self.assertEqual("return_url", ctx.exception.param_name)

    def test_authenticate_ok(self):
        '''This test case ensures a correct login token is generated during authentication phase. It also checks for correct
        redirect response.'''

        request = Mock()

        user_id = 123
        password = "12345"
        hashed_password = base64.b64encode(hashlib.sha512((password + str(user_id)).encode()).hexdigest().encode()).decode()

        user = User("john.doe@email.com", hashed_password, 5)
        user.user_id = 123

        model_facade = Mock()
        model_facade_cls = Mock(return_value=model_facade)

        model_facade.get_records_paged = Mock(return_value=user)

        self._idp_controller.authenticate(request)

        model_facade_cls.assert_called_once_with(User)
        model_facade.get_records_paged.assert_called_with(
                                            start_record=0, end_record=1,
                                            filter_expr=ModelFilter(User.username, user.username, ModelFilter.EQ))
        model_facade.get_records_paged.assert_called_with(
                                            start_record=0, end_record=1,
                                            filter_expr=ModelFilter(User.password, hashed_password, ModelFilter.EQ))
