from hashlib import sha256
import base
import async
import models.user
import utils.hash
import utils.cookie

def mkuser(name, passwd_origin, is_admin, response):
    if len(name) < 6 or len(passwd_origin) < 6:
        return { 'result': 'fail', 'reason': 'format' }
    if models.user.User.get_by_name(name) != None:
        return { 'result': 'fail', 'reason': 'existed' }
    usr = models.user.User.new(name)
    usr.passwd = utils.hash.passwd(passwd_origin)
    usr.session_key = utils.hash.session_key(usr)
    usr.admin = is_admin
    usr.put()
    utils.cookie.update_cookie(response, usr.session_key)
    return { 'result': 'ok' }

class NewAdmin(async.AsyncHandler):
    def serve(self):
        usr = models.user.User.get_admin()
        if usr is not None:
            return dict(result='fail', reason='admin_existed', name=usr.name)
        return mkuser(self.args['name'], self.args['passwd_origin'], True,
                      self.response)

class RegisterUser(async.AsyncHandler):
    def serve(self):
        return mkuser(self.args['name'], self.args['passwd_origin'], False,
                      self.response)

class UserLogin(async.AsyncHandler):
    def serve(self):
        usr = models.user.User.get_by_name(self.args['name'])
        if usr == None or usr.passwd != utils.hash.passwd(
                                            self.args['passwd_origin']):
            return { 'result': 'fail', 'reason': 'invalid' }
        utils.cookie.update_cookie(self.response, usr.session_key)
        return { 'result': 'ok' }
