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

setup(name="fantastico",
      version="1.0.0",
      description="Python MVC web framework with built in capabilities for developing Web Services and modular Web Applications.",
      author="Radu Viorel Cosnita",
      author_email="radu.cosnita@gmail.com",
      maintainer_email="radu.cosnita@gmail.com",
      url='https://github.com/rcosnita/fantastico/',
      packages=["fantastico", "fantastico.deployment", "fantastico.deployment.tests", "fantastico.locale",
                "fantastico.middleware", "fantastico.middleware.tests",
                "fantastico.mvc", "fantastico.mvc.models", "fantastico.mvc.models.tests", 
                "fantastico.mvc.tests", "fantastico.mvc.tests.subroutes", 
                "fantastico.routing_engine", "fantastico.routing_engine.tests",
                "fantastico.samples", "fantastico.samples.mvc", "fantastico.samples.mvc.models", 
                "fantastico.samples.mvc.tests", 
                "fantastico.server", "fantastico.server.tests", 
                "fantastico.tests", "fantastico.utils"])