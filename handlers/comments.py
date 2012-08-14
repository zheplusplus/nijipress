import base
import models.user
import models
import models.comment as comment
import utils.escape

class List(base.BaseView):
    @models.user.admin_only
    def get(self):
        p = self.request_value('page', int)
        self.put_page('templates/list_comments.html', {
            'comments': utils.escape.client_comments(models.comment.fetch(p)),
            'path': 'delcomment',
            'current_page': p,
            'page_count': xrange(models.comment.count_pages()),
        })

class Delete(base.BaseView):
    @models.user.admin_only
    def post(self):
        comment.Comment.get_by_id(int(self.request.get('id'))).delete()

class ListPending(base.BaseView):
    @models.user.admin_only
    def get(self):
        self.put_page('templates/list_comments.html', {
            'comments': utils.escape.client_comments(
                                        comment.PendingComment.all()),
            'path': 'approvecomment',
            'clearall': True,
        })

class Approve(base.BaseView):
    @models.user.admin_only
    def post(self):
        comment.PendingComment.get_by_id(int(self.request.get('id'))).approve()

class ClearPending(base.BaseView):
    @models.user.admin_only
    def get(self):
        comment.PendingComment.clear()
        self.redirect('/c/pendingcomments')
