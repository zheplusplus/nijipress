# -*- coding: utf-8 -*-
from hashlib import sha256
from Cookie import BaseCookie

import base
from admin import model


class UserView(base.BaseView):
    def usr_page(self, title, handler='', hint=''):
        self.put_page('templates/usr.html', {
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
            self.redirect('/c/error?msg=' + "Admin exist as User: " + str(usr.name)+ " You can reset password by GAE's Admin Console.")
            return
        else:
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


class Register(UserView):
    def get(self):
        self.usr_page('Register', 'newusr')


class New(UserView):
    def post(self):
        usr = model.User.get_by_name(self.request.get('name'))
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
        usr = model.User.get_by_name(self.request.get('name'))
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
