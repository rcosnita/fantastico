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
from argparse import ArgumentParser
from fantastico.settings import BasicSettings
from fantastico.utils import instantiator
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
import os
import sys

class ConfigNginx(object):
    '''This class provides all required operations for generating a valid nginx configuration file for
    a given domain name and ip address. The configuration can be used together with other scripts in order
    to include the configuration into nginx enabled sites.'''

    def __init__(self):
        self._args_parser = ArgumentParser(description="This script generates an nginx vhost file for the" +
                                           " current fantastico project.")

        root_folder = os.path.abspath(instantiator.get_class_abslocation(BasicSettings) + "../")
        
        tpl_loader = FileSystemLoader(searchpath=root_folder)
        self._tpl_env = Environment(loader=tpl_loader)        
        
        self._build_args_parser()
            
    def _build_args_parser(self):
        '''This method builds the args parser required to split an array of arguments into config attributes.'''
        
        self._args_parser.add_argument("--ipaddress", dest="ip_address", type=str,
                                       help="The ip address binded to the current virtual host.",
                                       required=True)
        self._args_parser.add_argument("--vhost-name", dest="vhost_name", type=str,
                                       help="The virtual host name for this project: e.g fantastico.org",
                                       required=True)
        self._args_parser.add_argument("--http-port", dest="http_port", type=int,
                                       help="The http port where nginx should listen for this virtual host.",
                                       default=80)
        self._args_parser.add_argument("--uwsgi-port", dest="uwsgi_port", type=int,
                                       help="Uwsgi port where nginx should proxy fantastico specific requests.",
                                       required=True)
        self._args_parser.add_argument("--root-folder", dest="root_folder", type=str,
                                       help="Root folder of this fantastico project.",
                                       required=True)
        self._args_parser.add_argument("--modules-folder", dest="modules_folder", type=str,
                                       help="Modules folder where this project holds fantastico custom components.",
                                       default="/")
    
    def __call__(self, args):
        '''This method coordinate the config generation by parsing the given arguments and using them
        to generate nginx config file.'''
        
        args_namespace = self._args_parser.parse_args(args)
        
        config_data = {"ip_address": args_namespace.ip_address,
                       "vhost_name": args_namespace.vhost_name,
                       "http_port": args_namespace.http_port,
                       "uwsgi_port": args_namespace.uwsgi_port,
                       "root_folder": args_namespace.root_folder,
                       "modules_folder": args_namespace.modules_folder}
        
        config = self._tpl_env.get_template("/deployment/conf/nginx/fantastico-wsgi").render(config_data) 
        
        return config

def main(stdout=sys.stdout):
    '''This method is executed by script __main__ entry point in order to generate the configuration.'''
    
    config_generator = ConfigNginx()

    stdout.write(config_generator(sys.argv[1:]))
    stdout.flush()
    
if __name__ == "__main__":
    main()