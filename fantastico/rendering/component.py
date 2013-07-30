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

.. py:module:: fantastico.rendering.component
'''

class Component(object):
    '''In fantastico, components are defined as a collection of classes and scripts grouped together as described in 
    :doc:`/features/component_model`. Each fantastico component provides one or more public routes that can be accessed from
    a browser or from other components. This class provides the mechanism for internal component referencing.
    
    In order to gain a better understanding about internal / in process component referencing we assume **Blog** component 
    provides the following public routes:
    
        * **/blog/articles/<article_id>** - Retrieves information about an article.
        * **/blog/ui/articles/<article_id>** - Displays an article within a html container.
    
    The first url is a simple json endpoint while the second url is a simple html dynamic page. When we want to reuse a
    datasource or an dynamic html page in fantastico is extremely easy to achieve. Lets first see possible responses from the
    above mentioned endpoints: 
    
    .. code-block:: javascript
        
        /* /blog/articles/<article_id> response */
        {"id": 1,
         "title": "Simple blog article",
         "content": "This is a simple and easy to read blog article."}
         
    .. code-block:: html
    
        <!-- /blog/ui/articles/<article_id> response-->
        
        <div class="blog-article">
            <p class="title">Simple blog article</p>
            
            <p class="content">This is a simple and easy to read blog article.</p>
        </div>
    
    A very common scenario is to create multiple views for a given endpoint.
    
    .. code-block:: html
    
        <!-- web service server side reusage -->
        {% component url="/blog/articles/1", template="/show_blog_formatted.html" %}{% endcomponent %}
    
    .. code-block:: html
        
        <!-- show_blog_formatted.html -->
        <p class="blog-title">{{model.title}}</p>
        <p class="blog-content">{{model.content}}</p>
        
    As you can see, json response is plugged into a given template name. It is mandatory that the given template exists on the
    component root path.
    
    Also a very common scenario is to include an endpoint that renders partial html into a page:
    
    .. code-block:: html
    
        <!-- html server side reusage -->
        {% component url="/blog/ui/articles/1" %}{% endcomponent %}
    '''