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
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
from mock import Mock
import os
from argparse import ArgumentParser

class ConfigNginxTests(FantasticoUnitTestsCase):
    '''This class provides the test suite for checking the correct behavior of config nginx script.'''
    
    def mocked_error(self, err_msg):
        '''This method is used to replace argparse error handling method.'''
        
        raise ValueError(err_msg)
    
    def init(self):
        self._os_provider = Mock()
        self._args = []
        self._config_nginx = ConfigNginx()
        
        self._old_error_handler = ArgumentParser.error
        ArgumentParser.error  = self.mocked_error
    
    def cleanup(self):
        ArgumentParser.error = self._old_error_handler

    def test_missing_args(self):
        '''This test case ensures exception are raised if not all arguments are provided.'''
        
        case_inputs = [("ipaddress required", []),
                       ("vhost-name required", ["--ipaddress", "127.0.0.1"]),
                       ("uwsgi-port required", ["--ipaddress", "127.0.0.1",
                                                 "--vhost-name", "fantastico-test.com"]),
                       ("root-folder required", ["--ipaddress", "127.0.0.1",
                                                 "--vhost-name", "fantastico-test.com",
                                                 "--uwsgi-port", "12080"])]
        
        for expected_msg, args in case_inputs:
            with self.assertRaises(ValueError) as cm:
                self._config_nginx(args)
            
            self.assertTrue(str(cm.exception).find(expected_msg))
               
    def test_conf_generated_ok(self):
        '''This test case ensures configuration file is generated correctly and added to nginx enabled sites.'''
        
        self._args.extend([
                           "--ipaddress", "127.0.0.1",
                           "--vhost-name", "test-app.com",
                           "--uwsgi-port", "12090",
                           "--root-folder", "/test/folder/vhost",
                           "--modules-folder", "/"])
        
        root_folder = os.path.abspath(instantiator.get_class_abslocation(BasicSettings) + "../")        
        
        tpl_loader = FileSystemLoader(searchpath=root_folder)
        tpl_env = Environment(loader=tpl_loader)
        
        config_data = {"ip_address": "127.0.0.1",
                       "vhost_name": "test-app.com",
                       "http_port": 80,
                       "uwsgi_port": 12090,
                       "root_folder": "/test/folder/vhost",
                       "modules_folder": "/"}
        
        expected_config = tpl_env.get_template("/deployment/conf/nginx/fantastico-wsgi").render(config_data)
        
        config = self._config_nginx(self._args)
        
        self.assertEqual(expected_config, config)