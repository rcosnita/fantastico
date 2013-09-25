OAUTH2 Fantastico Tokens Storage
================================

For OAUTH2, we need a Relational storage.

Relational storage
------------------

In the relational storage we will hold all information describing registered clients as well as their configuration. Each client
is described by the following attributes:

   #. client_id

      * Client unique identifier.

   #. client_name

      * A user friendly client_name: e.g (fantastico_admin)

   #. client_secret

      * A client secret key used for signing every authorization code and every token type.

   #. required_scopes

      * Holds a list of all required scopes of this client.

   #. grant_type

      * Holds the supported grant type for this client.
      * Only **authorization_code** and **password** are valid values.

   #. idp

      * Holds the Identity Provider Identifier which can authenticate users for this client.

   #. otp_expiration_interval

      * Holds the number of seconds for which a one time token is valid (e.g **60**).

   #. access_expiration_time

      * Holds the number of seconds for which access tokens are valid (e.g **3600**)

Clients registration
~~~~~~~~~~~~~~~~~~~~

Clients registration in **Fantastico** is done manually by inserting new records into **clients** table.

Considerations
--------------

At the moment all generated tokens are transient and can be validated based on their decrypted content. This introduces a
minor limitation at endpoint invocation because each client needs to also append its client id as a header.

In addition, no tokens audit is hold and we can not revoke tokens till they expire.