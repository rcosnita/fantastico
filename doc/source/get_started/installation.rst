Installation manual
-------------------

In this section you can find out how to configure fantastico framework for different purposes.

Developing a new fantastico project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Currently fantastico is in early stages so we did not really use it to create new projects. The desired way we want
to provide this is presented below:

pip-3.2 install fantastico

Done, now you are ready to follow our tutorials about creating new projects.


Contributing to fantastico framework
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fantastico is an open source MIT licensed project to which any contribution is welcomed. If you like this framework idea
and you want to contribute do the following (I assume you are on an ubuntu machine):

.. code-block:: bash

   #. Create a github account.
   #. Ask for permissions to contribute to this project (send an email to radu.cosnita@gmail.com) - I will gladly grant you permissions.
   #. Create a folder where you want to hold fantastico framework files. (e.g worspace_fantastico)
   #. cd ~/workspace_fantastico
   #. git clone git@github.com:rcosnita/fantastico
   #. sudo apt-get install python3-setuptools
   #. sh virtual_env/setup_dev_env.sh
   #. cd ~/workspace_fantastico
   #. git clone git@github.com:rcosnita/fantastico fantastico-doc
   #. git checkout gh-pages

Now you have a fully functional fantastico workspace. I personally use PyDev and spring toolsuite but you are free to use 
whatever editor you want. The only rule we follow is *always keep the code stable*. To check the stability of your contribution
before commiting the code follow the steps below:

.. code-block:: bash

   #. cd ~/workspace_fantastico/fantastico/fantastico
   #. sh run_tests.sh (we expect no failure in here)
   #. sh run_pylint.sh (we expect 9+ rated code otherwise the build will fail).
   #. cd ~/workspace_fantastico/fantastico
   #. export BUILD_NUMBER=1
   #. ./build_docs.sh (this will autogenerate documentation).
   #. Look into ~/workspace_fantastico/fantastico-doc
   #. Here you can see the autogenerated documentation (do not commit this as Jenkins will do this for you).
   #. Be brave and push your newly awesome contribution.