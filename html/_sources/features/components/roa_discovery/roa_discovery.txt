ROA Auto discovery
==================

REST relies on hypermedia and links in order to decouple clients from physical location of resources. In Fantastico,
we allow clients to introspect the platform in order to know which are the registered resources. Following some simple steps
you can enable autodiscovery of resources.

Integration
-----------

#. Activate **ROA Discovery** extension.

   .. code-block:: bash

      fsdk activate-extension --name roa_discovery --comp-root <comp_root>

#. Start your project
#. Access http://localhost/roa/resources

By default, **ROA Discovery** extension defines a sample resource (**Sample Resource**) which must be always present in your
discovery registry.

Current limitations
-------------------

   * ROA discovery supports only application/json content type for responses.

Technical summary
-----------------

.. autoclass:: fantastico.contrib.roa_discovery.discovery_controller.RoaDiscoveryController
   :members: