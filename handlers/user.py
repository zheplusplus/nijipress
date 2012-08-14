from hashlib import sha256
from Cookie import BaseCookie

import base
import models.admin

class UserView(base.BaseView):
    def usr_page(self, title, handler='', hint=''):
        self.put_page('templates/usr.html', {
                'title': title,
                'handler': handler,
                'hint': hint,
            })

class Register(UserView):
    def get(self):
        self.usr_page('Register', 'newusr')

class New(UserView):
    def post(self):
        usr = models.admin.User.get_by_name(self.request.get('name'))
        if usr.passwd and len(usr.passwd) > 0:
            self.usr_page('Register', 'newusr',
                          'User ' + usr.name + ' already exists')
            return
        usr.passwd = sha256(self.request.get('passwd_origin')).hexdigest()
        usr.session_key = sha256(usr.name + usr.passwd).hexdigest()
        usr.put()
        self.redirect('/')
        update_cookie(self.response, usr.session_key)

class LoginPage(UserView):
    def get(self):
        self.usr_page('Login', 'auth')

class LoginAction(UserView):
    def post(self):
        usr = models.admin.User.get_by_name(self.request.get('name'))
        if usr.passwd != sha256(self.request.get('passwd_origin')).hexdigest():
            self.usr_page('Login', 'auth', 'Authentication failed')
            return
        update_cookie(self.response, usr.session_key)
        self.redirect('/')

def update_cookie(response, session_key):
    cookie = BaseCookie()
    cookie['skey'] = session_key
    cookie['skey']['path'] = '/'
    cookie['skey']['max-age'] = 17299119
    response.headers.add('Set-Cookie', cookie['skey'].output(header='').strip())
