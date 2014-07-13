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

.. py:module:: fantastico.settings
'''

from fantastico.exceptions import FantasticoSettingNotFoundError
from fantastico.rendering.component import Component
from fantastico.utils import instantiator
import os

class BasicSettings(object):
    '''This is the core class that describes all available settings of fantastico framework. For convenience all options
    have default values that ensure minimum functionality of the framework. Below you can find an example of three possible
    configuration: Dev / Stage / Production.

    .. image:: /images/core/settings.png

    As you can see, if you want to overwrite basic configuration you simply have to extend the class and set new values
    for the attributes you want to overwrite.
    '''

    @property
    def installed_middleware(self):
        '''Property that holds all installed middlewares.'''

        return ["fantastico.middleware.request_middleware.RequestMiddleware",
                "fantastico.middleware.model_session_middleware.ModelSessionMiddleware",
                "fantastico.middleware.routing_middleware.RoutingMiddleware",
                "fantastico.oauth2.middleware.exceptions_middleware.OAuth2ExceptionsMiddleware",
                "fantastico.oauth2.middleware.tokens_middleware.OAuth2TokensMiddleware"]

    @property
    def supported_languages(self):
        '''Property that holds all supported languages by this fantastico instance.'''

        return ["en_us"]

    @property
    def routes_loaders(self):
        '''This property holds all routes loaders available.'''

        return ["fantastico.routing_engine.dummy_routeloader.DummyRouteLoader",
                "fantastico.mvc.controller_registrator.ControllerRouteLoader",
                "fantastico.roa.resources_registrator.ResourcesRegistrator"]

    @property
    def mvc_additional_paths(self):
        '''This property defines additional packages which must be scanned for controllers. You can use this in order to specify
        custom mvc controllers location which are not found in custom components. For instance, OAuth2 controller resides
        in core packages of Fantastico.'''

        return ["fantastico.oauth2"]

    @property
    def dev_server_port(self):
        '''This property holds development server port. By default this is 12000.'''

        return 12000

    @property
    def dev_server_host(self):
        '''This property holds development server hostname. By default this is localhost.'''

        return "localhost"

    @property
    def templates_config(self):
        '''This property holds configuration of templates rendering engine. For the moment this influence how
        `Jinja2 <http://jinja.pocoo.org/docs/>`_ acts.'''

        return {"block_start_string": "{%",
                "block_end_string": "%}",
                "variable_start_string": "{{",
                "variable_end_string": "}}",
                "comment_start_string": "{#",
                "comment_end_string": "#}",
                "trim_blocks": True,
                "optimized": False,
                "auto_reload": True,
                "extensions": [Component]}

    @property
    def database_config(self):
        '''This property holds the configuration of database. It is recommended to have all environment configured the same.
        An exception can be done for host but the rest must remain the same. Below you can find an example of functional
        configuration:

        .. code-block:: python

            config = {"drivername": "mysql+mysqlconnector",
                        "username": "fantastico",
                        "password": "12345",
                        "port": 3306,
                        "host": "localhost",
                        "database": "fantastico",
                        "additional_params": {"charset": "utf8"},
                        "show_sql": True,
                        "additional_engine_settings": {
                            "pool_size": 20,
                            "pool_recycle": 600}
                      }

        As you can see, in your configuration you can influence many attributes used when configuring the driver / database.
        **show_sql** key tells orm engine from **Fantastico** to display all generated queries.

        Moreover, by default **Fantastico** holds connections opened for 10 minutes. After 10 minutes it refreshes the connection
        and ensures no thread is using that connection till is completely refreshed.
        '''

        return {"drivername": "mysql+mysqlconnector",
                "username": "fantastico",
                "password": "12345",
                "port": 3306,
                "host": "localhost",
                "database": "fantastico",
                "additional_params": {"charset": "utf8"},
                "show_sql": False,
                "additional_engine_settings": {
                    "pool_size": 20,
                    "pool_recycle": 600}
               }

    @property
    def doc_base(self):
        '''This property defines public location of **Fantastico** documentation.'''

        return "http://rcosnita.github.io/fantastico/html/"

    @property
    def roa_api(self):
        '''This property defines the url for mapping ROA resources api. By default is **/api**. Read more about ROA on
        :doc:`/features/components/roa_discovery/roa_discovery`.'''

        return "/api"

    @property
    def oauth2_idp(self):
        '''This property holds the configuration for Fantastico default Identity Provider. In most cases you will change the
        template applied to login screen in order to customize it to your needs. If you want to change
        the template for login screen make sure your provide relative path to your components root folder
        (e.g /components/frontend/views/custom_login.html). Moreover, you can also specify the login token validity period (in
        seconds). It is recommended to set a high value (e.g 2 weeks).

        Additionaly, you can control default idp index page. Usually, Fantastico OAuth2 identity provider login page should be
        good enough.

        .. code-block:: python

            return {"client_id": "11111111-1111-1111-1111-111111111111",
                    "template": "/components/frontend/views/custom_login.html",
                    "expires_in": 1209600,
                    "idp_index": "/oauth/idp/ui/login"}
        '''

        return {"client_id": "11111111-1111-1111-1111-111111111111",
                "template": "login.html",
                "expires_in": 1209600,
                "idp_index": "/oauth/idp/ui/login"}

    @property
    def access_token_validity(self):
        '''This property defines the validity of an access token in seconds. By default, this property is set
        to 1h = 3600 seconds.'''

        return 3600
    
    @property
    def global_response_headers(self):
        '''This property defines the headers which must be appended to every response. You can use this property in order
        to globally enable cors.
        
        .. code-block:: python
        
            return {"Access-Control-Allow-Origin": "*"}
        
        By default, no global header is appended to response.
        '''
        
        return {}

class AwsStageSettings(BasicSettings):
    '''This class provides the configuration profile for Aws Stage environment integration.'''

    @property
    def database_config(self):
        '''This property is used to change the hostname used by Aws Stage environment for connecting to fantastico database.'''

        db_config = super(AwsStageSettings, self).database_config

        db_config["host"] = "fantastico.ccv3dqqpsvpf.eu-west-1.rds.amazonaws.com"
        db_config["show_sql"] = False

        return db_config

class SettingsFacade(object):
    '''For using a specific fantastico configuration you need to do two simple steps:

    * Set **FANTASTICO_ACTIVE_CONFIG** environment variable to the fully python qualified class name you want to use. E.g: :py:class:`fantastico.settings.BasicSettings`
    * In your code, you can use the following snippet to access a specific setting:

      .. code-block:: python

         from fantastico.settings import SettingsFacade

         print(SettingsFacade().get("installed_middleware"))

    If no active configuration is set in the :py:class:`fantastico.settings.BasicSettings` will be used.'''

    __ENV_ACTIVE_CONFIG = "FANTASTICO_ACTIVE_CONFIG"

    def __init__(self, environ=None):
        self._environ = environ

        if self._environ is None:
            self._environ = os.environ

        self._cached_config = None

    def get(self, name):
        '''Method used to retrieve a setting value.

        :param name: Setting name.
        :param type: string
        :returns: The setting value.
        :rtype: object'''

        try:
            self._cached_config = self._cached_config or self.get_config()

            return getattr(self._cached_config, name)
        except AttributeError as ex:
            raise FantasticoSettingNotFoundError("Attribute %s could not be obtained: %s" % (name, str(ex)))
        except Exception as ex:
            raise FantasticoSettingNotFoundError("Exception thrown for attribute %s : %s" % (name, str(ex)))

    def get_config(self):
        '''Method used to return the active configuration which is used by this facade.

        :rtype: :py:class:`fantastico.settings.BasicSettings`
        :returns: Active configuration currently used.'''

        active_config = self._environ.get(self.__ENV_ACTIVE_CONFIG) or "fantastico.settings.BasicSettings"

        self._cached_config = self._cached_config or instantiator.instantiate_class(active_config)

        return self._cached_config

    def get_root_folder(self):
        '''Method used to return the root folder of the current fantastico project (detected starting from settings)
        profile used.'''

        return instantiator.get_component_path_data(self.get_config().__class__)[1]
