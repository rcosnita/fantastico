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

         GET - /simple-menus/ui/index?state=abcdsxadsa

   #. Fantastico filter detects the route requires permissions (scopes).

      #. It checks to see if user is authenticated or not.
      #. Unauthenticated user is redirected to Fantastico IDP login page.

         .. code-block:: html

            GET - /oauth/idp/login?client_id=simple-menus&redirect_uri=%2Fsimple-menus%2Fui%2Findex%26state%3Dabcdsxadsa

      #. User authenticates successfully.

         .. code-block:: html

            GET - /oauth/authorize?client_id=simple-menus&redirect_uri=%2Fsimple-menus%2Fui%2Findex%26state%3Dabcdsxadsa

      #. Authorization server correctly authorizes the client and generates an access token.

         .. code-block:: html

            HTTP/1.1 302 Found
            Location: /simple-menus/ui/index#access_token=2YotnFZFEjr1zCsicMWpAA&state=abcdsxadsa&token_type=bearer&expires_in=3600

   #. Menus management application start page stores the access token into the application space (session storage might be used for this).
      It is recommended to validate received state in order to ensure it corresponds to the initial request.

This is it. Using the access token, end user can easily access desired functionality. Moreover, using the access token,
menus management application can easily invoke apis.