MVC How to
==========

In this article you can see how to assemble various pieces together in order to create a feature for a virtual blog application.
If you follow this step by step guide in the end you will have a running blog which can list all posts.

Code the model
--------------

Below you can find how to easily create **post** model.

#. Create a new package called **blog**
#. Create a new package called **blog.models**
#. Create a new module called posts and paste the following code into it:

    .. code-block:: python

        class Post(BaseModel):
            __tablename__ = "posts"

            id = Column("id", Integer, primary_key=True)
            blog_id =
            title = Column("title", String(150))
            tags = Column("tags", String(150))
            created_date = Column("registered_date", DateTime(), default=datetime.now)
            content = Column("content", Text(100))

Now you have a fully functional post model mapped over **posts** table.

Code the controller
-------------------

#. Create a new package called **blog.controllers**
#. Create a new module called **blog_controller** and paste the following code into it:

    .. code-block:: python

        @ControllerProvider()
        class BlogsController(BaseController):
            @Controller(url="/blogs/(?P<blog_id>\\d{1,})/posts/$", method="GET",
                        models={"Post": "fantastico.plugins.blog.models.posts.Post"])
            def list_blog_posts(self, request, blog_id):
                Post = request.models.Post

                blog_id = int(blog_id)

                posts = Post.get_records_paged(start_record=1, end_record=100,
                                       sort_expr=[ModelSort(Post.model_cls.created_date, ModelSort.ASC),
                                                  ModelSort(Post.title, ModelSort.DESC)],
                                       filter_expr=[ModelFilter(Post.model_cls.blog_id, blog_id, ModelFilter.EQ)])

                response = Response()
                response.text = self.load_template("/posts_listing.html",
                                                   {"posts": posts,
                                                    "blog_id": blog_id})

                return response

Now you have a fully functional controller that will list first 100 posts.

Code the view
-------------

#. Create a new folder called **blog.views**
#. Create a new view under **blog.views** called *posts_listing.html* and paste the following code into it:

    .. code-block:: html

        <html>
            <head>
                <title>List all available posts from blog {{blog_id}}</title>
            </head>

            <body>
                <ul>
                {% for post in posts %}
                    <li>{{post.title}} | {{post.created_date}}</li>
                {% endfor %}
                </ul>
            </body>
        </html>

Test your application
---------------------

#. Start fantastico dev server by executing script **run_dev_server.sh** (:doc:`/get_started/dev_mode`)
#. Open a browser and visit http://localhost:12000/blogs/1/posts.