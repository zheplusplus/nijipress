from Cookie import BaseCookie

def update_cookie(response, session_key):
    cookie = BaseCookie()
    cookie['skey'] = session_key
    cookie['skey']['path'] = '/'
    cookie['skey']['max-age'] = 17299119
    response.headers.add('Set-Cookie', cookie['skey'].output(header='').strip())
