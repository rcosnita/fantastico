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

.. py:module:: fantastico.tests.base_case
'''
from fantastico.middleware.fantastico_app import FantasticoApp
from fantastico.mvc import controller_decorators
from fantastico.settings import BasicSettings, SettingsFacade, AwsStageSettings
from fantastico.utils import instantiator
import inspect
import os
import unittest

class FantasticoBaseTestCase(unittest.TestCase):
    '''This is the base class that must be inherited by each specific test case: Unit tests / Integration tests'''

    FANTASTICO_CFG_OS_KEY = "FANTASTICO_ACTIVE_CONFIG"

    def setUp(self):
        '''We make the convention that setup method will always invoke init method for each test case.'''

        if hasattr(self, "init"):
            init = getattr(self, "init")
            init()

    def tearDown(self):
        '''We make the convention that teardown method will always invoke cleanup method for each test case.'''

        if hasattr(self, "cleanup"):
            cleanup = getattr(self, "cleanup")
            cleanup()

    @classmethod
    def setUpClass(cls):
        '''We make the convention that setUpClass method will always invoke setup_once method for each test case class.'''

        if hasattr(cls, "setup_once"):
            setup_once = getattr(cls, "setup_once")
            setup_once()


    @classmethod
    def tearDownClass(cls):
        '''We make the convention that tearDownClass method will always invoke cleanup_once method for each test case class.'''

        if hasattr(cls, "cleanup_once"):
            cleanup = getattr(cls, "cleanup_once")
            cleanup()

class FakeControllerDecorator(object):
    '''This is a simple mock that can be used to replace Controller decorator.'''

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, orig_fn):
        def fn_replace(*args, **kwargs):
            return orig_fn(*args, **kwargs)

        return fn_replace


class FantasticoUnitTestsCase(FantasticoBaseTestCase):
    '''This is the base class that must be inherited by each unit test written for fantastico.

    .. code-block:: python

        class SimpleUnitTest(FantasticoUnitTestsCase):
            def init(self):
                self._msg = "Hello world"

            def test_simple_flow_ok(self):
                self.assertEqual("Hello world", self._msg)'''

    def _get_root_folder(self):
        '''This method determines the root folder under which core is executed.'''

        return instantiator.get_component_path_data(BasicSettings)[1]

    def _get_class_root_folder(self):
        '''This methods determines the root folder under which the test is executed.'''

        return instantiator.get_component_path_data(self.__class__)[1]

    @classmethod
    def setup_once(cls):
        '''This method is overriden in order to correctly mock some dependencies:

        * :py:class:`fantastico.mvc.controller_decorators.Controller`
        '''

        cls._old_controller_decorator = controller_decorators.Controller
        controller_decorators.Controller = FakeControllerDecorator

    @classmethod
    def cleanup_once(cls):
        controller_decorators.Controller = cls._old_controller_decorator

    def check_original_methods(self, cls_obj):
        '''This method ensures that for a given class only original non decorated methods will be invoked. Extremely useful
        when you want to make sure @Controller decorator does not break your tests. It is strongly recommended to invoke
        this method on all classes which might contain @Controller decorator. It ease your when committing on CI environment.'''

        if controller_decorators.Controller != FakeControllerDecorator:
            return

        for meth_name, meth_value in inspect.getmembers(cls_obj, inspect.isfunction):
            if not hasattr(meth_value, "orig_fn"):
                continue

            setattr(cls_obj, meth_name, meth_value.orig_fn)

class FantasticoIntegrationTestCase(FantasticoBaseTestCase):
    '''This is the base class that must be inherited by each integration test written for fantastico.

    .. code-block:: python

        class SimpleIntegration(FantasticoIntegrationTestCase):
            def init(self):
                self.simple_class = {}

            def cleanup(self):
                self.simple_class = None

            def test_simple_ok(self):
                def do_stuff(env, env_cls):
                    self.assertEqual(simple_class[env], env_cls)

                self._run_test_all_envs(do_stuff)

    If you used this class you don't have to mind about restoring call methods from each middleware once they are wrapped
    by fantastico app. This is a must because otherwise you will crash other tests.
    '''

    @property
    def _envs(self):
        '''Private property that holds the environments against which we run the integration tests.'''

        return self.__envs

    @property
    def fantastico_cfg_os_key(self):
        '''This property holds the name of os environment variable used for setting up active fantastico configuration.'''

        return self.FANTASTICO_CFG_OS_KEY

    def setUp(self):
        self.__envs = [("fantastico.settings.BasicSettings", BasicSettings),
                       ("fantastico.settings.AwsStageSettings", AwsStageSettings)]
        self.__old_middlewares_call = []

        self._save_call_methods(SettingsFacade().get_config().installed_middleware)

        super(FantasticoIntegrationTestCase, self).setUp()

    def tearDown(self):
        self._restore_call_methods()

        super(FantasticoIntegrationTestCase, self).tearDown()

    def _save_call_methods(self, middlewares):
        '''This method save all call methods for each listed middleware so that later on they can be restored.'''

        self.__old_middlewares_call.append((FantasticoApp, FantasticoApp.__call__))

        for middleware_cls in middlewares:
            middleware_cls = instantiator.import_class(middleware_cls)

            self.__old_middlewares_call.append((middleware_cls, middleware_cls.__call__))

    def _restore_call_methods(self):
        '''This method restore original call methods to all affected middlewares.'''

        for middleware in self.__old_middlewares_call:
            middleware[0].__call__ = middleware[1]

    def _run_test_all_envs(self, callable_obj):
        '''This method is used to execute a callable block of code on all environments. This is extremely useful for
        avoid boiler plate code duplication and executing test logic against all environments.
        '''

        old_env = os.environ.get("FANTASTICO_ACTIVE_CONFIG") or 'fantastico.settings.BasicSettings'

        for env, settings_cls in self._envs:
            try:
                os.environ["FANTASTICO_ACTIVE_CONFIG"] = env

                callable_obj(env, settings_cls)
            finally:
                if old_env is None:
                    old_env = ""

                os.environ["FANTASTICO_ACTIVE_CONFIG"] = old_env
