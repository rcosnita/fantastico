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
      description="Python 3 MVC web framework with built in capabilities for developing Web Services and Modular Web Applications.",
      author="Radu Viorel Cosnita",
      author_email="radu.cosnita@gmail.com",
      maintainer_email="radu.cosnita@gmail.com",
      url='https://github.com/rcosnita/fantastico/',
      license="MIT",
      packages=["fantastico",
                "fantastico.contrib",
                "fantastico.contrib.dynamic_menu", "fantastico.contrib.dynamic_menu.models",
                "fantastico.contrib.dynamic_menu.tests",
                "fantastico.contrib.tracking_codes", "fantastico.contrib.tracking_codes.tests",
                "fantastico.contrib.tracking_codes.models", "fantastico.contrib.tracking_codes.models.tests",
                "fantastico.contrib.dynamic_pages", "fantastico.contrib.dynamic_pages.tests",
                "fantastico.contrib.oauth2_idp", "fantastico.contrib.oauth2_idp.tests",
                "fantastico.contrib.oauth2_idp.models", "fantastico.contrib.oauth2_idp.models.tests",
                "fantastico.contrib.oauth2_idp.models.validators", "fantastico.contrib.oauth2_idp.models.validators.tests",
                "fantastico.contrib.dynamic_pages.models", "fantastico.contrib.dynamic_pages.models.tests",
                "fantastico.contrib.roa_discovery", "fantastico.contrib.roa_discovery.models",
                "fantastico.contrib.roa_discovery.tests",
                "fantastico.deployment", "fantastico.deployment.tests", "fantastico.locale",
                "fantastico.middleware", "fantastico.middleware.tests",
                "fantastico.mvc", "fantastico.mvc.models", "fantastico.mvc.models.tests",
                "fantastico.mvc.tests", "fantastico.mvc.tests.subroutes",
                "fantastico.oauth2", "fantastico.oauth2.middleware", "fantastico.oauth2.middleware.tests",
                "fantastico.oauth2.models", "fantastico.oauth2.models.tests",
                "fantastico.oauth2.tests",
                "fantastico.rendering", "fantastico.rendering.tests",
                "fantastico.roa", "fantastico.roa.tests",
                "fantastico.routing_engine", "fantastico.routing_engine.tests",
                "fantastico.samples", "fantastico.samples.mvc", "fantastico.samples.mvc.models",
                "fantastico.samples.mvc.tests",
                "fantastico.sdk", "fantastico.sdk.tests", "fantastico.sdk.commands", "fantastico.sdk.commands.tests",
                "fantastico.server", "fantastico.server.tests",
                "fantastico.tests", "fantastico.utils"],
      package_data={"fantastico.rendering": ["views/*.html"],
                    "fantastico.samples.mvc": ["sql/*.sql", "static/*", "views/*.html"],
                    "fantastico.contrib.dynamic_menu": ["sql/*.sql", "static/*", "views/*.html"],
                    "fantastico.contrib.dynamic_pages": ["sql/*.sql", "views/*.html"],
                    "fantastico.contrib.oauth2_idp": ["sql/*.sql", "views/*.html"],
                    "fantastico.contrib.roa_discovery": ["sql/*.sql"],
                    "fantastico.contrib.tracking_codes": ["sql/*.sql", "views/*.html"]},
      data_files=[("scripts/fantastico", ["run_dev_server.sh", "run_prod_server.sh"])]
                  + list_folder_recursive("scripts/fantastico/virtual_env", "virtual_env")
                  + list_folder_recursive("doc/fantastico", "doc/build")
                  + list_folder_recursive("scripts/fantastico/deployment", "deployment")
                  + list_folder_recursive("scripts/fantastico/project_template", "project_template"),
      scripts=["fantastico_setup_project.sh", "fsdk"],
      classifiers=["Development Status :: 4 - Beta",
                   "Environment :: Web Environment",
                   "Intended Audience :: Developers",
                   "Intended Audience :: System Administrators",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3",
                   "Topic :: Software Development :: Libraries",
                   "Topic :: Software Development :: Libraries :: Application Frameworks",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   "Topic :: Software Development :: User Interfaces",
                   "Topic :: Internet",
                   "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
                   "Topic :: Internet :: WWW/HTTP :: Dynamic Content"])
