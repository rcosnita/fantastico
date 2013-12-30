OAUTH2 Fantastico IDP
=====================

Fantastico provides a default Identity provider which provides required APIs for managing users. As other Fantastico
extensions the APIs are secured with OAUTH2 tokens.

APIs
----

+----------------------------------------------+----------+---------------------+-----------------------------------------------------------------------+
| **URI**                                      | **Verb** | **Required scopes** | **Description**                                                       |
+----------------------------------------------+----------+---------------------+-----------------------------------------------------------------------+
| **/oauth/idp/profile?token=...**             | GET      | user.profile.read   | Retrieves information about authenticated user.                       |
+----------------------------------------------+----------+---------------------+-----------------------------------------------------------------------+
| **/oauth/idp/profile?token=...**             | POST     |                     | Creates a new user profile.                                           |
+----------------------------------------------+----------+---------------------+-----------------------------------------------------------------------+
| **/oauth/idp/profile?token=...**             | PUT      | user.profile.update | Updates an existing user profile.                                     |
+----------------------------------------------+----------+---------------------+-----------------------------------------------------------------------+
| **/oauth/idp/profile?token=...**             | DELETE   | user.profile.delete | Updates an existing user profile.                                     |
+----------------------------------------------+----------+---------------------+-----------------------------------------------------------------------+
| **/oauth/idp/ui/login?return_url=/test-url** | GET      |                     | Returns the markup for login screen.                                  |
+----------------------------------------------+----------+---------------------+-----------------------------------------------------------------------+
| **/oauth/idp/login?return_url=/test-url**    | POST     |                     | Authenticate the user, generates a token and passes it to return url. |
+----------------------------------------------+----------+---------------------+-----------------------------------------------------------------------+

User profile data
-----------------

.. image:: /images/oauth2/idp_profiles.png

Login frontend
--------------

.. image:: /images/oauth2/idp_login.png

Fantastico provides the secure process for login and account recovery. Developers can easily customize the login screen by providing
a template which must be applied to login screen. A typical custom login template is presented below:

.. code-block:: html

   {% block head %}
      <title>Simple login template</title>
   {% endblock %}
   
   {% block body_header %}
      <h1>Login screen</h1>
   {% endblock %}
   
   {% block body_footer %}
      <h6>A tiny little footer.</h6>
   {% endblock %}

You can find documentation on how to configure custom login template on :doc:`/get_started/settings`.

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