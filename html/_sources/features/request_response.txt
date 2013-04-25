Request lifecycle
=================

In this document you can find how a request is processed by fantastico framework. By default WSGI applications use a dictionary
that contains various useful keys:

   * HTTP Headers
   * HTTP Cookies
   * Helper keys (e.g file wrapper).
   
In fantastico we want to hide the complexity of this dictionary and allow developers to use some standardized objects. Fantastico
framework follows a Request / Response paradigm. This mean that for every single http request only one single http response will
be generated. Below, you can find a simple example of how requests are processed by fantastico framework:
 
.. image:: /images/request_response/request_response_sd.png

In order to not reinvent the wheels fantastico relies on WebOb python framework in order to correctly generate request and response
objects. For more information read `WebOB Doc <http://docs.webob.org/en/latest/reference.html>`_.

Request context
---------------

In comparison with WebOb **Fantastico** provides a nice improvement. For facilitating easy development of code, each fantastico
request has a special attribute called context. Below you can find the attributes of a request context object:

   * settings facade (:doc:`/get_started/settings`)
   * session (not yet supported)
   * **language** The current preferred by user. This is determined based on user lang header.
   * user (not yet supported)
   
.. autoclass:: fantastico.middleware.request_context.RequestContext
   :members:
   
Obtain request language
-----------------------

.. autoclass:: fantastico.locale.language.Language
   :members:
   
Obtain settings using request
-----------------------------

It is recommended to use *request.context* object to obtain fantastico settings. This hides the complexity of choosing the right
configuration and accessing attributes from it.

.. code-block:: python

   installed_middleware = request.context.settings.get("installed_middleware")
   
   print(installed_middleware)

For more information about how to configure **Fantastico** please read :doc:`/get_started/settings`.