import base
import async
import models.user
import utils.hash
import utils.cookie

class UserView(base.BaseView):
    def usr_page(self, title, handler='', hint=''):
        self.put_page('usr.html', {
            'title': title,
            'handler': handler,
            'hint': hint,
        })

class Init(UserView):
    def get(self):
        self.usr_page('Init (Set Admin\'s username and password.)', 'newadmin')

class NewAdmin(UserView):
    def post(self):
        usr = model.User.get_admin()
        if usr is not None:
            return self.redirect('/c/error?msg=' + "Admin exist as User: " + str(usr.name)+ " You can reset password by GAE's Admin Console.")
        usr = model.User.get_by_name(self.request.get('name'))
        usr.passwd = sha256(self.request.get('passwd_origin')).hexdigest()
        usr.session_key = sha256(usr.name + usr.passwd).hexdigest()
        usr.admin = True
        usr.put()
        self.redirect('/c/login')
        update_cookie(self.response, usr.session_key)

class Error(UserView):
    def get(self):
        msg = ""
        if 'msg' in self.request.arguments():
            msg = self.request.get("msg")
        self.put_page('templates/error.html', locals())

class RegisterUser(async.AsyncHandler):
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

class UserLogin(async.AsyncHandler):
    def serve(self):
        usr = models.user.User.get_by_name(self.args['name'])
        if usr == None or usr.passwd != utils.hash.passwd(
                                            self.args['passwd_origin']):
            return { 'result': 'fail', 'reason': 'invalid' }
        utils.cookie.update_cookie(self.response, usr.session_key)
        return { 'result': 'ok' }
