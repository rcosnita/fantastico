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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is common to want to access currently granted scopes for a given request. In order to do this use the following code snippet:

   .. code-block:: python

      @Controller(url="^/sample-controller$")
      @RequiredScopes(scopes=["custom_scope1.read"])
      def handle_request(self, request):
         access_token = request.context.security.access_token
         scopes = access_token.encrypted.scopes

         # validate scopes

Supported token generators
--------------------------

.. autoclass:: fantastico.oauth2.token.Token
   :members:

.. autoclass:: fantastico.oauth2.tokengenerator_factory.TokenGeneratorFactory
   :members:

.. autoclass:: fantastico.oauth2.token_generator.TokenGenerator
   :members:

.. autoclass:: fantastico.oauth2.logintoken_generator.LoginTokenGenerator
   :members:

.. autoclass:: fantastico.oauth2.accesstoken_generator.AccessTokenGenerator
   :members:

Encryption / decryption
-----------------------

In Fantastico OAuth2, tokens are encrypted / decrypted using AES symmetric encryption. Below you can find the classes which provides
AES implementation:

.. autoclass:: fantastico.oauth2.token_encryption.TokenEncryption
   :members:

.. autoclass:: fantastico.oauth2.token_encryption.AesTokenEncryption
   :members:

Concrete exceptions
-------------------

.. autoclass:: fantastico.oauth2.exceptions.OAuth2Error
   :members:

.. autoclass:: fantastico.oauth2.exceptions.OAuth2InvalidTokenDescriptorError
   :members:

.. autoclass:: fantastico.oauth2.exceptions.OAuth2InvalidTokenTypeError
   :members:

.. autoclass:: fantastico.oauth2.exceptions.OAuth2TokenExpiredError
   :members:

.. autoclass:: fantastico.oauth2.exceptions.OAuth2InvalidClientError
   :members:

.. autoclass:: fantastico.oauth2.exceptions.OAuth2InvalidScopesError
   :members:

.. autoclass:: fantastico.oauth2.exceptions.OAuth2MissingQueryParamError
   :members:

.. autoclass:: fantastico.oauth2.exceptions.OAuth2TokenEncryptionError
   :members: