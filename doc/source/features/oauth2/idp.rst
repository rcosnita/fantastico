OAUTH2 Fantastico IDP
=====================

Fantastico provides a default Identity provider which provides required APIs for managing users. As other Fantastico
extensions the APIs are secured with OAUTH2 tokens.

APIs
----

+------------------------------------------------+----------+---------------------+------------------------------------------------------------------------------------------+--------------------------------------+
| **URI**                                        | **Verb** | **Required scopes** | **Description**                                                                          | **Headers**                          |
+------------------------------------------------+----------+---------------------+------------------------------------------------------------------------------------------+--------------------------------------+
| **/api/latest/oauth-idp-profile**              | GET      | user.profile.read   | Retrieves information about authenticated user.                                          | Authorization: Bearer <oauth2_token> |
+------------------------------------------------+----------+---------------------+------------------------------------------------------------------------------------------+--------------------------------------+
| **/api/latest/oauth-idp-profile**              | POST     |                     | Creates a new user profile.                                                              |                                      |
+------------------------------------------------+----------+---------------------+------------------------------------------------------------------------------------------+--------------------------------------+
| **/api/latest/oauth-idp-profile**              | PUT      | user.profile.update | Updates an existing user profile.                                                        | Authorization: Bearer <oauth2_token> |
+------------------------------------------------+----------+---------------------+------------------------------------------------------------------------------------------+--------------------------------------+
| **/api/latest/oauth-idp-profile**              | DELETE   | user.profile.delete | Updates an existing user profile.                                                        | Authorization: Bearer <oauth2_token> |
+------------------------------------------------+----------+---------------------+------------------------------------------------------------------------------------------+--------------------------------------+
| **/oauth/idp/ui/login?redirect_uri=/test-url** | GET      |                     | Returns the markup for login screen.                                                     |                                      |
+------------------------------------------------+----------+---------------------+------------------------------------------------------------------------------------------+--------------------------------------+
| **/oauth/idp/login?redirect_uri=/test-url**    | POST     |                     | Authenticate the user, generates a token and passes it to redirect uri.                  |                                      |
+------------------------------------------------+----------+---------------------+------------------------------------------------------------------------------------------+--------------------------------------+
| **/oauth/idp/ui/cb**                           | GET      |                     | A very simple callback which extracts the access token received and prints it on screen. |                                      |
+------------------------------------------------+----------+---------------------+------------------------------------------------------------------------------------------+--------------------------------------+

User profile data
-----------------

.. image:: /images/oauth2/idp_profiles.png

Login frontend
--------------

.. image:: /images/oauth2/idp_login.png

Developers can easily customize the login screen by providing a template which must be applied to login screen. A typical custom
login template is presented below:

.. code-block:: html

   {% extends "login.html" %}

   {% block head %}
       <title>Fantastico IDP default login</title>

       <!-- Latest compiled and minified CSS -->
       <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">
       <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap-theme.min.css">

       <script src="//code.jquery.com/jquery-2.0.3.min.js"></script>
       <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
   {% endblock %}

   {% block body_header %}
   <div class="row" align="center">
       <div class="col-md-4">
           <div class="panel panel-default">
               <div class="panel-heading">
                   {% block panel_header %}
                   <h1>Login to fantastico</h1>
                   {% endblock %}
               </div>
   {% endblock %}

   {% block body_footer %}
               <div class="panel-footer">
                   <h4>Created by Radu Viorel Cosnita</h4>
               </div>
           </div>
       </div>
   </div>
   {% endblock %}

You can find documentation on how to configure custom login template on :doc:`/get_started/settings`.

Administrator account
~~~~~~~~~~~~~~~~~~~~~

When you first activate the extension and you syncdb an administrator account is created:

.. code-block:: bash

   username = "admin@fantastico.com"
   password = "1234567890"

This account can be used to access various applications provided by various Fantastico extensions.

Technical summary
-----------------

Password storage
~~~~~~~~~~~~~~~~

It is recommend that each identity provider holds hashes of passwords instead of plain text passwords. Foreasily development of
new Identity Providers, Fantastico provides a contract for easily hashing passwords.

.. autoclass:: fantastico.oauth2.passwords_hasher.PasswordsHasher
   :members:

.. autoclass:: fantastico.oauth2.sha512salt_passwords_hasher.Sha512SaltPasswordsHasher
   :members:

.. autoclass:: fantastico.oauth2.passwords_hasher_factory.PasswordsHasherFactory
   :members: