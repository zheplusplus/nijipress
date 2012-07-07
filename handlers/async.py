import json

import base
import models.comment

def comments_to_dicts(comments):
    return [{
        'email_md5': c.email_md5,
        'author': c.author,
        'url': c.url,
        'date': str(c.date),
        'content': c.esc_content,
    } for c in comments]

class CommentsLoader(base.BaseView):
    def post(self):
        try:
            pid = int(self.request.get('post'))
            clist = base.comments_for_client(models.comment.by_post_id(pid))
            self.response.out.write(json.dumps(comments_to_dicts(clist)))
        except ValueError:
            self.error(404)
