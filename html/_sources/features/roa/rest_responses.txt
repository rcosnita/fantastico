REST Responses
==============

When working with resources API it is important to understand what responses might be returned in order to correctly consume
them into your clients. In this document you can find success / exception responses coming from APIs.

Common responses
----------------

For each call there are some common responses that might be returned by APIs:

Internal Server Error
~~~~~~~~~~~~~~~~~~~~~

When working in distributed environments there are unexpected situations occuring (server failing, dns failing, and so on). In
all this cases a 500 HTTP Status code will be returned and an html generated page will be sent in the body of the error. Do
not make assumptions about the format of this response as it might change in the future.

Concrete errors
~~~~~~~~~~~~~~~

In Fantastico generated APIs, concrete errors follows a given format:

   .. code-block:: javascript

      {
         "error_code": <a numeric error code used for uniquely identifying the situation>,
         "error_description": <a user friendly message in English describing the error>,
         "error_details": <an http link where you can find more details about the error which occured>
      }

Resource Item
-------------

Retrieve resource item
~~~~~~~~~~~~~~~~~~~~~~

When retrieving a resource from a collection (**GET /api/2.0/app-settings/1**) the following responses might be returned:

   * 200 OK

      .. code-block:: html

         200 OK
         Content-Type: application/json
         Content-Length: 53

         {"id": 1, "name": "default_locale", "value": "en_US"}

   * 404 Not Found

      .. code-block:: html

         404 Not Found
         Content-Type: application/json
         Content-Length: 160

         {"error_code": 10001, "error_description": "Resource 1 does not exist.", "error_details": "https://rcosnita.github.com/fantastico/html/features/roa/1000x.html"}

Create a new resource item
~~~~~~~~~~~~~~~~~~~~~~~~~~

When creating a resource into a collection (**POST /api/2.0/app-settings**) the following responses might be returned:

   * 201 Created

      .. code-block:: html

         201 Created
         Content-Type: application/json
         Content-Length: 0
         Location: /api/2.0/app-settings/123

      If you want to fetch the newly created resource just follow the location header.

   * 400 Bad Request

      .. code-block:: html

         400 Bad Request
         Content-Type: application/json
         Content-Length: 173

         {"error_code": 10010, "error_description": "Resource 1 requires field (name|value).", "error_details": "https://rcosnita.github.com/fantastico/html/features/roa/1000x.html"}

Update an existing resource
---------------------------

When updating an existing resource (**PUT /api/2.0/app-settings**) the following responses might be returned:

   * 204 No Content

      .. code-block:: html

         204 No Content
         Content-Type: application/json
         Content-Length: 0

   * 400 Bad Request

      .. code-block:: html

         400 Bad Request
         Content-Type: application/json
         Content-Length: 173

         {"error_code": 10010, "error_description": "Resource 1 requires field (name|value).", "error_details": "https://rcosnita.github.com/fantastico/html/features/roa/1000x.html"}

Delete an existing resource
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When deleting an existing resource (**DELETE /api/2.0/app-settings**) the following responses might be returned:

   * 204 No Content

      .. code-block:: html

         204 No Content
         Content-Type: application/json
         Content-Length: 0

   * 400 Bad Request

      .. code-block:: html

         400 Bad Request
         Content-Type: application/json
         Content-Length:

         {"error_code": 10020, "error_description": "Resource 1 is still in use.", "error_details": "https://rcosnita.github.com/fantastico/html/features/roa/1000x.html"}

Bulk creation of items
~~~~~~~~~~~~~~~~~~~~~~

Fantastico APIs do not support bulk creation of items. We do not intend to add this kind of capability.