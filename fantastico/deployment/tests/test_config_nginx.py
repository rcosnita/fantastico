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
.. py:module:: fantastico.deployment.tests.test_config_nginx
'''
from fantastico.deployment.config_nginx import ConfigNginx
from fantastico.settings import BasicSettings
from fantastico.tests.base_case import FantasticoUnitTestsCase
from fantastico.utils import instantiator
from jinja2.environment import Template, Environment
from jinja2.loaders import FileSystemLoader
from mock import Mock
import os

class ConfigNginxTests(FantasticoUnitTestsCase):
    '''This class provides the test suite for checking the correct behavior of config nginx script.'''
    
    def init(self):
        self._os_provider = Mock()
        self._config_nginx = ConfigNginx(os_provider=self._os_provider, 
                                         args=["python_script.py", "/etc/nginx"])
        
        self.assertEqual("python_script.py", self._config_nginx.script_name)
        self.assertEqual("/etc/nginx", self._config_nginx.nginx_conf_folder)
    
    def test_noargs_invalid(self):
        '''This test case ensures an exception is raised if nginx location is not specified.'''
        
        with self.assertRaises(ValueError):
            ConfigNginx()
    
    def test_conf_folder_inexistent(self):
        '''This test case ensures an exception is raised when nginx location folder does not exist.'''
        
        self._os_provider.path = self._os_provider
        self._os_provider.exists = Mock(return_value=False)
        
        with self.assertRaises(IOError):
            self._config_nginx()
    
    def test_conf_generated_ok(self):
        '''This test case ensures configuration file is generated correctly and added to nginx enabled sites.'''
        
        root_folder = os.path.abspath(instantiator.get_class_abslocation(BasicSettings) + "../")        
        
        tpl_loader = FileSystemLoader(searchpath=root_folder)
        tpl_env = Environment(loader=tpl_loader)
        
        config_data = {"ip_address": "127.0.0.1",
                       "vhost_name": "test-app.com",
                       "http_port": 80,
                       "uwsgi_port": 12090,
                       "root_folder": "/test/folder/vhost",
                       "modules_folder": "/fantastico/modules"}
        
        expected_config = tpl_env.get_template("/deployment/conf/nginx/fantastico-wsgi").render(config_data)
        
        def keyboard_read(msg):
            if msg.lower().find("address") > -1:
                return "127.0.0.1"
            
            if msg.lower().find("vhost") > -1:
                return "test-app.com"
            
            if msg.lower().find("http port") > -1:
                return 80
            
            if msg.lower().find("uwsgi port") > -1:
                return 12090
            
            if msg.lower().find("root folder") > -1:
                return "/test/folder/vhost"
            
            if msg.lower().find("modules folder") > -1:
                return "/fantastico/modules"
            
            raise NotImplementedError()

        config = self._config_nginx(keyboard_read)
        
        self.assertEqual(expected_config, config)