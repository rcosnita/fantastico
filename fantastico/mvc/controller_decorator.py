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
.. py:module:: fantastico.mvc.controller_decorator
'''

class Controller(object):
    '''This class provides a decorator for magically registering methods as route handlers. This is an extremely important
    piece of Fantastico framework because it simplifies the way you as developer can define mapping between a method that
    must be executed when an http request to an url is made:
    
    .. code-block:: python
    
        @Controller(url="/blogs/", method="GET", models={"Blog": "fantastico.plugins.blog.models.blog.Blog"])
        def list_blogs(self, request):
            Blog = request.models.Blog
        
            blogs = Blog.all_paged(start_record=1, end_record=0, sort_expr=[asc(Blog.create_date), desc(Blog.title)])
        
            return Response(blogs)
            
    The above code assume the following:
    
    #. As developer you created a model called blog (this is already mapped to some sort of storage).
    #. Fantastico framework generate the facade automatically (and you never have to know anything about underlining repository).
    #. Fantastico framework takes care of data conversion.
    #. As developer you create the method that knows how to handle **/blog/** url.
    #. Write your view.
    
    Below you can find the design for MVC provided by **Fantastico** framework:
    
    .. image:: /images/core/mvc.png'''