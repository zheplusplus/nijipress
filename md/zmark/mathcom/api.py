import parser
from config import config

parse_func = parser.init(config['opmap'])


def parse(s):
    try:
        return parse_func(s)
    except parser.ParseError, e:
        return {'type': 'name',
                'name': '== PARSE ERROR %s (at %d) ==' % (e.token, e.pos)}
