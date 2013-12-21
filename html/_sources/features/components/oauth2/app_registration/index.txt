OAUTH2 application registration
===============================

This extension allows developers to register new OAUTH2 secured applications into a Fantastico project using an web application.
Of course this application is also secured using OAUTH2 so no unauthorized users can alter our project applications.

Overview
--------

View apps
~~~~~~~~~

**/oauth/oauth2-registration/ui/view-apps?token=1/fFAGRNJru1FTz70BzhT3Zg**

.. figure:: /images/oauth2/app_registration/view_apps.png


Edit existing app
~~~~~~~~~~~~~~~~~

**/oauth/oauth2-registration/ui/edit-app/1?token=1/fFAGRNJru1FTz70BzhT3Zg**

.. figure:: /images/oauth2/app_registration/edit_app.png

Register new app
~~~~~~~~~~~~~~~~

**/oauth/oauth2-registration/ui/register-app?token=1/fFAGRNJru1FTz70BzhT3Zg**

.. figure:: /images/oauth2/app_registration/edit_app.png

As you can see, **oauth2-registration** application is also secured with OAuth2. When you try to access any url mentioned above
without providing an access token you will be redirected to login screen (default behavior). From there, you can login and obtain
a correct access token.