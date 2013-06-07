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
from fantastico.utils import instantiator
from webob.response import Response
import mimetypes
import os

class StaticAssetsController(BaseController):
    '''This class provides a generic handler for static assets. It is used only by dev server and it does not
    ensure correct http client side caching. In production, only the web server serves static assets and
    Fantastico wsgi server is bypassed.'''
    
    @property
    def static_folder(self):
        '''This property returns the static folder locatio for fantastico framework. Currently this is set to 
        **static**.'''
        
        return "static"
    
    def serve_asset(self, request, component_name, asset_path, **kwargs):
        '''This method is invoked whenever a request to a static asset is done.'''

        file_path = "%s%s/%s/%s" % (instantiator.get_class_abslocation(self._settings_facade.get_config().__class__), 
                                    component_name, self.static_folder, asset_path)
        err_content_type = "text/html; charset=UTF-8"
        
        if not component_name or len(component_name.strip()) == 0:
            return Response(status=400, content_type=err_content_type, text="No component name provided.")
        
        if not asset_path or len(asset_path.strip()) == 0:
            return Response(status=400, content_type=err_content_type, text="No asset path provided.")
        
        os_provider = kwargs.get("os_provider") or os        
        
        if not self._is_asset_available(file_path, os_provider):
            return Response(status=404, content_type=err_content_type, text="Asset %s not found." % file_path)
         
        return self._load_file_from_disk(request, file_path, **kwargs)
    
    def handle_favicon(self, request, **kwargs):
        '''This method is used to handle favicon requests coming from browsers.'''
        
        os_provider = kwargs.get("os_provider") or os

        file_path = "%sstatic/%s" % (instantiator.get_class_abslocation(self._settings_facade.get_config().__class__), 
                                 "favicon.ico")
        
        if not os_provider.path.exists(file_path):
            return Response(app_iter=[], content_type="image/x-icon")
        
        return self._load_file_from_disk(request, file_path, **kwargs)
    
    def _is_asset_available(self, file_path, os_provider=os):
        '''This method detects if an asset exists on disk or not.'''

        if not os_provider.path.exists(file_path):
            return False
        
        return True
    
    def _load_file_from_disk(self, request, file_path, **kwargs):
        '''This method is used to load a file from disk if it exists.'''
        
        os_provider = kwargs.get("os_provider") or os
        err_content_type = "text/html; charset=UTF-8"
        
        if not self._is_asset_available(file_path, os_provider):
            return Response(status=404, content_type=err_content_type, text="Asset %s not found." % file_path)
         
        file_loader = kwargs.get("file_loader") or request.environ.get("wsgi.file_wrapper")
        
        file_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        
        file_opener = kwargs.get("file_opener") or open
        file_content = file_loader(file_opener(file_path, "rb"))
        
        return Response(app_iter=file_content, content_type=file_type)