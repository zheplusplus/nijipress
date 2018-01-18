A(nother) CMS based on Google AppEngine, for single user.

Features / Specifications

* Implemented in Python2.7
* No other Web framework requires

Fork this repository if you want deploy as your own app, and modify the following on your need

* edit *application*, *version* and the 3rd *handlers.url* for Google web tools verification in *app.yaml*
* replace static/favicon.ico
* replace static/googlexxxxxxxxxxxxxxxx.html --- the Google Webmaster authentication page

To manage your site

* go to `/c/init` of your own site to register a new admin, at the first time you deploy this program
* go to `/c/login` to sign in, then you may see administrator bar at the top of the page
* go to `/c/siteconf/` to configure your site
