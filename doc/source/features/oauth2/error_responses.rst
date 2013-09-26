OAUTH2 Fantastico Error Responses
=================================

In this section you can find possible error responses retrieved by **Fantastico** OAUTH2 endpoints.

/authorize
----------

Authorization code
------------------

Below parameters are appended as query parameters to the redirect sent by authorize endpoint:

* error

   * **400 Bad request**

      * invalid_request

         The request is missing a required parameter, includes an invalid parameter value, includes a parameter more than once,
         or is otherwise malformed.

      * unsupported_response_type

         The authorization server does not support obtaining an authorization code using this method.

      * invalid_scope

         The requested scope is invalid, unknown, or malformed.

   * **401 Unauthorized**

      * unauthorized_client

         The client is not authorized to request an authorization code using this method.

   * **403 Forbidden**

      * access_denied

         The resource owner or authorization server denied the request.

* error_description

   Human-readable ASCII [USASCII] text providing additional information, used to assist the client developer in
   understanding the error that occurred.

* error_uri

   A URI identifying a human-readable web page with information about the error, used to provide the client developer
   with additional information about the error.