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
.. py:module:: fantastico.mvc.static_assets_controller
'''
from fantastico.mvc.base_controller import BaseController
from fantastico.mvc.controller_decorators import Controller, ControllerProvider
from webob.response import Response
import mimetypes
import os

@ControllerProvider()
class StaticAssetsController(BaseController):
    '''This class provides a generic handler for static assets. It is used only by dev server and it does not
    ensure correct http client side caching. In production, only the web server serves static assets and
    Fantastico wsgi server is bypassed.'''
    
    @Controller(url="(?P<component_name>.*)/static/(?P<asset_path>.*)$")
    def serve_asset(self, request, component_name, asset_path, os_provider=os, file_loader=None):
        '''This method is invoked whenever a request to a static asset is done.'''
        
        file_path = "%s%s%s" % (self._settings_facade.get_root_folder(), component_name, asset_path)
        err_content_type="text/html; charset=UTF-8"
        
        if not component_name or len(component_name.strip()) == 0:
            return Response(status=400, content_type=err_content_type, text="No component name provided.")
        
        if not asset_path or len(asset_path.strip()) == 0:
            return Response(status=400, content_type=err_content_type, text="No asset path provided.")
        
        if not self._is_asset_available(file_path, os_provider):
            return Response(status=404, content_type=err_content_type, text="Asset %s not found." % file_path)
        
        file_loader = request.environ.get("wsgi.file_wrapper") or file_loader
        
        file_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        
        return Response(body=file_loader(os_provider.open(file_path)), content_type=file_type)
    
    def _is_asset_available(self, file_path, os_provider=os):
        '''This method detects if an asset exists on disk or not.'''

        if not os_provider.path.exists(file_path):
            return False
        
        return True