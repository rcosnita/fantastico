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

        @Controller(url="/blogs/1/posts/", method="GET", 
                    models={"Post": "fantastico.plugins.blog.models.posts.Post"])
        def list_blog_posts(self, request):
            Post = request.models.Post
        
            blog_id = int(request.params.id)
        
            posts = Post.all_paged(start_record=1,  
                                   sort_expr=[asc(Post.created_date), desc(Post.title)],
                                   where_expr=[eq_(Post.blog_id, blog_id)])
                            
            response = Response()
            response.text = self.load_template("/posts_listing.html", 
                                               {"posts": posts, 
                                                "blog_id": blog_id})
            
            return response
            
Now you have a fully functional controller that will list all posts.

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