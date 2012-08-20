import json
import base
import models.tag
import models.post
import utils.dumpjson
import utils.escape
import utils.cookie
import utils.hash

class AsyncHandler(base.BaseView):
    def post(self):
        self.args = json.loads(self.request.body)
        self.response.out.write(json.dumps(self.serve()))

class Tags(AsyncHandler):
    def serve(self):
        return models.tag.sort_by_count()

class RecentPosts(AsyncHandler):
    def serve(self):
        return [ utils.dumpjson.post_title(p) for p in
                utils.escape.client_posts(models.post.fetch(0, 6)) ]

class LoadPostById(AsyncHandler):
    def serve(self):
        return utils.dumpjson.post_full(utils.escape.client_post(
            models.post.by_id(self.args['id'])))

class RegisterUser(AsyncHandler):
    def serve(self):
        name = self.args['name']
        passwd_origin = self.args['passwd_origin']
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
        usr = models.user.User.get_by_name(self.args['name'])
        if usr == None or usr.passwd != utils.hash.passwd(
                                            self.args['passwd_origin']):
            return { 'result': 'fail', 'reason': 'invalid' }
        utils.cookie.update_cookie(self.response, usr.session_key)
        return { 'result': 'ok' }
