Changes
=======

* v0.1.1
   * Favicon route handling.
   * Deployment scripts error handling and root folder execution (rather than execution only for deployment subfolder).
   * I updated mvc how to article to use get_records_paged instead of all_pageed method (it used to be a bug in documentation).

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