Controllers security
====================

Regular controllers security
----------------------------

In general, you will want to secure your controllers (:doc:`/how_to/mvc_how_to`) using OAuth2. In addition, for some controllers
(e.g UI Controllers) you will want to tell Fantastico to redirect automatically to login screen rather than returning an
**401 Unauthorized** error. Below you can find a very simple example of a ui controller which automatically redirects user to
login screen in order to obtain access:

.. code-block:: python

   @ControllerProvider()
   class SecuredController(BaseController):
      @Controller(url="/secured-controller/ui/index")
      @RequiredScopes(scopes=["greet.verbose", "greet.read"])
      def say_hello(self, request):
         return "<html><body><h1>Hello world</body></html>"

The order in which decorators are chained is extremely important becauase **@Controller** injects the request while
**@RequiredScopes** decorator uses it.

ROA OAUTH2 Security
-------------------

ROA (:doc:`/features/roa`) resource can be easily secured using OAuth2 as shown below:

.. code-block:: python

   @Resource(name="app-setting", url="/app-settings", version=1.0)
   @RequiredScopes(create="app_setting.create",
                   read="app_setting.read",
                   update="app_setting.update",
                   delete="app_setting.delete"})
   class AppSetting(BASEMODEL):
      id = Column("id", Integer, primary_key=True, autoincrement=True)
      name = Column("name", String(50), unique=True, nullable=False)
      value = Column("value", Text, nullable=False)

      def __init__(self, name, value):
         self.name = name
         self.value = value

This is an extremely convenient way to secure a resource. In addition, each argument from **@Resource** constructor is optional.
For instance, if read is not given any scope then everyone can read **AppSetting** resources.

Fantastico will autodiscover endpoints / resources which require scopes and preauthorize every call to them.

The order in which decorators are chained is extremely important.