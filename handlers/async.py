import time
from hashlib import sha256
import json

import base
import models.comment
import models.tag
import utils.dumpjson

class AsyncHandler(base.BaseView):
    def post(self):
        self.response.out.write(json.dumps(self.serve()))

class CommentsLoader(AsyncHandler):
    def serve(self):
        def comments_to_dicts(comments):
            return [{
                'email_md5': c.email_md5,
                'author': c.author,
                'url': c.url,
                'date': str(c.date),
                'content': c.esc_content,
            } for c in comments]
        try:
            pid = int(self.request.get('post'))
            clist = base.comments_for_client(models.comment.by_post_id(pid))
            return comments_to_dicts(clist)
        except ValueError:
            self.error(404)
            return []

class CommentRecv(AsyncHandler):
    def serve(self):
        try:
            post_id = int(self.request.get('post_id'))
            models.post.by_id(post_id)
        except ValueError:
            self.error(404)
            return []
        comment = models.comment.PendingComment()
        comment.content = self.request.get('content').strip()
        if not (0 < len(comment.content) <= 500):
            return []

        def comment_token(request):
            token = request.get('token')
            if len(token) == 0:
                token = sha256(str(time.time())).hexdigest()
            return token
        comment.author = self.request.get('author').strip()
        comment.email = self.request.get('email').strip()
        comment.ctoken = comment_token(self.request)
        url = self.request.get('url').strip()
        if len(url) > 0 and not url.startswith('http'):
            url = 'http://' + url
        comment.url = url
        comment.ipaddr = self.request.remote_addr
        comment.post_id = post_id
        if models.comment.put(comment):
            return { 'result': 'ok' }
        return {
            'result': 'pending',
            'token': comment.ctoken,
        }

class Tags(AsyncHandler):
    def serve(self):
        return models.tag.sort_by_count()

class RecentPosts(AsyncHandler):
    def serve(self):
        return [ utils.dumpjson.post_title(p)
                for p in utils.escape.client_posts(models.post.fetch(0, 8)) ]
