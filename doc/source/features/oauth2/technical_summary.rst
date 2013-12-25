OAUTH2 Technical Summary
========================

In this document you can find out information about OAUTH2 implementation in Fantastico framework. It is important to have read
the previous sections before actually deep diving into technical details.

Overview
--------

.. autoclass:: fantastico.oauth2.oauth2_controller.OAuth2Controller
   :members:

Security context
----------------

.. autoclass:: fantastico.oauth2.security_context.SecurityContext
   :members:

Common tokens usage
-------------------

Obtain authenticated user id
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is common in web applications to want to obtain the current authenticated user unique identifier so that additional information
can be obtained in a secure context.

   .. code-block:: python

      @Controller(url="^/users/ui/show-profile$")
      def show_profile(self, request):
         security_ctx = request.context.security
         user_id = security_ctx.login_token.user_id

         # use profile endpoint to obtain additional information.

Obtain current granted scopes
-----------------------------

It is common to want to access currently granted scopes for a given request. In order to do this use the following code snippet:

   .. code-block:: python

      @Controller(url="^/sample-controller$")
      @RequiredScopes(scopes=["custom_scope1.read"])
      def handle_request(self, request):
         access_token = request.context.security.access_token
         scopes = access_token.encrypted.scopes

         # validate scopes