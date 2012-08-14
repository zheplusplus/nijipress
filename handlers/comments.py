import base
import models.admin
import models
import models.comment as comment
import utils.escape

class List(base.BaseView):
    def get(self):
        p = self.request_value('page', int)
        usr = models.admin.User.get_by_session(self.request)
        if not usr.admin:
            return base.raise_forbidden(self)
        self.put_page('templates/list_comments.html', {
            'comments': utils.escape.client_comments(models.comment.fetch(p)),
            'path': 'delcomment',
            'current_page': p,
            'page_count': xrange(models.comment.count_pages()),
        })

class Delete(base.BaseView):
    def post(self):
        usr = models.admin.User.get_by_session(self.request)
        if not usr.admin:
            return base.raise_forbidden(self)
        comment.Comment.get_by_id(int(self.request.get('id'))).delete()

class ListPending(base.BaseView):
    def get(self):
        usr = models.admin.User.get_by_session(self.request)
        if not usr.admin:
            return base.raise_forbidden(self)
        self.put_page('templates/list_comments.html', {
            'comments': utils.escape.client_comments(
                                        comment.PendingComment.all()),
            'path': 'approvecomment',
            'clearall': True,
        })

class Approve(base.BaseView):
    def post(self):
        usr = models.admin.User.get_by_session(self.request)
        if not usr.admin:
            return base.raise_forbidden(self)
        comment.PendingComment.get_by_id(int(self.request.get('id'))).approve()

class ClearPending(base.BaseView):
    def get(self):
        usr = models.admin.User.get_by_session(self.request)
        if not usr.admin:
            return base.raise_forbidden(self)
        comment.PendingComment.clear()
        self.redirect('/c/pendingcomments')
