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

class ResourcesRegistry(object):
    '''This class provide the methods for registering resources into Fantastico framework and locating them by url or name and
    version. As a Developer you will not usually need access to this class.'''

    AVAILABLE_RESOURCES = {}

    AVAILABLE_URL_RESOURCES = {}

    def register_resource(self, resource):
        '''This method register a new resource into Fantastico framework. It first checks against name, url and version collision
        in order to detect as early as possible errors with the current defined resources.

        :param resource: The resource instance we want to register into Fantastico ROA registry.
        :type resource: :py:class:`fantastico.roa.resource_decorator.Resource`
        :raises fantastico.roa.roa_exceptions.FantasticoRoaDuplicateError: This exception is raised when:

            * resource name and version already registered.
            * resource url already registered.'''

        registry = ResourcesRegistry.AVAILABLE_RESOURCES
        registry_urls = ResourcesRegistry.AVAILABLE_URL_RESOURCES

        if not registry.get(resource.name):
            registry[resource.name] = {}

        resource_versions = registry[resource.name]

        if resource_versions.get(resource.version):
            raise FantasticoRoaDuplicateError("Resource %s with version %s already registered." % \
                                              (resource.name, resource.version))

        resource_versions[resource.version] = resource

        if not registry_urls.get(resource.url):
            registry_urls[resource.url] = {}

        registry_url_versions = registry_urls[resource.url]

        if registry_url_versions.get(resource.version):
            raise FantasticoRoaDuplicateError("URL %s is already taken. Can not register resource %s." % \
                                              (resource.url, resource.name))

        registry_url_versions[resource.version] = resource
