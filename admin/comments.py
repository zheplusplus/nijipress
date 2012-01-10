import base
import admin.model as admin
from persist import recent_comments as get_comments

class List(base.BaseView):
    def get(self):
        usr = admin.User.get_by_session(self.request)
        if not usr.admin:
            base.raise_forbidden(self)
            return
        self.put_page('templates/list_comments.html', {
                'comments': get_comments(),
            })
