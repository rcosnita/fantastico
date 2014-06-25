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
.. py:module:: fantastico.oauth2.tests.test_required_scopes
'''
from fantastico.mvc.base_controller import BaseController
from fantastico.oauth2.oauth2_decorators import RequiredScopes
from fantastico.oauth2.security_context import SecurityContext
from fantastico.oauth2.token import Token
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from fantastico.oauth2.exceptions import OAuth2UnauthorizedError

class RequiredScopesTests(FantasticoUnitTestsCase):
    '''This class provides the tests suite for RequiredScopes decorator class.'''

    _controller = None
    _settings_facade = None

    def init(self):
        '''This method is invoked automatically in order to set common dependencies for all test cases.'''

        self._settings_facade = Mock()
        self._controller = MockController(self._settings_facade)

    def test_required_scopes_ok(self):
        '''This test case ensures required_scopes are correctly appended to request security context.'''

        self._test_required_scopes_method(self._controller.do_stuff, ["scope1", "scope2", "scope3"])

    def test_required_scopes_unauthorized(self):
        '''This test case ensures a concrete exception is raised if the requested scopes are not available in
        the current security context.'''
        
        access_token = Token({"scopes": []})

        request = Mock()
        request.context = Mock()
        request.context.security = SecurityContext(access_token)
        
        mock_controller = MockController(Mock())
        
        self.assertRaises(OAuth2UnauthorizedError, lambda: mock_controller.do_stuff(request))

    def test_no_required_scopes_ok(self):
        '''This test case ensures required scopes decorator still works when no scopes are specified.'''

        self._test_required_scopes_method(self._controller.do_stuff_noscopes, [])

    def test_roa_required_on_method_ok(self):
        '''This test case ensures roa required scopes style definition works on method as well.'''

        self._test_required_scopes_method(self._controller.do_stuff_roastyle,
                                          ["sample.create", "sample.read", "sample.update", "sample.delete"])

    def test_generic_scopes_on_method_ok(self):
        '''This test case ensures that scopes are union if ROA + generic scopes style are used.'''

        self._test_required_scopes_method(self._controller.do_stuff_generic,
                                          ["scope1", "scope2", "scope3", "sample.create", "sample.read", "sample.update",
                                           "sample.delete"])

    def test_roa_scopes_on_resource_ok(self):
        '''This test case ensures required scopes are correctly saved in ROA classes.'''

        expected_scopes = sorted(["sample.create", "sample.read", "sample.update", "sample.delete"])

        resource = MockRoaResource()

        required_scopes = MockRoaResource.get_required_scopes()

        self.assertIsInstance(required_scopes, RequiredScopes)
        self.assertEqual(expected_scopes, required_scopes.scopes)
        self.assertEqual(["sample.create"], required_scopes.create_scopes)
        self.assertEqual(["sample.read"], required_scopes.read_scopes)
        self.assertEqual(["sample.update"], required_scopes.update_scopes)
        self.assertEqual(["sample.delete"], required_scopes.delete_scopes)
        self.assertIsInstance(resource, MockRoaResource)

        self.assertEqual(required_scopes, resource.get_required_scopes())

    def _test_required_scopes_method(self, method, expected_scopes):
        '''This method provides a template test case for invoking and asserting result of a method decorated with
        @RequiredScopes.'''

        expected_scopes = sorted(expected_scopes)

        access_token = Token({"scopes": expected_scopes})

        request = Mock()
        request.context = Mock()
        request.context.security = SecurityContext(access_token)

        self.assertIsNone(method(request))

        security_ctx = request.context.security

        self.assertEqual(access_token, security_ctx.access_token)
        self.assertEqual(expected_scopes, security_ctx.required_scopes.scopes)

class MockController(BaseController):
    '''This is a very simple mock object used for testing RequiredScopes decorator.'''

    @RequiredScopes(scopes=["scope1", "scope2", "scope3"])
    def do_stuff(self, request):
        pass

    @RequiredScopes(scopes="")
    def do_stuff_noscopes(self, request):
        pass

    @RequiredScopes(create="sample.create",
                    read="sample.read",
                    update="sample.update",
                    delete="sample.delete")
    def do_stuff_roastyle(self, request):
        pass

    @RequiredScopes(scopes=["scope1", "scope2", "scope3"],
                    create="sample.create",
                    read=["sample.read", "sample.read"],
                    update="sample.update",
                    delete="sample.delete")
    def do_stuff_generic(self, request):
        pass

@RequiredScopes(create="sample.create",
                read="sample.read",
                update="sample.update",
                delete="sample.delete")
class MockRoaResource(object):
    '''This class is used to ensure RequiredScopes decorator can safely be used on Mocked resources.'''
