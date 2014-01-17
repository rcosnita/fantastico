Example (Simple Menu API)
=========================

Lets consider a virtual resource called SimpleMenu which has the following API:

+---------------+---------------------------+---------------------------+--------------------------+
| **HTTP Verb** | **URL**                   | **Description**           | **Required permissions** |
+---------------+---------------------------+---------------------------+--------------------------+
| GET           | /api/1.0/simple-menus     | Retrieve all menus.       |                          |
+---------------+---------------------------+---------------------------+--------------------------+
| POST          | /api/1.0/simple-menus     | Create a new system menu. | simple_menus.create      |
+---------------+---------------------------+---------------------------+--------------------------+
| PUT           | /api/1.0/simple-menus/:id | Update an existing menu.  | simple_menus.update      |
+---------------+---------------------------+---------------------------+--------------------------+
| DELETE        | /api/1.0/simple-menus/:id | Delete an existing menu.  | simple_menus.delete      |
+---------------+---------------------------+---------------------------+--------------------------+

Terminology
-----------

In OAUTH, we always talk about three concepts:

   #. Resource (Image, Melody, Menu).
   #. Resource Owner (an Identity Provider which can authenticatate the entities owning resources).
   #. Client (an application which wants access to resources owned by Resources owner in order to provide useful features).

In the above example, Simple Menu is a resource owned by a system (global resource). Resource owners are all persons who
are granted at least one scope required by the resource:

   * Everyone has anonymous (read) access to the menus.
   * Everyone granted **simple_menus.create**,**simple_menus.update** or **simple_menus.delete** can manage (CRUD) existing menus.

It is important to understand that permissions are called **scopes** in OAUTH2 specification.

Display all menus
-----------------

.. image:: /images/oauth2/simple_menu_read.png

As you can see in the above example read access is pretty straightforward because the read endpoint (route) does not require
authorization (specific scopes).

.. _oauth_create_new_menu:

Managing menus.
---------------

.. image:: /images/oauth2/simple_menu_create.png

The above diagram assumes an application exists for managing **menus**. This application (extension) consist of a set of frontend
controllers which renders only markup and a set of **REST APIs** described above. The above diagram assumes **End user** uses an
user agent capable of supporting HTTP protocol. Below you can find the http calls made:

   #. Unauthenticated user requests:

      .. code-block:: html

         GET - /authorize?response_type=token&client_id=sample-menus&state=xyz&error_format=hash&redirect_uri=/simple-menus/ui/index&scopes=simple_menus.create%20simple_menus.update%20simple_menus.delete

   #. Fantastico /authorize endpoint detects that user is not authenticated and redirects the user agent to login screen.
   #. If authentication is successful user agent is redirected back to /authorize.
   #. At this point an access token is generated and user agent is redirected back to simple menus ui index page with an access token in hash.
   #. Menus management application start page stores the access token into the application space (session storage might be used for this).
      It is recommended to validate received state in order to ensure it corresponds to the initial request state. Application must decide
      how to generate state and keep it consistent before request and response.

This is it. Using the access token, end user can easily access desired functionality. Moreover, using the access token,
menus management application can easily invoke apis.