OAUTH2 Fantastico Tokens
========================

In Fantastico framework there are currently two type of supported tokens:

   * Authenticated user token.

      An opaque value used to prove the requester (end user) is indeed authenticated. This token is set once by the Fantastico IDP
      login page and lives a long time (couple of weeks). The structure of this opaque value as seen on server side is presented
      below:

         .. code-block:: javascript

            {"client_id": "fantastico-idp",
             "type": "login",
             "encrypted": {
                "client_id": "fantastico-idp",
                "type": "login",
                "user_id": 1,
                "creation_time": "1380137651",
                "expiration_time": "1380163800",
             }
            }

   * Access token

      An opaque value used to allow applications to access resource owner resources (images, documents, menus, etc). Below you can
      find the access token structure, as seen on server side:

         .. code-block:: javascript

            {"client_id": "simple-menus",
             "type": "access",
             "encrypted": {
               "client_id": "simple-menus",
               "type": "access",
               "user_id": 1,
               "scopes": ["simple_menus.create", "simple_menus.update", "simple_menus.delete"],
               "creation_time": "1380137651",
               "expiration_time": "1380163800"
             }
            }

All supported tokens are symmetrical encrypted by Fantastico on server side and though become opaque for the user agent. Currently,
AES-256 is used for encryption.