Fantastico settings
===================

Fantastico is configured using a plain settings file. This file is located in the root of fantastico framework
or in the root folder of your project. Before we dig further into configuration options lets see a very simple settings
file:

.. code-block:: python

   class BasicSettings(object):
      @property    
      def installed_middleware(self):
         return ["fantastico.middleware.request_middleware.RequestMiddleware",
                "fantastico.middleware.routing_engine.RoutingEngineMiddleware"]
                 
      @property
      def supported_languages(self):
         return ["en_us"]
                                
The above code sample represent the minimum required configuration for fantastico framework to run. The order in which
middlewares are listed is the order in which they are executed when an http request is made.

Settings API
------------

Below you can find technical information about settings.

.. autoclass:: fantastico.settings.BasicSettings
   :members:
   
Create Dev configuration
------------------------

Let's imagine you want to create a custom dev configuration for your project. Below you can find the code for this:

.. code-block:: python

   class DevSettings(BasicSettings):
      @property
      def supported_languages(self):
         return ["en_us", "ro_ro"]
         
The above configuration actually overwrites supported languages. This mean that only en_us is relevant for **Dev** environment. You
can do the same for **Stage**, **Prod** or any other custom configuration.

Using a specifc configuration
-----------------------------

.. autoclass:: fantastico.settings.SettingsFacade
   :members: