OAUTH2 Fantastico IDP
=====================

In this document you can find information about the requirements for an OAUTH2 Fantastico Identity Provider.

Endpoints
---------

/authenticate
~~~~~~~~~~~~~

This endpoint is responsible for authenticating a resource owner. Optionally, it can ask the user to accept terms of use and
to grant required permissions to the application. Consent given for an application will contain all scopes for which it was
signed.

Below you can find an authenticate request initiated by OAUTH2 Fantastico authorization server:

   .. code-block:: html

      GET /authenticate?client_id=s6BhdRkqt&state=xyz&redirect_uri=https%3A%2F%2Fclient%2fantasticoproject%2Ecom%2Fcb%3Fclient_id%3Ds6BhdRkqt%26state%3D&scopes=simple_menus.create%20simple_menus.update%20simple_menus.delete HTTP/1.1
      Host: idp.fantasticoproject.com
      Referrer: http://oauth2.fantasticoproject.com/authorize

Once the authenticate endpoint authenticate an user and obtain his consent for client required permissions the following redirect
is done:

   .. code-block:: html

      HTTP/1.1 302 Found
      Location: http://oauth2.fantasticoproject.com/authorize?client_id=s6BhdRkqt&state=xyz&redirect_uri=https%3A%2F%2Fclient%2fantasticoproject%2Ecom%2Fcb%3Fclient_id%3Ds6BhdRkqt%26state%3D&scopes=simple_menus.create%20simple_menus.update%20simple_menus.delete&response_type=code&userid=123

Now the authorize endpoint will obtain an authorization code (:doc:`/features/oauth2/tokens_format`). Based on the userid,
the endpoint will double check user consent with the idp in order to avoid attacks.

/consent
~~~~~~~~

This endpoint supports the following operations:

   * GET /consents/:userid?scopes=:scopes HTTP/1.1

      * This operation can response with 204 if consent was given or 403 if the consent was not given by resource owner.
      * In addition it can return 400 if the scopes query parameter is not given.

/profile
~~~~~~~~

This endpoint supports the following operations:

   * GET /profiles/:userid HTTP/1.1

      * This operation returns given user profile.
      * It needs a valid access token.

At the moment, users are manually created and there is no API provided.