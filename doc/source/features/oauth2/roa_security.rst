ROA OAUTH2 Security
===================

In this document we continue the discussion about Resource Oriented Architecture encouraged by Fantastico. Here you can
find how to secure your resources.

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