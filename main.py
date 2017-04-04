import wsgiref.handlers
import webapp2

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
]

def main(debug_mode):
    for m in modules:
        importlib.import_modules('handlers.' + m)

    application = webapp2.WSGIApplication(handlers.base.all_routes + [
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
        ('/c/init', render.page_renderer('init_admin.html')),
        ('/json/register', handlers.usr.RegisterUser),
        ('/json/login', handlers.usr.UserLogin),
        ('/json/newadmin', handlers.usr.NewAdmin),
        ('/c/siteconf', render.page_renderer('siteconf.html')),
        ('/c/savesiteconf', handlers.siteconf.Save),
        ('/about', render.page_renderer('about.html')),
        ('/.*', handlers.base.BaseView),
    ], debug=debug_mode)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main(True)
