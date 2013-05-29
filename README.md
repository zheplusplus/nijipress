A(nother) CMS for Google AppEngine, single user.

If you want deploy as your own app, modify

* app.yaml --- application, *version* and url for Google web tools verification
* static/favicon.ico
* static/googlexxxxxxxxxxxxxxxx.html --- the Google Webmaster authentication page
* templates/ --- change any pages as you want

To manage your site

* go to `/c/init` of your site and register a new admin
* go to `/c/login` of your site, then you may see administrator bar at the top of the page
* go to `/c/siteconf/` to configure your site
* go wherever you want

This project is published under the MIT License.
