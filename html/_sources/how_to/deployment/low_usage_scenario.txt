Low usage (simplest scenario)
=============================

.. image:: /images/deployment/low_usage_all_in_one.png

Above diagram described the simplest scenario for rolling out Fantastico to production. You can use this scenario
for minimalistic web applications like:

   * Presentation website
   * Personal website
   * Blog

We usually recommend to start with this deployment scenario and the migrate to more complex scenarios when
you application requires it.

+----------------------------------------------------------------+---------------------------------------------------------------+
| Advantages                                                     | Disadvantages                                                 |
+================================================================+===============================================================+
| Extremely easy to deploy                                       | Does not scale well for more than couple of requests / second |
+----------------------------------------------------------------+---------------------------------------------------------------+
| Minimal os configuration                                       | All components are bundled on one node without any failover.  |
+----------------------------------------------------------------+---------------------------------------------------------------+
| Automatic scripts for configuring the os                       | Does not support vertical scaling out of the box.             |
+----------------------------------------------------------------+---------------------------------------------------------------+
| Easy to achieve horizontal scaling for all components at once. | Static files are not served from a cdn.                       |
+----------------------------------------------------------------+---------------------------------------------------------------+

Setup
-----

#. Install Fantastico framework on the production machine (:doc:`/get_started/installation`.).
#. Goto $FANTASTICO_ROOT/deployment
#. sh setup_low_usage_<os_distribution).sh (e.g sh setup_low_usage_ubuntu.sh)
#. Done.