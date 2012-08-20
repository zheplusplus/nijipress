import async
import models.comment
import models.user
import utils.dumpjson
import utils.hash

class Receiver(async.AsyncHandler):
    def serve(self):
        post_id = int(self.args['post_id'])
        models.post.by_id(post_id)

        comment = models.comment.PendingComment()
        comment.content = self.args['content'].strip()
        if not (0 < len(comment.content) <= 500):
            return []
        comment.author = self.args['author'].strip()
        comment.email = self.args['email'].strip()

        token = self.args['token']
        if len(token) == 0:
            token = utils.hash.comment_token(comment.email)
        comment.ctoken = token

        url = self.args['url'].strip()
        if len(url) > 0 and not url.startswith('http'):
            url = 'http://' + url
        comment.url = url
        comment.ipaddr = self.request.remote_addr
        comment.post_id = post_id
        if models.comment.put(comment):
            return dict({ 'result': 'ok' }.items() +
                    utils.dumpjson.comment_view(
                            utils.escape.client_comment(comment)).items())
        return {
            'result': 'pending',
            'token': comment.ctoken,
        }

def deal_with_comments(handler, comment_class, action_mapper):
    for id in handler.args['ids'].split(' '):
        try:
            action_mapper(comment_class.get_by_id(int(id)))
        except ValueError:
            pass
    return []

def dump_comments(comments, dump_func):
    return [ dump_func(c) for c in utils.escape.client_comments(comments) ]

class ByPostLoader(async.AsyncHandler):
    def serve(self):
        return dump_comments(models.comment.by_post_id(int(self.args['post'])),
                             utils.dumpjson.comment_view)

class PendingLoader(async.AsyncHandler):
    @models.user.admin_only
    def serve(self):
        return [ utils.dumpjson.comment_admin(c) for c in
            utils.escape.client_comments(models.comment.PendingComment.all()) ]

class Approve(async.AsyncHandler):
    @models.user.admin_only
    def serve(self):
        return deal_with_comments(self, models.comment.PendingComment,
                                  lambda c: c.approve())

class ClearPending(async.AsyncHandler):
    @models.user.admin_only
    def serve(self):
        return deal_with_comments(self, models.comment.PendingComment,
                                  lambda c: c.delete())

class ApprovedLoader(async.AsyncHandler):
    @models.user.admin_only
    def serve(self):
        return dump_comments(models.comment.fetch(int(self.args['start'])),
                             utils.dumpjson.comment_admin)

class Deleter(async.AsyncHandler):
    @models.user.admin_only
    def serve(self):
        return deal_with_comments(self, models.comment.Comment,
                                  lambda c: c.delete())
