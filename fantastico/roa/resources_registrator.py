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
.. py:module:: fantastico.roa.resources_registrator
'''

from fantastico.settings import SettingsFacade
from fantastico.utils import instantiator
import os
import re

class ResourcesRegistrator(object):
    '''This class provides the algorithm for registering all defined resources. Resources discovered by this class are decorated
    by :py:class:`fantastico.roa.resource_decorator.Resource`. In the constructor of this class you can define special naming
    convention for discovered resources (through regex). Default behavior is to scan only in models folder / subfolders in all
    available files.'''

    def __init__(self, file_patterns=None):
        self._file_patterns = file_patterns or []

    def _is_file_supported(self, abspath, filename):
        '''This method determins if a given file name may contain resources or not.'''

        if os.path.isdir(os.path.join(abspath, filename)):
            return True

        for file_pattern in self._file_patterns:
            if re.search(file_pattern, filename):
                return True

        return False

    def register_resources(self, path):
        '''This method scans all files and folders from the given path, match the filenames against registered file patterns
        and import all ROA resources.'''

        instantiator.import_modules_from_folder(path,
                                                file_matcher=self._is_file_supported,
                                                settings_facade=SettingsFacade())
