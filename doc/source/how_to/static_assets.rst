Static assets
=============

By default, static assets can be any file that is publicly available. Most of the time, here you can place:

   * css files
   * png, jpg, gif files
   * downloadable pdf
   * movie files
   * any other file format you can think about
   
For Production environment, requests to these files are handled by the web server you are using. You only need to
place them under **static** folder of your component (:doc:`/features/component_model`).

There are several scenario in which Fantastico projects are deployed which influence where your component static files
are stored. I recommend you read :doc:`/how_to/deployment_how_to` section.

Static assets on dev
--------------------

Of course, on development environment you are not required to have a web server in front of your Fantastico dev server.
For this purpose, fantastico framework provides a special controller which can easily serve static files. Even though
it works as expected, please do not use it in production. It does not send headers required by browser for caching
purposes.

Static assets routes are the same between **prod** and **dev** environments.  