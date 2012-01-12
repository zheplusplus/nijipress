import base
import admin.model as admin
import persist

class List(base.BaseView):
    def get(self):
        p = self.request_value('page', int)
        usr = admin.User.get_by_session(self.request)
        if not usr.admin:
            base.raise_forbidden(self)
            return
        self.put_page('templates/list_comments.html', {
                'comments': base.comments_for_client(persist.fetch_comments(p)),
                'current_page': p,
                'page_count': xrange(persist.comments_page_count()),
            })
