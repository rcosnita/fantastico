Step 4 - TODO activate google analytics
=======================================

In this step of the tutorial we are going to activate frontend tracking solution for our newly created **TODO** application.
One solution would be to create a template page and included in your other pages using {% component %} tag. A more elegant solution
which does not require any code redeployment is presented below:

   #. git checkout -b step-4-activate-googleanalytics
   #. fsdk activate-extension --name tracking_codes --comp-root todo
   #. Paste the following code under fantastico-todo/todo/sql/create_data.sql:

      .. code-block:: sql

         ##############################################################################################################################
         # Copyright 2013 Cosnita Radu Viorel
         #
         # Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
         # documentation files (the "Software"), to deal in the Software without restriction, including without limitation
         # the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
         # and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
         #
         # The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
         #
         # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
         # WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
         # COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
         # ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
         ##############################################################################################################################

         DELETE FROM tracking_codes WHERE provider = 'Google Analytics';

         INSERT INTO tracking_codes(provider, script)
         SELECT 'Google Analytics', '
             <script type="text/javascript">
                  var _gaq = _gaq || [];
                  _gaq.push(["_setAccount", "UA-XXXXX-X"]);
                  _gaq.push(["_trackPageview"]);

                  (function() {
                    var ga = document.createElement("script"); ga.type = "text/javascript"; ga.async = true;
                    ga.src = ("https:" == document.location.protocol ? "https://ssl" : "http://www") + ".google-analytics.com/ga.js";
                    var s = document.getElementsByTagName("script")[0]; s.parentNode.insertBefore(ga, s);
                  })();
             </script>';

   #. fsdk syncdb -d /usr/bin/mysql -p todo
   #. Paste the following code at the end of fantastico-todo/todo/frontend/views/listing.html (before </body> tag):

      .. code-block:: html

         {% component url="/tracking-codes/ui/codes/" %}{% endcomponent %}

   #. . pip-deps/bin/activate
   #. fantastico_run_dev_server
   #. Done. Access http://localhost:12000/frontend/ui/index and view page source. You should be able to see the tracking code from above.

Explanation
-----------

By default, Fantastico framework provides an extension which can easily integrate tracking codes into components. The real advantage
of using this component comes from the fact that you can easily have one or multiple tracking scripts for multiple providers. Moreover,
you can manage tracking scripts at database level meaning you will never have to redeploy your code for tracking changes.

You can read more about tracking codes extension on :doc:`/features/components/tracking_codes/tracking_codes`.

Known issues
------------

If you are using a Fantastico version prior to 0.5.1 you will run into problems when running **fdsk syncdb** command. In order to fix this,
you must manually drop from your database the following tables:

   * sample_resource_subresources
   * sample_resources