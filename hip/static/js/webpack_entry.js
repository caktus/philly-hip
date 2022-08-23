/**
 * Javascript files must be imported here.
 * Webpack uses this file as the entry-point for bundling.
 */

 import jQuery from 'jquery'
 /*
   Certain legacy libraries (e.g. django-el-pagination) require
   access to a global jQuery instance, which we can link in here.
 */
 window.$ = window.jQuery = jQuery;
 
 /** Sentry Init
  *
  * This import, if you choose to use sentry logging for javascript, should stay at the top of this file.
  *
  */
 // import '../../../apps/home/static/js/sentryInit';
 
 /** App imports
  *
  * Import javascript for your apps here
  *
  */
//  import '../../../apps/{{cookiecutter.primary_app}}/assets/js/main';
//  import '../bundles/main';
 import './index.js';
