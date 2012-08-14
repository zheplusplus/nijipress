from hashlib import sha256
import base
import models.user
import utils.cookie

class UserView(base.BaseView):
    def usr_page(self, title, handler='', hint=''):
        self.put_page('templates/usr.html', {
                'title': title,
                'handler': handler,
                'hint': hint,
            })

class LoginPage(UserView):
    def get(self):
        self.usr_page('Login', 'auth')

class LoginAction(UserView):
    def post(self):
        usr = models.user.User.get_by_name(self.request.get('name'))
        if usr.passwd != sha256(self.request.get('passwd_origin')).hexdigest():
            self.usr_page('Login', 'auth', 'Authentication failed')
            return
        utils.cookie.update_cookie(self.response, usr.session_key)
        self.redirect('/')
