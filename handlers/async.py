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

def comment_token(request):
    import time
    from hashlib import sha256
    token = request.get('token')
    if len(token) == 0:
        token = sha256(str(time.time())).hexdigest()
    return token

class CommentRecv(base.BaseView):
    def post(self):
        try:
            post_id = int(self.request.get('post_id'))
            models.post.by_id(post_id)
        except ValueError:
            return self.error(404)
        comment = models.comment.PendingComment()
        comment.content = self.request.get('content').strip()
        if 0 < len(comment.content) <= 500:
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
                return self.response.out.write(json.dumps({ 'result': 'ok' }))
            self.response.out.write(json.dumps({
                'result': 'pending',
                'token': comment.ctoken,
            }))
