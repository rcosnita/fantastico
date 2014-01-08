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
.. py:module:: fantastico.oauth2.tests.test_security_context
'''
from fantastico.oauth2.oauth2_decorators import RequiredScopes
from fantastico.oauth2.security_context import SecurityContext
from fantastico.oauth2.token import Token
from fantastico.tests.base_case import FantasticoUnitTestsCase

class SecurityContextTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for SecurityContext class.'''

    _ATTR_SCOPES = ["scopes", "create", "read", "update", "delete"]

    def test_validate_context_ok_noscopes(self):
        '''This test case ensures a security context is valid when no required scopes are necessary.'''

        access_token = Token({"scopes": ["scope1"]})
        security_ctx = SecurityContext(access_token)

        self.assertTrue(security_ctx.validate_context())

    def test_validate_context_ok_requiredscopes(self):
        '''This test case ensures a security context is valid when some required scopes are found in access token scopes.'''

        for attr_scope in self._ATTR_SCOPES:
            access_token = Token({"scopes": ["scope1", "scope2", "scope3"]})
            required_scopes = ["scope1", "scope3"]
            required_scopes_obj = self._mock_required_scopes_obj(attr_scope, required_scopes)

            security_ctx = SecurityContext(access_token, required_scopes_obj)

            self.assertTrue(security_ctx.validate_context(attr_scope))

    def test_validate_context_invalid(self):
        '''This test case ensures a security context is invalid when required scopes are not found in access_token scopes.'''

        for attr_scope in self._ATTR_SCOPES:
            access_token = Token({"scopes": []})
            required_scopes = ["scope1", "scope2"]
            required_scopes_obj = self._mock_required_scopes_obj(attr_scope, required_scopes)

            security_ctx = SecurityContext(access_token, required_scopes_obj)
            self.assertFalse(security_ctx.validate_context(attr_scope))

    def _mock_required_scopes_obj(self, attr_scopes, required_scopes):
        '''This method builds a mock RequiredScopes which returns for the given attribute the list defined.'''

        kwargs = {attr_scopes: required_scopes}

        return RequiredScopes(**kwargs)
