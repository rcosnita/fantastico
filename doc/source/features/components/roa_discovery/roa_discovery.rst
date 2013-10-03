ROA Auto discovery
==================

REST relies on hypermedia and links in order to decouple clients from physical location of resources. In Fantastico,
we allow clients to introspect the platform in order to know which are the registered resources. Following some simple steps
you can enable autodiscovery of resources.

Integration
-----------

#. Activate **ROA Discovery** extension.

   .. code-block:: bash

      fsdk activate-extension --name roa-discovery --comp-root <comp_root>

#. Start your project
#. Access http://localhost/roa/resources

Current limitations
-------------------

   * ROA discovery supports only application/json content type for responses.

Technical summary
-----------------

.. autoclass:: fantastico.contrib.roa_discovery.discovery_controller.RoaDiscoveryController
   :members: