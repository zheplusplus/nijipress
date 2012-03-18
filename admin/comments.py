import base
import admin.model as admin
import models.post
from models.comment import Comment

class List(base.BaseView):
    def get(self):
        p = self.request_value('page', int)
        usr = admin.User.get_by_session(self.request)
        if not usr.admin:
            return base.raise_forbidden(self)
        self.put_page('templates/list_comments.html', {
                'comments': base.comments_for_client(models.comment.fetch(p)),
                'current_page': p,
                'page_count': xrange(models.comment.count_pages()),
            })

class Delete(base.BaseView):
    def get(self):
        p = self.request_value('page', int)
        usr = admin.User.get_by_session(self.request)
        if not usr.admin:
            return base.raise_forbidden(self)
        Comment.get_by_id(int(self.request.get('id'))).delete()
        self.redirect('/c/comments')
