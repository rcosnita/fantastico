OAuth2 Identity Provider
========================

This component provides the built in Fantastico identity provider which supports:

   * Customizable login screen
   * API for users CRUD operations
   * API for persons.

You can read more about this on :doc:`/features/oauth2/idp`.

Integration
-----------

In order to use OAuth2 identity provider into your project follow the steps below:

   #. Activate **OAuth2 IDP** extension.

      .. code-block:: bash

         fsdk activate-extension --name oauth2_idp --comp-root <comp_root>

   #. Synchronize your database with latest changes.

      .. code-block:: bash

         fsdk syncdb --db-command /usr/bin/mysql --comp-root <comp_root>

   #. Run development server.
   #. Visit http://localhost:12000/oauth/authorize?response_type=token&state=xyz&error_format=hash&client_id=11111111-1111-1111-1111-111111111111&scope=user.profile.read&redirect_uri=/oauth/idp/ui/cb
   #. Log with admin@fantastico.com / 1234567890
   #. You should see a success html page which displays your access token.