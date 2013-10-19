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
.. py:module:: fantastico.contrib.roa_discovery.roa_helper
'''

def calculate_resource_url(roa_api, resource, version):
    '''This method calculates resource API url based on the given resource object and version.'''

    url = "%(api_url)s/%(version)s%(url)s" % \
            {"api_url": roa_api,
             "version": version,
             "url": resource.url}

    return url

def normalize_absolute_roa_uri(roa_api):
    '''This method normalize a given url so that it does not include protocol and host sections.'''

    roa_api = roa_api.lower()

    if not roa_api.startswith("http") and not roa_api.startswith("https"):
        return roa_api

    segments = roa_api.split("/")

    if len(segments) < 4:
        return "/"

    return "/%s" % "/".join(segments[3:])
