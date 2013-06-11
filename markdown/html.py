import re
import nijiconf

ESC_DICT = {
        '&': nijiconf.AND,
        '<': nijiconf.LT,
        '>': nijiconf.GT,
        '"': nijiconf.DQUOT,
        "'": nijiconf.SQUOT
    }

def escape(text):
    return ''.join([ ESC_DICT.get(ch, ch) for ch in text ])

_LEADING_SP_RE = re.compile('^[ ]+')
_TRIPLE_MIN_RE = re.compile('---')

def leading_spaces(text):
    return _LEADING_SP_RE.sub(lambda m: len(m.group(0)) * nijiconf.SPACE, text)

def tripple_minus(text):
    return _TRIPLE_MIN_RE.sub(lambda m: nijiconf.MINUS * 3, text)

def forge(text):
    return tripple_minus(leading_spaces(escape(text)))
