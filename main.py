import wsgiref.handlers
import webapp2
import importlib

import render
import handlers.base
import handlers.async
import handlers.comments
import handlers.usr
import handlers.postmgr
import handlers.siteconf

modules = [
    'browse',
    'rss',
    'sitemap',
    'postmgr',
]

def main(debug_mode):
    for m in modules:
        importlib.import_module('handlers.' + m)

    app = webapp2.WSGIApplication(handlers.base.all_routes + [
        ('/json/loadpostbyid', handlers.async.LoadPostById),
        ('/json/loadcomments', handlers.comments.ByPostLoader),
        ('/json/leavecomment', handlers.comments.Receiver),
        ('/json/loadpendingcomments', handlers.comments.PendingLoader),
        ('/json/approvecomments', handlers.comments.Approve),
        ('/json/clearpending', handlers.comments.ClearPending),
        ('/json/loadapprovedcomments', handlers.comments.ApprovedLoader),
        ('/json/deletecomments', handlers.comments.Deleter),
        ('/json/deleteblogroll', handlers.siteconf.DeleteBlogroll),
        ('/json/previewpost', handlers.postmgr.Preview),
        ('/json/submitpost', handlers.postmgr.Receiver),
        ('/c/comments', render.admin_page_renderer('approved_comments.html')),
        ('/c/pendingcomments', render.admin_page_renderer(
                                    'pending_comments.html')),
        ('/c/reg', render.page_renderer('register.html')),
        ('/c/login', render.page_renderer('login.html')),
        ('/c/init', render.page_renderer('init_admin.html')),
        ('/json/register', handlers.usr.RegisterUser),
        ('/json/login', handlers.usr.UserLogin),
        ('/json/newadmin', handlers.usr.NewAdmin),
        ('/c/siteconf', render.page_renderer('siteconf.html')),
        ('/c/savesiteconf', handlers.siteconf.Save),
        ('/about', render.page_renderer('about.html')),
        ('/.*', handlers.base.BaseView),
    ], debug=debug_mode)
    wsgiref.handlers.CGIHandler().run(app)
    return app

application = main(True)
