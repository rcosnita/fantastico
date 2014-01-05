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
.. py:module:: fantastico.mvc.controller_registrator
'''
from fantastico.mvc.controller_decorators import Controller
from fantastico.routing_engine.routing_loaders import RouteLoader
from fantastico.settings import SettingsFacade
from fantastico.utils import instantiator
import importlib
import inspect
import os

class ControllerRouteLoader(RouteLoader):
    '''This class provides a route loader that is capable of scanning the disk and registering only the routes that
    contain a controller decorator in them. This happens when **Fantastico** servers starts. In standard configuration
    it ignores tests subfolder as well as test_* / itest_* modules.'''

    @property
    def scanned_folders(self):
        '''This property returns the currently scanned folder from where mvc routes are collected.'''

        return self._folders

    def __init__(self, settings_facade=SettingsFacade, scanned_folder=None, ignore_prefix=None):
        super(ControllerRouteLoader, self).__init__(settings_facade)

        self._scanned_folder = scanned_folder or instantiator.get_class_abslocation(self._settings_facade.get_config().__class__)

        custom_packages = self._settings_facade.get("mvc_additional_paths")

        folders = self._get_custom_packages_filelist(custom_packages)
        folders.add(self._scanned_folder)

        self._folders = list(folders)

        self._ignore_prefix = ignore_prefix or ["__init__", "__pycache__", "tests", "test", "itest"]

    def _get_custom_packages_filelist(self, custom_packages):
        '''This method returns all filenames where the given custom packages reside on disk.'''

        folders = set()

        for custom_package in custom_packages:
            package = importlib.import_module(custom_package)
            filename = inspect.getabsfile(package)

            folders.add(filename[:filename.rfind(os.path.sep)])

        return folders

    def _is_ignored_file(self, filename):
        '''This method determines if a filename is ignored or not.'''

        for prefix in self._ignore_prefix:
            if filename.startswith(prefix):
                return True

        return False

    def _register_from_folder(self, folder):
        '''This method is used for registering all modules that contains Controller from a given location.'''

        file_matcher = lambda folder, filename: not self._is_ignored_file(filename)

        instantiator.import_modules_from_folder(folder, file_matcher, self._settings_facade)

    def load_routes(self):
        '''This method is used for loading all routes that are mapped through
        :py:class:`fantastico.mvc.controller_decorators.Controller` decorator.'''

        for scanned_folder in self._folders:
            self._register_from_folder(scanned_folder)

        controller_routes = Controller.get_registered_routes()
        routes = {}

        for controller in controller_routes:
            contr_routes = controller.url

            for route in contr_routes:
                route_config = routes.get(route)

                if not route_config:
                    route_config = {}
                    routes[route] = route_config

                route_config["http_verbs"] = route_config.get("http_verbs", {})

                for method in controller.method:
                    route_config["http_verbs"][method] = controller.fn_handler.full_name

        return routes
