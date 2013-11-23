Step 3 - TODO frontend
======================

In this section of this tutorial we will develop the frontend for our simple todo application. At this moment you should already
have an API which supports tasks CRUD operations. More over your can order and filter tasks collection and you can request
partial representation of the tasks. (you can find out more on :doc:`/features/roa` doc page).

For frontend we will quickly develop an application using Backbone.js framework.

Create models
-------------

   #. git checkout -b step-3-create-frontend
   #. Paste the code below under fantastico-todo/todo/frontend/static/js/bootstrap.js

      .. code-block:: javascript

         /**
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
         */

         (function($) {
             Todo = {};

             Todo.Models = {};
         })(jQuery);

   #. Paste the code below under fantastico-todo/todo/frontend/static/js/models/resources_registry.js

      .. code-block:: javascript

         /**
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
         */

         (function($) {
             var registry = {},
                 endpoint = "/roa/resources";

             /**
              * This model holds the object attributes of a resource. Currently it supports only fetch through collection.
              */
             registry.Resource = Backbone.Model.extend({});

             /**
              * This collection provides access to ROA resources registered to the current project. It is recommended to code each model
              * against the registry so that location changes are not breaking client side code.
              */
             registry.ResourceCollection = Backbone.Collection.extend({
                 model: registry.Resource,
                 url: endpoint,
                 /**
                  * This method returns the resource url for a given resource name and version. If the version is omitted latest resource
                  * url is returned.
                  *
                  * @param {String} name The name of the resource we want to retrieve discovery information about.
                  * @param {String} version (Optional) The version of the resource we want to retrieve discovery information about.
                  * @returns The resource url extracted from ROA discovery registry (/roa/resources).
                  */
                 getResourceUrl: function(name, version) {
                     version = version || "latest";

                     if(this.length == 0) {
                         throw new Error("No ROA resources registered.");
                     }

                     var resources = this.at(0),
                         resource = (resources.get(name) || {})[version];

                     if(!resource) {
                         throw new Error("Resource " + name + ", version " + version + " is not registered.");
                     }

                     return resource;
                 }
             });

             Todo.Models.Registry = new registry.ResourceCollection();
             Todo.Models.Registry.fetch();
         })(jQuery);

   #. Paste the code below under fantastico-todo/todo/frontend/static/js/models/tasks.js

      .. code-block:: javascript

         /**
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
         */

         (function($) {
             var tasks = {};

             function getTasksUrl() {
                 return Todo.Models.Registry.getResourceUrl("Task");
             }

             tasks.Task = Backbone.Model.extend({
                 urlRoot: getTasksUrl
             });

             tasks.TaskCollection = Backbone.Collection.extend({
                 model: tasks.Task,
                 /**
                  * This method is overriden so that it guarantees tasks are ordered alphabetically and only id and name attributes are
                  * returned for each available task (partial resource representation).
                  */
                 url: function() {
                     var url = [getTasksUrl()];
                     url.push("?");

                     if(this._offset) {
                         url.push("offset=" + this._offset);
                     }

                     if(this._limit) {
                         url.push("&limit=" + this._limit);
                     }

                     url.push("&fields=id,name");
                     url.push("&order=asc(name)");

                     return url.join("");
                 },
                 /**
                  * In comparison with standard backbone collection fetch, ROA collections support pagination. This is why options is
                  * parsed before actually fetching the collection.
                  */
                 fetch: function(options) {
                     options = options || {};

                     this._offset = options.offset;
                     this._limit = options.limit;

                     return Backbone.Collection.prototype.fetch.call(this, options);
                 },
                 /**
                  * This method save the items returned form REST ROA api to this backbone collection. Additionally it adds the total
                  * items counter as collection property.
                  *
                  * @param {Object} response The http response coming for /api/latest/tasks collection.
                  */
                 parse: function(response) {
                     this.set({"totalItems": response.totalItems});

                     return response.items;
                 }
             });

             Todo.Models.Tasks = tasks;
         })(jQuery);

    #. We have all models in place so we are going to implement the frontend of the application in the next section.

Models implementation notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Fantastico, there is a resource registry which can be used for discovery. It is recommended to always use it to obtain your
models api urls. This will guarantee that any change of API location on server side is automatically propagated on client side.

In addition because our application is not going to use description we optimized the client side code by using ROA partial resource
representation. More over, the resources are ordered alphabetically by name.

ROA collections support pagination out of the box and tasks client side implementation shows how easily it is to provide it
for client side code.

For better understanding all the concepts used in this section you can read :doc:`/features/roa`