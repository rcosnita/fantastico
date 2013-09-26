OAUTH2 Fantastico Tokens
========================

In Fantastico, authorization codes and access tokens are opaque values for all humans (encrypted). They contain information into
them used for easily invalidating them and expiring them. In addition, they do not require a persistent store and allows
endpoint authorization without storage calls (increased performance and response time).

Authorization code structure
----------------------------

Authorization codes are opaque values for humans with the following structure (encrypted):

   .. code-block:: javascript

      {
         "scopes": ["simple_menus.create", "simple_menus.update", "simple_menus.delete"],
         "userid": 1,
         "state": "unique generated value",
         "creation_time": "1380137542",
         "expiration_time": "1380137651"
      }

Each authorization code from Fantastico OAUTH2 implementation contains the following fields:

   #. scopes

      * A JSON list of scopes for which this token was generated. (this will be transmitted to the access token)

   #. user id

      * user unique identifier (possibly email address) which can be used to obtain additional information about the user.

   #. state

      * A key uniquely generated and hard to guess.
      * It is used to protect against **Cross Site Request Forgery (CSRF)**.

   #. creation_time

      * The timestamp when this token was generated.

   #. expiration_time

      * The timestamp when this token expires (must be a really short period - 1min).

Access token structure
----------------------

.. code-block:: javascript

   {
      "scopes": ["simple_menus.create", "simple_menus.update", "simple_menus.delete"],
      "user": {
         "id": 1,
         "email: "john.doe@gmail.com",
         "first_name": "John",
         "last_name": "Doe"
      },
      "state": "unique generated value",
      "creation_time": "1380137651",
      "expiration_time": "1380163800",
      "token_type": "bearer"
   }


Each access token from Fantastico OAUTH2 implementation contains the following fields:

   #. scopes

      * A JSON list of scopes for which this token was generated. (used for endpoint authorization).

   #. user id

      * User unique identifier (used for obtaining additional information about an user).

   #. user email address

      * User email address (as stored in his profile).

   #. user first name

      * Might be used in certain secure components.

   #. user last name

      * Might be used in certain secure components.

   #. state

      * A key uniquely generated and hard to guess.
      * It is used to protect against **Cross Site Request Forgery (CSRF)**.

   #. creation_time

      * A timestamp indicating the date when this token was generated.

   #. expiration_time

      * A timestamp indicating the date when this token is going to expire.

Obtaining access tokens
-----------------------

In order to obtain an access token which can be used for calling **Fantastico** APIs requires the following:

   #. Obtain an authorization code

      .. code-block:: html

          GET /authorize?response_type=code&client_id=s6BhdRkqt3&state=xyz&redirect_uri=https%3A%2F%2Fclient%2fantasticoproject%2Ecom%2Fcb&scopes=simple_menus.create%20simple_menus.update%20simple_menus.delete HTTP/1.1
          Host: oauth2.fantasticoproject.com

   #. client.fantasticoproject.com/cb?code=<unique one time only code>&state=<unique generated state>

      * Automatically obtain an access token starting from the given autorization code.

         .. code-block:: html

           POST /token HTTP/1.1
           Host: client.fantasticoproject.com
           Content-Type: application/json

           {
               "grant_type": "authorization_code",
               "code": <unique one time only code>,
               "redirect_uri": "https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb",
               "state": "unique generated value"
           }

   #. provide access token for client usage

      .. code-block:: javascript

         {
            "access_token": "<encrypted token containing all specified information"
         }