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

.. py:module:: fantastico.routing_engine.routing_loaders
'''

from abc import abstractmethod, ABCMeta # pylint: disable=W0611

class RouteLoader(object, metaclass=ABCMeta):
    '''This class provides the contract that must be provided by each concrete implementation. Each route loader is responsible
    for implementing its own business logic for loading routes.

    .. code-block:: python

        class DummyRouteLoader(RouteLoader):
            def __init__(self, settings_facade):
                self_settings_facade = settings_facade

            def load_routes(self):
                return {"/index.html": {"http_verbs": {
                                                    "GET": "fantastico.plugins.static_assets.StaticAssetsController.resolve_text"
                                                    }
                                        },
                        "/images/image.png": {"http_verbs": {
                                                    "GET": "fantastico.plugins.static_assets.StaticAssetsController.resolve_binary"
                                                    }
                                             }
                }
    '''

    def __init__(self, settings_facade):
        '''
        :param settings_facade: An active instance of settings facade that can be used for accessing framework settings.
        :type settings_facade: :py:class:`fantastico.settings.SettingsFacade`
        '''
        self._settings_facade = settings_facade

    @abstractmethod
    def load_routes(self):
        '''This method must be overriden by each concrete implementation so that all loaded routes can be handled by
        fantastico routing engine middleware.'''
