'''
Copyright 2013 Cosnita Radu Viorel

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. codeauthor:: Radu Viorel Cosnita <radu.cosnita@gmail.com>
.. py:module:: fantastico.roa.resources_registry
'''
from fantastico.roa.roa_exceptions import FantasticoRoaDuplicateError
from fantastico.utils.singleton import Singleton

@Singleton()
class ResourcesRegistry(object):
    '''This class provide the methods for registering resources into Fantastico framework and locating them by url or name and
    version. As a Developer you will not usually need access to this class.'''

    _RESOURCE_LATEST_VERSION = "latest"

    @property
    def available_resources(self):
        '''This readonly property returns the indexed resources by name.'''

        return self._available_resources

    @property
    def available_url_resources(self):
        '''This readonly property returns the indexed resources by urk.'''

        return self._available_url_resources

    _available_resources = {}
    _available_url_resources = {}

    def register_resource(self, resource):
        '''This method register a new resource into Fantastico framework. It first checks against name, url and version collision
        in order to detect as early as possible errors with the current defined resources.

        :param resource: The resource instance we want to register into Fantastico ROA registry.
        :type resource: :py:class:`fantastico.roa.resource_decorator.Resource`
        :raises fantastico.roa.roa_exceptions.FantasticoRoaDuplicateError: This exception is raised when:

            * resource name and version already registered.
            * resource url already registered.'''

        self._register_resource_in_resources(resource)

        self._register_resource_in_urls(resource)

    def _register_resource_in_resources(self, resource):
        '''This method registers a given resource into AVAILABLE_RESOURCES dictionary.'''

        registry = self._available_resources

        if not registry.get(resource.name):
            registry[resource.name] = {}

        resource_versions = registry[resource.name]

        if resource_versions.get(resource.version):
            raise FantasticoRoaDuplicateError("Resource %s with version %s already registered." % \
                                              (resource.name, resource.version))

        resource_versions[resource.version] = resource

        self._update_latest_version(resource_versions, resource)

    def _register_resource_in_urls(self, resource):
        '''This method registers a given resource into AVAILABLE_URLS dictionary.'''

        registry_urls = self._available_url_resources

        if not registry_urls.get(resource.url):
            registry_urls[resource.url] = {}

        registry_url_versions = registry_urls[resource.url]

        if registry_url_versions.get(resource.version):
            raise FantasticoRoaDuplicateError("URL %s is already taken. Can not register resource %s." % \
                                              (resource.url, resource.name))

        registry_url_versions[resource.version] = resource

        self._update_latest_version(registry_url_versions, resource)

    def _update_latest_version(self, registry, resource):
        '''This method updates the registry latest version to point to the given resource (if necessary).'''

        for registered_version in registry.keys():
            if registered_version == self._RESOURCE_LATEST_VERSION:
                continue

            if registered_version > resource.version:
                return

        registry[self._RESOURCE_LATEST_VERSION] = resource

    def _find_resource_in_registry(self, registry, resource_id, version):
        '''This method returns a resource from a given registry by a given id (resource name or resource url) and resource
        version.'''

        if not registry.get(resource_id):
            return

        if not registry[resource_id].get(version):
            return

        return registry[resource_id][version]

    def find_by_name(self, name, version=_RESOURCE_LATEST_VERSION):
        '''This method returns a registered resource under the given name and version.

        :param name: The resource name.
        :type name: string
        :param version: The numeric version of the resource or **latest**.
        :type version: string
        :returns: The resource found or None.
        :rtype: :py:class:`fantastico.roa.resource_decorator.Resource`
        '''

        registry = self._available_resources

        return self._find_resource_in_registry(registry, name, version)

    def find_by_url(self, url, version=_RESOURCE_LATEST_VERSION):
        '''This method returns a registered resource under the given url and version.

        :param name: The resource name.
        :type name: string
        :param version: The numeric version of the resource or **latest**.
        :type version: string
        :returns: The resource found or None.
        :rtype: :py:class:`fantastico.roa.resource_decorator.Resource`'''

        registry = self._available_url_resources

        return self._find_resource_in_registry(registry, url, version)

    def all_resources(self):
        '''This method returns a list of all registered resources order by name and version. It is extremely useful for
        introspecting Fantastico ROA platform.'''

        registry = self._available_resources

        resources = []

        for name in registry.keys():
            resources.extend(registry[name].values())

        return sorted(resources)

    def _get_latest_version(self, registry):
        '''This method obtains the latest version resource from the list of available versions.'''

        resource_latest = None

        for registered_version in registry.keys():
            if registered_version == self._RESOURCE_LATEST_VERSION:
                continue

            resource = registry[registered_version]

            if not resource_latest:
                resource_latest = resource

            if resource.version > resource_latest.version:
                resource_latest = resource

        return resource_latest

    def _unregister_registry_resource(self, registry, resource_id, version):
        '''This method unregister a given resource from the given registry.'''

        versions = registry.get(resource_id)

        if not versions:
            return

        resource = versions.get(version)

        if resource:
            del versions[version]

        resource_latest = self._get_latest_version(versions)

        if resource_latest:
            versions[self._RESOURCE_LATEST_VERSION] = resource_latest
        else:
            del versions[self._RESOURCE_LATEST_VERSION]

        return resource

    def unregister_resource(self, name, version):
        '''This method unregister a resource version. If the given resource is not found no exception is raised. Once a resource
        is unregistered latest version is recalculated. The resource is completely removed from AVAILABLE_RESOURCES and
        AVAILABLE_URLS dictionaries.

        :param name: Resource name.
        :type name: string
        :param version: Resource version. If you specify **latest** it will have no effect.
        :type version: float
        '''

        if version == self._RESOURCE_LATEST_VERSION:
            return

        registry_resources = self._available_resources
        registry_urls = self._available_url_resources

        resource = self._unregister_registry_resource(registry_resources, name, version)

        if not resource:
            return

        self._unregister_registry_resource(registry_urls, resource.url, version)
