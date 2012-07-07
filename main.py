import wsgiref.handlers
import webapp2

import base
import browse
import handlers.async
from admin import post
from admin import usr
from admin import siteconf
from admin import comments
import rss
import sitemap

if __name__ == '__main__':
    application = webapp2.WSGIApplication([
        ('/', browse.Index),
        ('/json/loadcomments', handlers.async.CommentsLoader),
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
        ('/about', base.About),
        ('/rss', rss.Build),
        ('/sitemap.*', sitemap.Build),
        ('/.*', base.NotFound),
    ], debug=True)
    wsgiref.handlers.CGIHandler().run(application)
