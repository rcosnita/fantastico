Model View Controller
=====================

**Fantastico** framework provides quite a powerful model - view - controller implementation. Here you can find details about
design decisions and how to benefit from it.

Classic approach
----------------

Usually when you want to work with models as understood by MVC pattern you have in many cases boiler plate code:

#. Write your model class (or entity)
#. Write a repository that provides various methods for this model class.
#. Write a facade that works with the repository.
#. Write a web service / page that relies on the facade.
#. Write one or multiple views.

As this is usually a good in theory, in practice you will see that many methods from facade are converting a data transfer object
to an entity and pass it down to repository.

Fantastico approach
-------------------

**Fantastico** framework provides an alternative to this classic approach (you can still work in the old way if you really really
want). Let's see a simple example below:

.. code-block:: python

    @Controller(url="/blogs/", method="GET", models={"Blog": "fantastico.plugins.blog.models.blog"])
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

.. image:: /images/core/mvc.png

Model
-----

A model is a very simple object that inherits :py:class:`fantastico.mvc.models.BaseModel`.

View
----

A view can be a simple html plain file or html + jinja2 enriched support. You can read more about **Jinja2** 
`here <http://jinja.pocoo.org/docs/>`_. Usually, if you need some logical block statements in your view (if, for, ...)
it is easier to use jinja 2 template engine. The good news is that you can easily embed jinja 2 markup in your views
and it will be rendered automatically.

Controller
----------

A controller is the *brain*; it actually combines a model execute some business logic and pass data to the desired view
that needs to be rendered. In some cases you don't really need view in order to provide the logic you want:

    * A REST Web service.
    * A RSS feed provider.
    * A file download service
    
Though writing REST services does not require a view, you can load external text templates that might be useful for assembling the
response:

    * An invoice generator service
    * An xml file that must be filled with product data
    * A `vCard <http://en.wikipedia.org/wiki/VCard>`_. export service.
    
If you want to read a small tutorial and to start coding very fast on Fantastico MVC read :doc:`/how_to/mvc_how_to`.     