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
.. py:module:: fantastico.mvc.tests.test_static_assets_controller
'''

from fantastico.mvc.static_assets_controller import StaticAssetsController
from fantastico.tests.base_case import FantasticoUnitTestsCase
from mock import Mock
from sqlalchemy.exc import NotSupportedError
from fantastico.settings import BasicSettings

class StaticAssetsControllerTests(FantasticoUnitTestsCase):
    '''This class provides the test suite for checking static assets are correctly handled by static controller.'''
    
    def init(self):
        self._settings_facade = Mock()
        self._settings_facade.get_config = Mock(return_value=TestProfileNotUsed())
        self._assets_contr = StaticAssetsController(self._settings_facade)
        self._os_provider = Mock()
        
    def test_serve_asset_no_component(self):
        '''This test case makes sure serve asset returns bad request if no component name is provided.'''
        
        for component_name in [None, "", "      "]:
            response = self._assets_contr.serve_asset(Mock(), component_name, "/valid/path")
            
            self.assertIsNotNone(response)
            self.assertEqual("text/html", response.content_type)
            self.assertEqual("UTF-8", response.charset)
            self.assertEqual(400, response.status_code)
    
    def test_serve_asset_no_path(self):
        '''This test case makes sure serve asset returns bad request if no asset path is provided.'''
        
        component_name = "component1"
        
        for asset_path in [None, "", "      "]:
            response = self._assets_contr.serve_asset(Mock(), component_name, asset_path)
            
            self.assertIsNotNone(response)
            self.assertEqual("text/html", response.content_type)
            self.assertEqual("UTF-8", response.charset)            
            self.assertEqual(400, response.status_code)

    def test_serve_asset_not_found(self):
        '''This test case makes sure a 404 response is retrieved if asset request is not found.'''
        
        component_name = "component1"
        asset_path ="images/not_found.png"
        
        self._mock_os_provider(component_name, asset_path, False)
        
        response = self._assets_contr.serve_asset(Mock(), component_name, asset_path, 
                                                  os_provider=self._os_provider)
        
        self.assertIsNotNone(response)
        self.assertEqual("text/html", response.content_type)
        self.assertEqual("UTF-8", response.charset)
        self.assertEqual(404, response.status_code)
    
    def test_serve_asset_ok(self):
        '''This test case makes sure valid assets are retrieved correctly to the client.'''

        component_name = "component1"
        asset_path ="images/image.png"
        
        self._mock_os_provider(component_name, asset_path)
        
        content = b"simple test"
        
        request = Mock()
        request.environ = {}
        
        response = self._assets_contr.serve_asset(request, component_name, asset_path, 
                                                  os_provider=self._os_provider,
                                                  file_loader=Mock(return_value=content),
                                                  file_opener=Mock())
        
        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)
        self.assertEqual("image/png", response.content_type)
        self.assertEqual(content, response.app_iter)
    
    def test_serve_asset_unknown_mimetype(self):
        '''This test case ensures a default mimetype is detected if the given file has an unknown extension.'''
        
        component_name = "component1"
        asset_path ="images/image.unknown"
        
        self._mock_os_provider(component_name, asset_path)
        
        content = b"simple test"
        
        request = Mock()
        request.environ = {}
        
        response = self._assets_contr.serve_asset(request, component_name, asset_path, 
                                                  os_provider=self._os_provider,
                                                  file_loader=Mock(return_value=content),
                                                  file_opener=Mock())
        
        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/octet-stream", response.content_type)
        self.assertEqual(content, response.app_iter)
    
    def test_favicon_ok(self):
        '''This test case ensures favicon is loaded correctly if it exists.'''
        
        component_name = "static"
        asset_path = "favicon.ico"
        
        self._mock_os_provider(component_name, asset_path, 
                               file_exists=True, 
                               static_local=False)
        
        content = b"simple test"
        
        request = Mock()
        request.environ = {}
        
        response = self._assets_contr.handle_favicon(request,
                                                     os_provider=self._os_provider,
                                                     file_loader=Mock(return_value=content),
                                                     file_opener=Mock())
        
        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.content_type in ["image/vnd.microsoft.icon", "image/x-icon"])
        self.assertEqual(content, response.app_iter)
    
    def test_favicon_not_found(self):
        '''This test case makes sure an empty response is retrieved if the icon is not found.'''
        
        component_name = "static"
        asset_path = "favicon.ico"
        
        self._mock_os_provider(component_name, asset_path, 
                               file_exists=False, 
                               static_local=False)
        
        request = Mock()
        request.environ = {}
        
        response = self._assets_contr.handle_favicon(request,
                                                     os_provider=self._os_provider)
        
        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.content_type in ["image/vnd.microsoft.icon", "image/x-icon"])
        self.assertEqual(0, len(response.app_iter))        
    
    def _mock_os_provider(self, component_name, asset_path, file_exists=True, static_local=True):
        '''This method correctly mocks the os provider based on the component name and asset path.'''

        self._os_provider.path = Mock(return_value=self._os_provider)
        
        def exists(filename):
            if static_local:
                computed_path = "/mvc/tests/%(component_name)s/static/%(asset_path)s" %\
                                {"component_name": component_name, 
                                 "asset_path": asset_path}
            else:
                computed_path = "/mvc/tests/%(component_name)s/%(asset_path)s" %\
                                {"component_name": component_name, 
                                 "asset_path": asset_path}                

            if filename.endswith(computed_path):
                return file_exists
            
            raise NotSupportedError()
            
        self._os_provider.path.exists = exists

class TestProfileNotUsed(BasicSettings):
    '''This class is used only for correctly mocking a settings profile.'''