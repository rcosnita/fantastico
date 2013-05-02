Routing engine
==============

.. image:: /images/routing_engine/routing_engine.png

Fantastico routing engine is design by having extensibility in mind. Below you can find the list of concerns for routing engine:

   #. Support multiple sources for routes.
   #. Load all available routes.
   #. Select the controller that can handle the request route (if any available).

.. autoclass:: fantastico.routing_engine.router.Router
    :members:

   
Routes loaders
--------------

Fantastico routing engine is designed so that routes can be loaded from multiple sources (database, disk locations, and others).
This give huge extensibility so that developers can use Fantastico in various scenarios:

   * Create a CMS that allows people to create new pages (mapping between page url / controller) is hold in database. Just by
     adding a simple loader in which the business logic is encapsulated allows routing engine extension.
   * Create a blog that loads articles from disk.
   
I am sure you can find other use cases in which you benefit from this extension point.

How to write a new route loader
-------------------------------

Before digging in further details see the RouteLoader class documentation below:

.. autoclass:: fantastico.routing_engine.routing_loaders.RouteLoader
   :members:
   
As you can, each concrete route loader receives in the constructor settings facade that can be used to access fantastico settings.
In the code example above, DummyRouteLoader maps a list of urls to a controller method that can be used to render it. Keep in
mind that a route loader is a stateless component and it can't in anyway determine the wsgi environment in which it is used. In
addition this design decision also make sure clear separation of concerned is followed.

Once your **RouteLoader** implementation is ready you must register it into settings profile. The safest bet is to add it into
BaseSettings provider. For more information read :doc:`/get_started/settings`.

Configuring available loaders
-----------------------------

You can find all available loaders for the framework configured in your settings profile. You can find below a sample
configuration of available loaders:


.. code-block:: python

    class CustomSettings(BasicSettings):
        @property
        def routes_loaders(self):
            return ["fantastico.routing_engine.custom_loader.CustomLoader"]
            
The above configuration tells **Fantastico routing engine** that only CustomLoader is a source of routes. If you want to learn
more about multiple configurations please read :doc:`/get_started/settings`.

DummyRouteLoader
----------------

.. autoclass:: fantastico.routing_engine.dummy_routeloader.DummyRouteLoader
    :members:
