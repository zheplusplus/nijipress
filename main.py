import wsgiref.handlers
import webapp2

import render
import handlers.base
import handlers.browse
import handlers.async
import handlers.rss
import handlers.sitemap
import handlers.postmgr
import handlers.siteconf
import handlers.comments

if __name__ == '__main__':
    application = webapp2.WSGIApplication([
        ('/', handlers.browse.Index),
        ('/json/posttags', handlers.async.Tags),
        ('/json/recentposts', handlers.async.RecentPosts),
        ('/json/loadpostbyid', handlers.async.LoadPostById),
        ('/json/loadcomments', handlers.async.CommentsLoader),
        ('/json/leavecomment', handlers.async.CommentRecv),
        ('/json/register', handlers.async.RegisterUser),
        ('/json/login', handlers.async.UserLogin),
        ('/c/newpost', handlers.postmgr.NewPost),
        ('/c/preview', handlers.postmgr.Preview),
        ('/c/add', handlers.postmgr.Add),
        ('/c/posts', handlers.postmgr.List),
        ('/c/edit', handlers.postmgr.Edit),
        ('/c/comments', handlers.comments.List),
        ('/c/pendingcomments', handlers.comments.ListPending),
        ('/c/delcomment', handlers.comments.Delete),
        ('/c/approvecomment', handlers.comments.Approve),
        ('/c/clearpending', handlers.comments.ClearPending),
        ('/c/reg', render.page_renderer('templates/register.html')),
        ('/c/login', render.page_renderer('templates/login.html')),
        ('/c/siteconf', render.page_renderer('templates/siteconf.html')),
        ('/c/savesiteconf', handlers.siteconf.Save),
        ('/about', render.page_renderer('templates/about.html')),
        ('/rss', handlers.rss.Build),
        ('/sitemap.*', handlers.sitemap.Build),
        ('/.*', handlers.base.BaseView),
    ], debug=True)
    wsgiref.handlers.CGIHandler().run(application)
