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