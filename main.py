import wsgiref.handlers
import webapp2 as webapp

import base
import browse
import handlers.async
from admin import post
from admin import usr
from admin import siteconf
from admin import comments
import rss
import sitemap


application = webapp.WSGIApplication([
    ('/', browse.Index),
    ('/json/loadcomments', handlers.async.CommentsLoader),
    ('/json/leavecomment', handlers.async.CommentRecv),
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
    ('/c/init', usr.Init),
    ('/c/newadmin', usr.NewAdmin),
    ('/c/reg', usr.Register),
    ('/c/newusr', usr.New),
    ('/c/error', usr.Error),
    ('/c/login', usr.LoginPage),
    ('/c/auth', usr.LoginAction),
    ('/c/siteconf', siteconf.ConfigureSite),
    ('/c/savesiteconf', siteconf.Save),
    ('/about', base.About),
    ('/rss', rss.Build),
    ('/sitemap.*', sitemap.Build),
    ('/.*', base.NotFound),
], debug=True)
#wsgiref.handlers.CGIHandler().run(application)
