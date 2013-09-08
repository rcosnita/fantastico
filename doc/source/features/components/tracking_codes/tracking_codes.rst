Tracking codes
==============

Every web application usually requires support for tracking visitors behavior. Most of the solutions can be easily integrated
into a website by adding a small javascript snippet into every page you want to track. Below you can find some popular tracking
solutions (free or commercial).

Analytic solutions
------------------

At the moment of writting this article, there are plenty of options available for web developers to track their
website performance:

   #. `Google analytics <https://www.google.com/analytics/>`_ (probably the most popular solution).
   #. `Reinvigorate <https://www.reinvigorate.net/>`_.
   #. `KISSmetrics <https://www.kissmetrics.com/>`_.
   #. `FoxMetrics <http://foxmetrics.com/>`_.
   #. `Mint <http://haveamint.com/>`_.
   #. `Open Web Analytics <http://www.openwebanalytics.com/>`_.
   #. `Clicky <http://clicky.com/>`_.
   #. `Mixpanel <https://mixpanel.com/>`_.
   #. `Chartbeat <https://chartbeat.com/>`_.
   #. `Adobe Web Analytics <http://www.adobe.com/solutions/digital-analytics.html>`_.
   #. `Chartbeat <https://chartbeat.com/>`_.
   #. `Inspectlet <http://www.inspectlet.com/>`_.

Of course there are many other solutions available out there. For more information about the above mentioned solution I recommend
you read the excellent `article <http://www.onextrapixel.com/2013/07/16/ten-best-alternatives-to-google-analytics/>`_
posted by Aidan Huang.

Integration
-----------

Follow the steps from this section in order to enable tracking in **Fantastico** projects:

#. Activate tracking extension:

   .. code-block:: bash

      fsdk activate-extension --name tracking_codes --comp-root <comp_root>

#. Add your tracking codes into database (easiest way is through :doc:`/features/sdk/command_syncdb`)

#. Create a sql script similar to the one below and place it under **<comp_root>/sql/create_data.sql**:

   .. code-block:: sql

      INSERT INTO tracking_codes(provider, snippet)
      VALUES ('Google Analytics', '
         <script type="text/javascript">
              var _gaq = _gaq || [];
              _gaq.push(["_setAccount", "UA-XXXXX-X"]);
              _gaq.push(["_trackPageview"]);

              (function() {
                var ga = document.createElement("script"); ga.type = "text/javascript"; ga.async = true;
                ga.src = ("https:" == document.location.protocol ? "https://ssl" : "http://www") + ".google-analytics.com/ga.js";
                var s = document.getElementsByTagName("script")[0]; s.parentNode.insertBefore(ga, s);
              })();
         </script>');

#. Update your project database

   .. code-block:: bash

      fsdk syncdb --db-command /usr/bin/mysql --comp-root <comp_root>

#. Use tracking codes in your pages:

   .. code-block:: html

      {% component url="/tracking-codes/codes/" %}{% endcomponent %}

Tracking component is rendering all available codes from the database.

Current limitations
-------------------

In the first version of this component (part of **Fantastico 0.4**) there are some known limitations:

   * No API provided for Create / Update / Delete operations.

Technical summary
-----------------

.. autoclass:: fantastico.contrib.tracking_codes.tracking_controller.TrackingController
   :members:

.. autoclass:: fantastico.contrib.tracking_codes.models.codes.TrackingCode
   :members: