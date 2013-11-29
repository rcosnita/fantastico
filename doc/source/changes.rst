Changes
=======

Feedback
--------

I really hope you enjoy using Fantastico framework as much as we love developing it. Your feedback is highly appreciated
so do not hesitate to get in touch with us (for support, feature requests, suggestions, or everything else is on your mind):
`Provide feedback <https://docs.google.com/forms/d/1tKBopU3lfDB_w8F4h7Rl1Rn4uydAJq-nha09L_ptJck/edit?usp=sharing>`_

Versions
--------

* v0.5.1 (Work in progress)

   * Add a tutorial for creating TODO application based on ROA.
   * Fix roa discovery component fsdk syncdb bug on subsequent runs.
   * Fix roa api cors support.

* v0.5.0 (`Provide feedback <https://docs.google.com/forms/d/1tKBopU3lfDB_w8F4h7Rl1Rn4uydAJq-nha09L_ptJck/edit?usp=sharing>`_)

   * Added specification for auto generated API for resources.
   * Added OAUTH2 draft implementation details for Fantastico.
   * Added Identity Provider draft specification.
   * Added REST API Standard for ROA (Resource Oriented Architecture).
   * Added REST filter parser implementation using fast ll grammar for ROA (Resource Oriented Architecture).
   * Added auto generated APIs for resources (Resource Oriented Architecture).
   * Improved routing loaders so that multiple methods can serve separate http verbs of a route.
   * Added support for multiple routes mapped on the same controller.
   * Fixed a bug in MySql connections pool (not recycling correctly after a long idle period).
   * I changed thread local MySql connection strategy to request based.

* v0.4.1 (`Provide feedback <https://docs.google.com/forms/d/1tKBopU3lfDB_w8F4h7Rl1Rn4uydAJq-nha09L_ptJck/edit?usp=sharing>`_)
   * Fix a bug into analytics component sample data insert.
   * Fix a bug into component rendering for no json responses coming for given url.

* v0.4.0 (`Provide feedback <https://docs.google.com/forms/d/1tKBopU3lfDB_w8F4h7Rl1Rn4uydAJq-nha09L_ptJck/edit?usp=sharing>`_)
   * Fantastico SDK commands display official link to command documentation.
   * Fantastico SDK syncdb command.
   * Standard detection of database tables module setup / data insert created.
   * Multiple tracking codes extension integrated into fantastico contrib.
   * Dynamic pages extension integrated into fantastico contrib.
   * Direct feedback channel integrated into documentation (`Provide feedback <https://docs.google.com/forms/d/1tKBopU3lfDB_w8F4h7Rl1Rn4uydAJq-nha09L_ptJck/edit?usp=sharing>`_)

* v0.3.0
   * Fantastico SDK core is available.
   * Fantastico SDK activate-extension command is available.
   * Samples of how to activate extensions for an existing project are provided.

* v0.2.2
   * Update dynamic menu activation documentation.
   * Fix a serious bug in engine management and too many sql connections opened.
   * Fix a bug in db session close when an unexpected error occurs when opening the connection.
   * Add extensive unit tests for db session management.

* v0.2.1
   * Fix packaging of pypi package. Now it is usable and contains rendering package as well as contrib package.

* v0.2.0
   * Framework documentation is tracked using Google Analytics
   * Component reusage is done using {% component %} tag.
   * Dynamic menu pluggable component can be used out of the box.
   * MVC documentation improvements.
   * Fix a bug in DB session management cache when configuration was changed at runtime.

* v0.1.2
   * Nginx config file now also maps www.<vhost_name>
   * Redirect support from controllers
   * Setup fantastico framework script does not override deployment files anymore

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