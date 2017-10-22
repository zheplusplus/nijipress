import cgi
import re

SPACE = '&nbsp;'
MINUS = '&#45;'

_LEADING_SP_RE = re.compile('^[ ]+')
_TRIPLE_MIN_RE = re.compile('---')

def leading_spaces(text):
    return _LEADING_SP_RE.sub(lambda m: len(m.group(0)) * SPACE, text)

def tripple_minus(text):
    return _TRIPLE_MIN_RE.sub(lambda m: MINUS * 3, text)

def escape(text):
    return tripple_minus(leading_spaces(cgi.escape(text, quote=True)))
