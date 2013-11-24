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
             Todo.Models.Registry.loader = Todo.Models.Registry.fetch();
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
                 idAttribute: "task_id",
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

                     url.push("&fields=task_id,name,status");
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
                     this.totalItems = response.totalItems;

                     return response.items;
                 }
             });

             Todo.Models.Tasks = tasks;
         })(jQuery);

We have all models in place so we are going to implement the frontend of the application in the next section.

Models implementation notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Fantastico, there is a resource registry which can be used for discovery. It is recommended to always use it to obtain your
models api urls. This will guarantee that any change of API location on server side is automatically propagated on client side.

In addition because our application is not going to use description we optimized the client side code by using ROA partial resource
representation. More over, the resources are ordered alphabetically by name.

ROA collections support pagination out of the box and tasks client side implementation shows how easily it is to provide it
for client side code.

For better understanding all the concepts used in this section you can read :doc:`/features/roa`.

In addition you probably noticed that static assets are created under a special folder named **static**. This allows us to easily
serve static assets from a cache server or cdn in production. You can read more about this on :doc:`/how_to/static_assets`.

Create frontend
---------------

In this section we are going to create all routes used in frontend:

   #. /frontend/ui/index
   #. /frontend/ui/tasks-list-menu
   #. /frontend/ui/tasks-list-content
   #. /frontend/ui/tasks-list-pager

This approach allows us to have a very clear separation and control of listing components of TODO application. In order to create
the frontend follow the steps below:

   #. Paste the following code under fantastico-todo/todo/frontend/todo_ui.py:

      .. code-block:: python

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
         .. py:module:: todo.frontend.ui
         '''

         from fantastico.mvc.base_controller import BaseController
         from fantastico.mvc.controller_decorators import Controller, ControllerProvider
         from webob.response import Response

         @ControllerProvider()
         class TodoUi(BaseController):
             '''This class provides all routes used by todo frontend application.'''

             @Controller(url="/frontend/ui/index")
             def get_index(self, request):
                 '''This method returns the index of todo ui application.'''

                 content = self.load_template("listing.html")

                 return Response(content)

             @Controller(url="/frontend/ui/tasks-list-menu")
             def get_tasks_menu(self, request):
                 '''This method return the tasks list menu.'''

                 content = self.load_template("listing_menu.html")

                 return Response(content)

             @Controller(url="/frontend/ui/tasks-list-content")
             def get_tasks_content(self, request):
                 '''This method returns the markup for tasks listing content area.'''

                 content = self.load_template("listing_content.html")

                 return Response(content)

             @Controller(url="/frontend/ui/tasks-list-pager")
             def get_tasks_pager(self, request):
                 '''This method returns the markup for tasks listing pagination area.'''

                 content = self.load_template("listing_pager.html")

                 return Response(content)

The final step of this tutorial requires the creation of controller code for listing tasks and CRUD operations:

   #. Paste the code below under fantastico-todo/todo/frontend/static/js/list_tasks.js:

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
             TPL_TASK = ['<div class="task">'];
             TPL_TASK.push('<div class="input-group">');
             TPL_TASK.push('<span class="input-group-addon">');
             TPL_TASK.push('<input type="checkbox" data-role="tasks-complete" data-tid="<%= task.get(\"task_id\") %>" />');
             TPL_TASK.push('</span>');
             TPL_TASK.push('<% if(task.get("status") === 0) { %>');
             TPL_TASK.push('<h3 class="form-control"><%= task.get(\"name\") %></h3>');
             TPL_TASK.push('<% } else { %>');
             TPL_TASK.push('<h3 class="form-control task-completed"><%= task.get(\"name\") %></h3>');
             TPL_TASK.push('<% } %>');
             TPL_TASK.push("</div>");
             TPL_TASK.push("<hr/>");
             TPL_TASK.push("</div>");

             TPL_TASK = TPL_TASK.join("");

             function ListingController() {
                 this._tasks = new Todo.Models.Tasks.TaskCollection();
                 this._offset = 0;
                 this._limit = 10;
                 this._fetchMoreSize = 5;
             };

             ListingController.prototype.start = function() {
                 this._tfNewTask = $("#txt-new-task");
                 this._btnComplete = $("#btn-complete-task");
                 this._btnRemove = $("#btn-remove-task");
                 this._tasksArea = $(".tasks-area");
                 this._pagerText = $(".tasks-pager").find("p");
                 this._btnPagerFetch = $(".tasks-pager").find("button");

                 this._initEvents();
             };

             ListingController.prototype._getSelectedTasks = function() {
                 var ids = [],
                     tasksChk = this._tasksArea.find("input[data-role='tasks-complete']");

                 _.each(tasksChk, function(item) {
                     item = $(item);

                     if(!item.is(":checked")) {
                         return;
                     }

                     ids.push(parseInt(item.attr("data-tid")));
                 });

                 return ids;
             };

             ListingController.prototype._initEvents = function() {
                 var self = this;

                 this._tfNewTask.keyup(function(evt) {
                     if(evt.keyCode == 13) {
                         self._createTask(self._tfNewTask.val());

                         return false;
                     }

                     return true;
                 });

                 this._btnRemove.click(function() {
                     var ids = self._getSelectedTasks();

                     self._deleteTasks(ids);
                 });

                 this._btnComplete.click(function() {
                     var ids = self._getSelectedTasks();

                     self._completeTasks(ids);
                 });

                 this._btnPagerFetch.click(function() {
                     self._fetchMoreTasks();
                 });

                 this._tasks.on("reset", function() {
                     self._tasksArea.html("");
                     self._fetchTasks();
                 });

                 this._pagerText.html("");
                 this._tasks.reset();
             };

             ListingController.prototype._fetchTasks = function() {
                 var response = this._tasks.fetch({"offset": this._offset,
                                                   "limit": this._limit}),
                     self = this;

                 response.done(function() {
                     self._tasks.each(function(task) {
                         self._renderTask(task);
                     });

                     self._showPageText();
                 });
             };

             ListingController.prototype._renderTask = function(task) {
                 var taskUi = _.template(TPL_TASK),
                     model = {"task": task},
                     taskHtml = taskUi(model);

                 this._tasksArea.append(taskHtml);
             };

             ListingController.prototype._createTask = function(taskName) {
                 this._tasks.create({"name": taskName, "status": 0});

                 this._tasks.reset();
             };

             ListingController.prototype._showPageText = function() {
                 var totalItems = this._tasks.totalItems,
                     displayedItems = Math.min(this._limit, totalItems),
                     pagesText = displayedItems + " out of " + totalItems;

                 this._pagerText.html(pagesText);
             };

             ListingController.prototype._deleteTasks = function(taskIds) {
                 this._btnRemove.button("loading");

                 taskIds = taskIds || [];

                 var deletePromises = [],
                     self = this;

                 _.each(taskIds, function(taskId) {
                     var response = new Todo.Models.Tasks.Task({"task_id": taskId}).destroy();

                     taskIds.push(response);
                 });

                 $.when.apply($, deletePromises).done(function() {
                     self._btnRemove.button("reset");

                     self._tasks.reset();
                 });
             };

             ListingController.prototype._completeTasks = function(taskIds) {
                 this._btnComplete.button("loading");

                 taskIds = taskIds || [];

                 var updatePromises = [],
                     self = this;

                 _.each(taskIds, function(taskId) {
                     var task = self._tasks.get(taskId);

                     task.set({"status": 1});

                     updatePromises.push(task.save());
                 });

                 $.when.apply($, updatePromises).done(function() {
                     self._btnComplete.button("reset");

                     self._tasks.reset();
                 });
             };

             ListingController.prototype._fetchMoreTasks = function() {
                 var newLimit = this._limit + this._fetchMoreSize;

                 newLimit = Math.min(newLimit, this._tasks.totalItems);

                 if(newLimit >= this._tasks.totalItems) {
                     this._btnPagerFetch.hide();
                 }

                 this._limit = newLimit;

                 this._tasks.reset();
             };

             Todo.Controllers.ListingController = ListingController;
         })(jQuery);

   #. Done. Now you have a fully functional todo application. Access http://localhost:12000/frontend/ui/index for seeing the results.