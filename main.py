import wsgiref.handlers
from google.appengine.ext import webapp

import base
import browse
from admin import post
from admin import usr
from admin import siteconf
from admin import comments
import rss

if __name__ == '__main__':
    application = webapp.WSGIApplication([
        ('/', browse.Index),
        ('/postcomment', browse.PostComment),
        ('/c/newpost', post.NewPost),
        ('/c/preview', post.Preview),
        ('/c/add', post.Add),
        ('/c/posts', post.List),
        ('/c/edit', post.Edit),
        ('/c/comments', comments.List),
        ('/c/pendingcomments', comments.ListPending),
        ('/c/delcomment', comments.Delete),
        ('/c/approvecomment', comments.Approve),
        ('/c/clearpending', comments.ClearPending),
        ('/c/reg', usr.Register),
        ('/c/newusr', usr.New),
        ('/c/login', usr.LoginPage),
        ('/c/auth', usr.LoginAction),
        ('/c/siteconf', siteconf.ConfigureSite),
        ('/c/savesiteconf', siteconf.Save),
        ('/rss', rss.Build),
        ('/about', base.About),
        ('/.*', base.NotFound),
    ], debug=True)
    wsgiref.handlers.CGIHandler().run(application)
