A(nother) CMS for Google AppEngine, single user.

If you want deploy as your own app, modify

* app.yaml --- application, version and url for Google web tools verification
* static/favicon.ico
* conf.py --- for RSS use, the site information
* templates/analytics.htmlt --- for Google Analytics, will be added to the about page, the index page and each post
* templates/ --- change any pages as you want

To manage your site

* go to `/c/reg` of your site and register a new user
* go to Google AppEngine dashboard -> Datastore Viewer, choose `User`
* edit the user you have just registered, change field `admin` to `True`, save
* go to `/` of your site, then you may see administrator bar at the top of the page
* go wherever you want
