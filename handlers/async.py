import json
import base
import models.comment
import models.tag
import models.post
import utils.dumpjson
import utils.escape
import utils.cookie
import utils.hash

class AsyncHandler(base.BaseView):
    def post(self):
        self.response.out.write(json.dumps(self.serve()))

def dump_comments(comments, dump_func):
    return [dump_func(c) for c in utils.escape.client_comments(comments)]

class CommentsLoader(AsyncHandler):
    def serve(self):
        return dump_comments(
                models.comment.by_post_id(self.request_value('post', int)),
                utils.dumpjson.comment_view)

class CommentRecv(AsyncHandler):
    def serve(self):
        post_id = self.request_value('post_id', int)
        models.post.by_id(post_id)

        comment = models.comment.PendingComment()
        comment.content = self.request.get('content').strip()
        if not (0 < len(comment.content) <= 500):
            return []
        comment.author = self.request.get('author').strip()
        comment.email = self.request.get('email').strip()

        token = self.request_value('token', str)
        if len(token) == 0:
            token = utils.hash.comment_token(comment.email)
        comment.ctoken = token

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
                for p in utils.escape.client_posts(models.post.fetch(0, 6)) ]

class LoadPostById(AsyncHandler):
    def serve(self):
        return utils.dumpjson.post_full(utils.escape.client_post(
            models.post.by_id(self.request.get('id'))))

class RegisterUser(AsyncHandler):
    def serve(self):
        name = self.request.get('name')
        passwd_origin = self.request.get('passwd_origin')
        if len(name) < 6 or len(passwd_origin) < 6:
            return { 'result': 'fail', 'reason': 'format' }
        if models.user.User.get_by_name(name) != None:
            return { 'result': 'fail', 'reason': 'existed' }
        usr = models.user.User.new(name)
        usr.passwd = utils.hash.passwd(passwd_origin)
        usr.session_key = utils.hash.session_key(usr)
        usr.put()
        utils.cookie.update_cookie(self.response, usr.session_key)
        return { 'result': 'ok' }

class UserLogin(AsyncHandler):
    def serve(self):
        usr = models.user.User.get_by_name(self.request.get('name'))
        if usr == None or usr.passwd != utils.hash.passwd(
                                            self.request.get('passwd_origin')):
            return { 'result': 'fail', 'reason': 'invalid' }
        utils.cookie.update_cookie(self.response, usr.session_key)
        return { 'result': 'ok' }

class PendingCommentsLoader(AsyncHandler):
    @models.user.admin_only
    def serve(self):
        return [utils.dumpjson.comment_admin(c) for c in
              utils.escape.client_comments(models.comment.PendingComment.all())]

def deal_with_comments(handler, comment_class, action_mapper):
    for id in handler.request_value('ids', str).split(' '):
        try:
            action_mapper(comment_class.get_by_id(int(id)))
        except ValueError:
            pass
    return []

class ApproveComments(AsyncHandler):
    @models.user.admin_only
    def serve(self):
        return deal_with_comments(self, models.comment.PendingComment,
                                  lambda c: c.approve())

class ClearPending(AsyncHandler):
    @models.user.admin_only
    def serve(self):
        return deal_with_comments(self, models.comment.PendingComment,
                                  lambda c: c.delete())

class ApprovedCommentsLoader(AsyncHandler):
    @models.user.admin_only
    def serve(self):
        return dump_comments(
                models.comment.fetch(self.request_value('start', int)),
                utils.dumpjson.comment_admin)

class DeleteComments(AsyncHandler):
    @models.user.admin_only
    def serve(self):
        return deal_with_comments(self, models.comment.Comment,
                                  lambda c: c.delete())
