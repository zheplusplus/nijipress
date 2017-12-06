import wsgiref.handlers
import webapp2
import importlib

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
    'misc',
]

def main():
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
        ('/json/register', handlers.usr.RegisterUser),
        ('/json/login', handlers.usr.UserLogin),
        ('/json/newadmin', handlers.usr.NewAdmin),
        ('/c/savesiteconf', handlers.siteconf.Save),
        ('/.*', handlers.base.BaseView),
    ], debug=False)
    wsgiref.handlers.CGIHandler().run(app)
    return app

application = main()
