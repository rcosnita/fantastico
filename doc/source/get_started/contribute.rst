Contribute
==========

Fantastico framework is open source so every contribution is welcome. For the moment we are looking for more developers willing
to contribute.

Code contribution
-----------------

If you want to contribute with code to fantastico framework there are a simple set of rules that you must follow:

   * Write unit tests (for the code / feature you are contributing). 
   * Write integration tests (for the code / feature you are contributing).
   * Make sure your code is rated above 9.5 by pylint tool.
   * In addition integration tests and unit tests must cover 95% of your code.

In order for each build to remain stable the following hard limits are imposed:

   #. Unit tests must cover >= 95% of the code.
   #. Integration tests must cover >= 95% of the code.
   #. Code must be rated above 9.5 by pylint.
   #. Everything must pass.
   
When you push on master a set of jobs are cascaded executed:

   #. Run all unit tests job.
   #. Run all integration tests job (only if unit tests succeeds).
   #. Generate documentation and publish it (only if integration tests job succeeds).
   
You can follow the above build process by visiting `Jenkins build <http://jenkins.scrum-expert.ro:8080/job/fantastico-framework/>`_.
Login with your github account and everything should work smoothly.

In the end do not forget that in Fantastico framework we love to develop against a **stable** base. We really think code will have
high quality and zero bugs.   

Writing unit tests
~~~~~~~~~~~~~~~~~~

For better understanding how to write unit tests see the documentation below:

.. autoclass:: fantastico.tests.base_case.FantasticoUnitTestsCase
   :members:
   :private-members: 
   
Writing integration tests
~~~~~~~~~~~~~~~~~~~~~~~~~

For better understanding how to write integration tests see the documentation below:

.. autoclass:: fantastico.tests.base_case.FantasticoIntegrationTestCase
   :members:
   :private-members: 