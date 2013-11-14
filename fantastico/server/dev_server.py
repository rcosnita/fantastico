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
.. py:module:: fantastico.server.dev_server
'''
from fantastico.middleware.fantastico_app import FantasticoApp
from fantastico.settings import SettingsFacade
from wsgiref.simple_server import make_server

class DevServer(object):
    '''This class provides a very simple wsgi http server that embeds Fantastico framework into it. As developer you can use
    it to simply test your new components.'''

    def __init__(self, settings_facade=SettingsFacade):
        self._settings_facade = settings_facade()

        self._httpd = None
        self.port = None
        self.hostname = None

    @property
    def started(self):
        '''Property used to tell if development server is started or not.'''

        return self._httpd is not None

    def start(self, build_server=make_server, app=FantasticoApp):
        '''This method starts a WSGI development server. All attributes like port, hostname and protocol are read from
        configuration file.'''

        self.port = self._settings_facade.get("dev_server_port")
        self.hostname = self._settings_facade.get("dev_server_host")

        self._httpd = build_server(self.hostname, self.port, app())

        self._httpd.serve_forever()

    def stop(self):
        '''This method stops the current running server (if any available).'''

        if self._httpd:
            try:
                self._httpd.shutdown()
                self._httpd.socket.close()
            finally:
                self._httpd = None

if __name__ == "__main__":
    SERVER = DevServer()
    SERVER.start()
