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
.. py:module:: fantastico.contrib.dynamic_pages.pages_router
'''
from fantastico.mvc.base_controller import BaseController
from fantastico.mvc.controller_decorators import ControllerProvider

@ControllerProvider()
class PagesRouter(BaseController):
    '''This class provides the API for managing dynamic pages. In addition, it creates the special route **/dynamic/<page_url>**
    used to access pages stored in the database. From dynamic pages module perspective, a web page is nothing more than a relation
    between :py:class:`fantastico.contrib.dynamic_pages.models.pages.DynamicPage` and
    :py:class:`fantastico.contrib.dynamic_pages.models.pages.DynamicPageModel`.

    .. image:: /images/components/dynamic_pages/erd.png

    A typical template for dynamic pages might look like:

    .. code-block:: html

      <!DOCTYPE html>

      <html lang="{{page.language}}">
         <head>
            <meta http-equiv="Content-type" content="text/html;charset=UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="keywords" content="{{page.keywords}}" />
            <meta name="description" content="{{page.description}}" />

            <link href="/frontend/static/css/bootstrap-responsive.css" rel="stylesheet">
            <link href="/frontend/static/css/forhidraulic.css" rel="stylesheet">
            <title>{{page.title}}</title>
         </head>

         <body>
            <h1>{{page.article_left.value}}</h1>

            <h2>{{page.article_right.value}}</h1>
         </body>
       </html>
    '''
