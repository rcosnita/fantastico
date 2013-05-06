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
want).

.. autoclass:: fantastico.mvc.controller_decorators.Controller
    :members:
    
If you want to find more details and use cases for controller read :ref:`core-controller-section` section.
        
Model
-----

A model is a very simple object that inherits :py:class:`fantastico.mvc.models.BaseModel`.

View
----

A view can be a simple html plain file or html + jinja2 enriched support. You can read more about **Jinja2** 
`here <http://jinja.pocoo.org/docs/>`_. Usually, if you need some logical block statements in your view (if, for, ...)
it is easier to use jinja 2 template engine. The good news is that you can easily embed jinja 2 markup in your views
and it will be rendered automatically.

.. _core-controller-section:

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
    
If you want to read a small tutorial and to start coding very fast on Fantastico MVC read :doc:`/how_to/mvc_how_to`. Controller
API is documented :py:class:`fantastico.mvc.controller_decorator.Controller`.

.. autodoc:: fantastico.mvc.controller_registrator.ControllerRouteLoader
    :members: