CORS
====

In Fantastico framework, CORS (cross origin resource sharing) can be enabled easily per each individual controller method.

.. autoclass:: fantastico.mvc.controller_decorators.CorsEnabled
   :members:
   
In addition to **CorsEnabled** decorator, you can also configure the framework to globally append some headers to each
response:

   #. Go to your settins profile (see :py:class:`fantastico.settings.BasicSettings`)
   #. Change **global_response_headers** property and add all desired headers (e.g: Access-Control-Allow-Origin: "*")