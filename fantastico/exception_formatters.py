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
.. py:module:: fantastico.exception_formatters
'''

from abc import ABCMeta, abstractmethod # pylint: disable=W0611
import json
import urllib

class ExceptionFormatter(object, metaclass=ABCMeta):
    '''This class provides a contract for formatting dictionary representation of an exception to a string.'''

    @abstractmethod
    def format_ex(self, ex_desc, ctx=None):
        '''This method must be overriden in order to transform the given exception descriptor into a suitable string.

        :param ex_desc: A dictionary containing various information about exception.
        :type ex_desc: dict
        :param ctx: A dictionary containing additional information useful for transforming exception descriptor to string.
        :type ctx: dict
        :returns: A string representation of the given dictionary.
        :rtype: string'''

class ExceptionFormattersFactory(object):
    '''This class provides the factory for obtaining a suitable exception formatter for a requested exception format.'''

    JSON = "json"
    FORM = "form"
    HASH = "hash"

    def __init__(self):
        self._supported_formatters = {self.JSON: JsonExceptionFormatter,
                                      self.FORM: FormUrlEncodedExceptionFormatter,
                                      self.HASH: HashUrlEncodedExceptionFormatter}

    def get_formatter(self, ex_format):
        '''This method returns a concrete exception formatter matching ex_format. If no suitable formatter is found an exception
        is raised.'''

        formatter_cls = self._supported_formatters.get(ex_format, DummyExceptionFormatter)

        return formatter_cls()

class JsonExceptionFormatter(ExceptionFormatter):
    '''This class provides a concrete formatter which transforms exception descriptors into json strings.'''

    def format_ex(self, ex_desc, ctx=None):
        '''This method converts the given dictionary into a json representation.'''

        ex_desc = ex_desc or "{}"

        return json.dumps(ex_desc)

class FormUrlEncodedExceptionFormatter(ExceptionFormatter):
    '''This class provides a formatter which tranform exception descriptors into url encoded query parameters.'''

    def format_ex(self, ex_desc, ctx=None):
        '''This method transform the given exception descriptor into query parameters appended to redirect uri from ctx.'''

        ex_desc = ex_desc or {}
        ctx = ctx or {}

        redirect_uri = ctx["redirect_uri"]
        keys = sorted(ex_desc.keys())

        hash_pos = redirect_uri.rfind("#")

        if hash_pos == -1:
            hash_pos = len(redirect_uri)

        result = [redirect_uri[:hash_pos]]

        if result[-1].find("?") == -1:
            result.append("?")
        else:
            result.append("&")

        for key in keys:
            result.append("%s=%s" % (key, urllib.parse.quote(ex_desc[key])))
            result.append("&")

        if result[-1] == "&":
            del result[-1]

        result.append(redirect_uri[hash_pos:])

        return "".join(result)

class HashUrlEncodedExceptionFormatter(ExceptionFormatter):
    '''This class provides a formatter similar to :py:class:`FormUrlEncodedExceptionFormatter` with the only difference that
    query parameters are added into hash section rather than http query parameters section of redirect uri.'''

    def format_ex(self, ex_desc, ctx=None):
        '''This method transform ex_desc into a hash section of redirect_uri specified in ctx.'''

        ex_desc = ex_desc or {}
        ctx = ctx or {}

        redirect_uri = ctx["redirect_uri"]

        if len(ex_desc.keys()) == 0:
            return redirect_uri

        keys = sorted(ex_desc.keys())

        result = [redirect_uri]

        if redirect_uri.rfind("#") == -1:
            result.append("#")
        else:
            result.append("&")

        for key in keys:
            result.append("%s=%s" % (key, urllib.parse.quote(ex_desc[key])))
            result.append("&")

        if result[-1] == "&":
            del result[-1]

        return "".join(result)

class DummyExceptionFormatter(ExceptionFormatter):
    '''This class provides a very simple formatter which transform exception descriptors into empty strings. You should not use
    this formatter directly. It is designed for internal Fantastico usage.'''

    def format_ex(self, ex_desc, ctx=None):
        '''This method simply returns an empty string.'''

        return ""
