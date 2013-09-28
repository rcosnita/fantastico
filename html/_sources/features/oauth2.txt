OAUTH2
======

In Fantastico, a very modern authorization framework (**OAUTH2**) was choosen for guaranteeing:

   #. Easy security for REST APIs.
   #. Easy integration of 3rd party applications.
   #. Easy integration of various Identity Providers.

OAUTH2 specification contains many scenarios for its usage and provide various flows:

   #. Authorizaton code grant.
   #. Implicit grant.
   #. Resource owner password credentials grant.
   #. Client credentials grant.

In order to understand all this flows you can read the official `OAUTH2 <http://tools.ietf.org/pdf/rfc6749.pdf>`_
documentation.

Fantastico security
-------------------

In order to keep things as simple as possible, in Fantastico we currently support only **authorization code grant**. Moreover,
you can find some particularities of Fantastico implementation:

   * We only support **Authorization code grant** (for all use cases where protected resources are involved).
   * We only support **Resource owner password credentials grant** for Anonymous access to resources.
   * We fully support scopes
   * We support state parameter for avoiding Cross Site Request Forgery

.. toctree::
   :maxdepth: 3
   
   oauth2/simple_api_example
   oauth2/tokens_format
   oauth2/tokens_storage
   oauth2/error_responses
   oauth2/compatible_idp
   oauth2/roa_security