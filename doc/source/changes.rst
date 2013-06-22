Changes
=======

* v0.2.0
   * Provide sample file for monit integration (keep alive checks).
   * How to configure an EC2 / Ubuntu OS production environment for hosting fantastico projects.
   * Inline component rendering in pages / template markup
   
* v0.1.2
   * Nginx config file now also maps www.<vhost_name>
   * Redirect support from controllers
   * Dynamic pages component for reading routes from database (useful in many web site scenarios).   

* v0.1.1
   * Favicon route handling.
   * Deployment scripts error handling and root folder execution (rather than execution only for deployment subfolder).
   * MVC how to article was changed to use get_records_paged instead of all_paged method (it used to be a bug in documentation).
   * DB Session manager was changed from one singleton connection to connection / request.
   * FantasticoIntegrationTestCase now has a property that holds os environment variable name for setting up Fantastico active config. 

* v0.1.0
   * Built in router that can be easily extended.
   * WebOb Request / Response architecture.
   * Request context support for accessing various attributes (current language, current user and other attributes).
   * Multiple project profiles support.
   * Database simple configuration for multiple environments.  
   * Model - View - Controller support.
   * Automatic model facade generator.
   * Model facade injection into Controllers.   
   * Templating engine support for views (jinja2).
   * Documentation generator for pdf / html / epub formats.
   * Automatic framework packaging and deployment.
   * Helper scripts for creating projects based on Fantastico.
   * Easy rollout script for running Fantastico projects behind nginx.
   * Rollout scenarios for deploying Fantastico projects on Amazon (AWS).
   * How to sections for creating new projects and components using Fantastico.