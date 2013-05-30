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
#. export ROOT_PASSWD=<your root password>
#. sh setup_low_usage_<os_distribution).sh --ipaddress <desired_ip> --vhost-name <desired_vhost> --uwsgi-port <uwsgi port> --root-folder <desired root folder> --modules-folder <desired modules folder> (e.g sh setup_low_usage_ubuntu.sh --ipaddress 127.0.0.1 --vhost-name fantastico-framework.com --uwsgi-port 12090 --root-folder \`pwd\` --modules-folder /fantastico/samples)
#. Done.

It is usually a good idea to change the number of parallel connections supported by your linux kernel:

1. sudo nano /etc/sysctl.conf
2. Search for **net.core.somaxconn**.
3. If it does not exist you can add net.core.somaxconn = 8192 to the bottom of the file.
4. Restart the os.