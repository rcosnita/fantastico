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
.. py:module:: fantastico.deployment.tests.itest_config_nginx
'''
from _pyio import StringIO
from fantastico.settings import SettingsFacade
from fantastico.tests.base_case import FantasticoIntegrationTestCase
from fantastico.utils import instantiator
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
import os
import sys

class ConfigNginxIntegration(FantasticoIntegrationTestCase):
    '''This class provides the integration scenarios for config nginx generator script.'''

    def test_config_generation_ok(self):
        '''This test case ensures config nginx script works as expected.'''

        settings_cls = SettingsFacade

        root_folder = os.path.abspath(instantiator.get_class_abslocation(settings_cls) + "../")

        tpl_loader = FileSystemLoader(searchpath=root_folder)
        tpl_env = Environment(loader=tpl_loader)

        config_data = {"ip_address": "127.0.0.1",
                   "vhost_name": "test-app.com",
                   "http_port": 80,
                   "uwsgi_port": 12090,
                   "root_folder": "/test/folder/vhost",
                   "modules_folder": "/"}

        expected_config = tpl_env.get_template("/deployment/conf/nginx/fantastico-wsgi").render(config_data)

        sys.argv = ["config_nginx.py",
                    "--ipaddress", "127.0.0.1",
                    "--vhost-name", "test-app.com",
                    "--uwsgi-port", "12090",
                    "--root-folder", "/test/folder/vhost",
                    "--modules-folder", "/"]

        from fantastico.deployment import config_nginx

        generated_config = StringIO()

        config_nginx.main(generated_config)

        self.assertEqual(expected_config, generated_config.getvalue())
