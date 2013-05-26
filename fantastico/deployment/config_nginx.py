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
.. py:module:: fantastico.config_nginx
'''
from fantastico.settings import BasicSettings
from fantastico.utils import instantiator
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
import os
import sys

class ConfigNginx(object):
    '''This class provides all required operations for generating a valid nginx configuration file for
    a given domain name and ip address. Config file will be automatically included into active nginx configuration.'''

    @property
    def script_name(self):
        '''This property returns the script file name used for configuring nginx.'''
        
        return self._script_name
    
    @property
    def nginx_conf_folder(self):
        '''This property return the nginx conf folder given as argument.'''
        
        return self._nginx_conf_folder

    def __init__(self, os_provider=os, args=None):
        self._os_provider = os_provider
        self._args = args or []
        
        if len(self._args) < 2:
            raise ValueError("You must specify nginx config folder location.")
        
        self._script_name = self._args[0]
        self._nginx_conf_folder = self._args[1]

        root_folder = os.path.abspath(instantiator.get_class_abslocation(BasicSettings) + "../")
        
        tpl_loader = FileSystemLoader(searchpath=root_folder)
        self._tpl_env = Environment(loader=tpl_loader)
        
        self._ip_address = None
        self._vhost_name = None
        self._http_port = None
        self._uwsgi_port = None
        self._root_folder = None
        self._modules_folder = None
    
    def _read_config_attributes(self, keyboard_read=input):
        '''This method is used to read configuration attributes from console.'''
    
        if not self._ip_address:
            self._ip_address = keyboard_read("IP Address: ")
        
        if not self._vhost_name:
            self._vhost_name = keyboard_read("VHost name: ")
        
        if not self._http_port:
            self._http_port = keyboard_read("Http port: ")
        
        if not self._uwsgi_port:
            self._uwsgi_port = keyboard_read("Uwsgi port: ")
        
        if not self._root_folder:
            self._root_folder = keyboard_read("Root folder: ")
        
        if not self._modules_folder:
            self._modules_folder = keyboard_read("Modules folder: ")
    
    def __call__(self, keyboard_read=input):
        '''This method coordinate the config generation and installation into active nginx server.'''
        
        if not self._os_provider.path.exists(self.nginx_conf_folder):
            raise IOError("Nginx config folder %s does not exist." % self.nginx_conf_folder)

        self._read_config_attributes(keyboard_read)

        config_data = {"ip_address": self._ip_address,
                       "vhost_name": self._vhost_name,
                       "http_port": self._http_port,
                       "uwsgi_port": self._uwsgi_port,
                       "root_folder": self._root_folder,
                       "modules_folder": self._modules_folder}
        
        config = self._tpl_env.get_template("/deployment/conf/nginx/fantastico-wsgi").render(config_data) 
        
        return config

if __name__ == "__main__":
    config_generator = ConfigNginx(args=sys.argv)

    print(config_generator())