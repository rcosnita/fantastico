Low usage AWS
=============

.. image:: /images/deployment/low_usage_aws.png

This scenario is a little bit more complex than :doc:`/how_to/deployment/low_usage_scenario` but it provides some 
advantages:

+-------------------------------------------+-----------------------------------------+
| Advantages                                | Disadvantages                           |
+===========================================+=========================================+
| Can be autoscaled.                        | Requires AWS EC2 instances              |
+-------------------------------------------+-----------------------------------------+
| Easier crash recovery                     | Requires manual configuration           |
+-------------------------------------------+-----------------------------------------+
| Very easy monitoring support (CloudWatch) | Requires AWS EBS.                       |
+-------------------------------------------+-----------------------------------------+
|                                           | Requires some AWS know how.             |
+-------------------------------------------+-----------------------------------------+
|                                           | Static files are not served from a cdn. |
+-------------------------------------------+-----------------------------------------+

This scenario is recommended if you want to rollout you application on AWS infrastructure. Usually it is non expensive
to do this as it requires micro instances and low cost storage. For more information about AWS required components
read:

   #. `AWS Instance types <http://aws.amazon.com/ec2/instance-types/>`_.
   #. `AWS EBS <http://aws.amazon.com/ebs/>`_.

Setup
-----

#. Create an AWS account. (`AWS Getting Started <http://aws.amazon.com/documentation/gettingstarted/>`_).
#. Create an EC2 instance from AWS Management Console (`EC2 setup <http://www.youtube.com/watch?v=WBro0TEAd7g>`_). 
#. SSH on EC2 instance.
#. Install Fantastico framework on the production machine (:doc:`/get_started/installation`.).
#. Goto $FANTASTICO_ROOT
#. fantastico_setup_low_usage_<os_distribution).sh (e.g fantastico_setup_low_usage_ubuntu.sh)
#. Done.

Optimization
------------

This scenario can be easily optimized by using **AWS S3** buckets for static files. This ensures faileover for static
files and very easy horizontal scaling for sites. Below you can find the new diagram:

.. image:: /images/deployment/low_usage_s3_aws.png

You can read more about **AWS S3** storage on http://aws.amazon.com/s3/. In this version of fantastico there is no
way to sync static module files with S3 buckets. This feature is going to be implemented in upcoming **Fantastico**
features. As a workaround you can easily copy **static** folder content from each module on S3 using the tool
provided from AWS Management Console.

You can see how to use AWS Management Console S3 tool on http://www.youtube.com/watch?v=1qrjFb0ZTm8

Setup with S3
-------------

#. export ROOT_PASSWD=<your root password>
#. Create an AWS account. (`AWS Getting Started <http://aws.amazon.com/documentation/gettingstarted/>`_).
#. Create an EC2 instance from AWS Management Console (`EC2 setup <http://www.youtube.com/watch?v=WBro0TEAd7g>`_). 
#. SSH on EC2 instance.
#. Install Fantastico framework on the production machine (:doc:`/get_started/installation`.).
#. Goto $FANTASTICO_ROOT/deployment
#. fantastico_setup_low_usage_s3_<os_distribution).sh --ipaddress <desired_ip> --vhost-name <desired_vhost> --uwsgi-port <uwsgi port> --root-folder <desired root folder> --modules-folder <desired modules folder> (e.g fantastico_setup_low_usage_s3_ubuntu.sh --ipaddress 127.0.0.1 --vhost-name fantastico-framework.com --uwsgi-port 12090 --root-folder \`pwd\` --modules-folder /fantastico/samples)
#. Done.

It is usually a good idea to change the number of parallel connections supported by your linux kernel:

1. sudo nano /etc/sysctl.conf
2. Search for **net.core.somaxconn**.
3. If it does not exist you can add net.core.somaxconn = 8192 to the bottom of the file.
4. Restart the os.