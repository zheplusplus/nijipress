import time
from hashlib import sha256

def passwd(p):
    return sha256(p).hexdigest()

def session_key(user):
    return sha256(user.name + user.passwd + str(time.time())).hexdigest()

def comment_token(email):
    return sha256(email + str(time.time())).hexdigest()
