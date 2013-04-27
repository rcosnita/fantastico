Routing engine
==============

.. image:: /images/routing_engine/routing_engine.png

Fantastico routing engine is design by having extensibility in mind. Below you can find the list of concerns for routing engine:

   #. Support multiple sources for routes.
   #. Load all available routes.
   #. Select the controller that can handle the request route (if any available).
   
Routes loaders
--------------

Fantastico routing engine is designed so that routes can be loaded from multiple sources (database, disk locations, and others). This give huge extensibility so that developers can use Fantastico in various scenarios:

   * Create a CMS that allows people to create new pages (mapping between page url / controller) is hold in database. Just by adding a simple loader in which the business logic is encapsulated allows routing engine extension.
   * Create a blog that loads articles from disk.
   
I am sure you can find other use cases in which you benefit from this extension point.

How to write a new route loader
-------------------------------

TODO