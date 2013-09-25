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

   * Everyone has anonymous access to the menu
   * Everyone granted **simple_menus.create**,**simple_menus.update** or **simple_menus.delete** permissions is Resource Owner.

It is important to understand that permissions are called **scopes** in OAUTH2 specification.

Display all menus
-----------------

.. image:: /images/oauth2/simple_menu_read.png

As you can see in the above example, each **Fantastico** project will benefit from an **Anonymous** user. This user is considered
the **Resource owner** for all public accessible resources. This mean, that each visitor of a Fantastico application will not
be forced to authenticate when it is not necessary (**e.g display website menubar**).

.. _oauth_create_new_menu:

Create a new menu
-----------------

.. image:: /images/oauth2/simple_menu_create.png

The above diagram specifies only the standard steps from OAUTH2 specification. In reality, when authorize endpoint is reached
**End user** browser is redirected to a login screen. Once logged in, **End user** browser is redirected back to **/authorize**
url from where he is granted an authorization code.

Once the user is granted an authorization code, he will exchange the authorization code for an access_token. With the newly
obtained access token he can easily create a new simple menu.

Update an existing menu
-----------------------

It is similar to :ref:`oauth_create_new_menu` with the only difference that the final API called is
**PUT /api/1.0/simple-menus/:id**.

Delete an existing menu
-----------------------

It is similar to :ref:`oauth_create_new_menu` with the only difference that the final API called is
**DELETE /api/1.0/simple-menus/:id**.

Cautions
--------

You must understand the following steps are one time:

   #. Authenticate user
   #. Obtain authorization code
   #. Obtain access token

Once the token expires, the flow will start again from step **1.1**.