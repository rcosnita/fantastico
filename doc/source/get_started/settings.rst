Fantastico settings
===================

Fantastico is configured using a plain settings file. This file is located in the root of fantastico framework
or in the root folder of your project. Before we dig further into configuration options lets see a very simple settings
file:

.. code-block:: python
    
   installed_middleware = ['fantastico.core.middleware.RequestResponseMiddleware',
                           'fantastico.core.middleware.RoutingEngineMiddleware']
                                
The above code sample represent the minimum required configuration for fantastico framework to run. The order in which
middlewares are listed is the order in which they are executed when an http request is made.

Settings API
------------

Below you can find technical information about settings.

.. autoclass:: fantastico.settings.BasicSettings
   :members:
   
Create Dev configuration
------------------------

Create Prod configuration
-------------------------
   