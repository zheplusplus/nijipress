import wsgiref.handlers
import webapp2

import render
import handlers.base
import handlers.browse
import handlers.async
import handlers.comments
import handlers.rss
import handlers.sitemap
import handlers.usr
import handlers.postmgr
import handlers.siteconf

application = webapp2.WSGIApplication([
    ('/', handlers.browse.Index),
    ('/json/posttags', handlers.async.Tags),
    ('/json/recentposts', handlers.async.RecentPosts),
    ('/json/loadpostbyid', handlers.async.LoadPostById),
    ('/json/loadcomments', handlers.comments.ByPostLoader),
    ('/json/leavecomment', handlers.comments.Receiver),
    ('/json/loadpendingcomments', handlers.comments.PendingLoader),
    ('/json/approvecomments', handlers.comments.Approve),
    ('/json/clearpending', handlers.comments.ClearPending),
    ('/json/loadapprovedcomments', handlers.comments.ApprovedLoader),
    ('/json/deletecomments', handlers.comments.Deleter),
    ('/json/deleteblogroll', handlers.siteconf.DeleteBlogroll),
    ('/c/newpost', handlers.postmgr.NewPost),
    ('/json/previewpost', handlers.postmgr.Preview),
    ('/json/submitpost', handlers.postmgr.Receiver),
    ('/c/posts', handlers.postmgr.List),
    ('/c/edit', handlers.postmgr.Edit),
    ('/c/comments', render.admin_page_renderer('approved_comments.html')),
    ('/c/pendingcomments', render.admin_page_renderer(
                                    'pending_comments.html')),
    ('/c/reg', render.page_renderer('register.html')),
    ('/c/login', render.page_renderer('login.html')),
    ('/json/register', handlers.usr.RegisterUser),
    ('/json/login', handlers.usr.UserLogin),
    ('/c/init', handlers.usr.Init),
    ('/c/newadmin', handlers.usr.NewAdmin),
    ('/c/error', handlers.usr.Error),
    ('/c/siteconf', render.page_renderer('siteconf.html')),
    ('/c/savesiteconf', handlers.siteconf.Save),
    ('/about', render.page_renderer('about.html')),
    ('/rss', handlers.rss.Build),
    ('/sitemap.*', handlers.sitemap.Build),
    ('/.*', handlers.base.BaseView),
], debug=True)
wsgiref.handlers.CGIHandler().run(application)
