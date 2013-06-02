#!/usr/bin/env python3

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
.. py:module:: fantastico.deployment.setup
'''

from distutils.core import setup
import os

def list_folder_recursive(virtual_folder, folder):
    '''This method list a given folder and retrieves a new list containing a list of tuples (vfolder, [files]).'''
    
    curr_tuple = (virtual_folder, [])
    ret_list = [curr_tuple]
    
    for filename in os.listdir(folder):
        abspath = "%s/%s" % (folder, filename)
        
        if os.path.isfile(abspath):
            curr_tuple[1].append(abspath)
        elif os.path.isdir(abspath):
            virtual_folder_new = "%s/%s" % (virtual_folder, filename)
            
            ret_list.extend(list_folder_recursive(virtual_folder_new, abspath))
    
    return ret_list

setup(name="fantastico",
      version=os.environ.get("FANTASTICO_VERSION", "0.0.1"),
      description="Python MVC web framework with built in capabilities for developing Web Services and modular Web Applications.",
      author="Radu Viorel Cosnita",
      author_email="radu.cosnita@gmail.com",
      maintainer_email="radu.cosnita@gmail.com",
      url='https://github.com/rcosnita/fantastico/',
      license="MIT",
      packages=["fantastico", "fantastico.deployment", "fantastico.deployment.tests", "fantastico.locale",
                "fantastico.middleware", "fantastico.middleware.tests",
                "fantastico.mvc", "fantastico.mvc.models", "fantastico.mvc.models.tests", 
                "fantastico.mvc.tests", "fantastico.mvc.tests.subroutes", 
                "fantastico.routing_engine", "fantastico.routing_engine.tests",
                "fantastico.samples", "fantastico.samples.mvc", "fantastico.samples.mvc.models", 
                "fantastico.samples.mvc.tests", 
                "fantastico.server", "fantastico.server.tests", 
                "fantastico.tests", "fantastico.utils"],
      data_files=[("scripts/fantastico", ["virtual_env/setup_dev_env.sh",
                                          "run_dev_server.sh", "run_prod_server.sh"])]
                  + list_folder_recursive("doc/fantastico", "doc/build"))