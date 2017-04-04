from Cookie import BaseCookie

import async
import base
import models.user
import utils.hash

def update_cookie(response, session_key):
    cookie = BaseCookie()
    cookie['skey'] = session_key
    cookie['skey']['path'] = '/'
    cookie['skey']['max-age'] = 17299119
    response.headers.add('Set-Cookie', cookie['skey'].output(header='').strip())

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
    update_cookie(response, usr.session_key)
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
        update_cookie(self.response, usr.session_key)
        return { 'result': 'ok' }

base.page_render('/c/reg', 'register.html')
base.page_render('/c/login', 'login.html')
base.page_render('/c/init', 'init_admin.html')
