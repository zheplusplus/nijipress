import re

def escape(text):
    from nijiconf import AND, LT, GT, SQUOT, DQUOT
    escape_dict = {'&' : AND , '<' : LT, '>' : GT, '"' : DQUOT, "'" : SQUOT}
    return re.sub('''&|<|>|[']|["]''', lambda m: escape_dict[m.group(0)], text)

def leading_spaces(text):
    from nijiconf import SPACE
    return re.sub('^[ ]+', lambda m: len(m.group(0)) * SPACE, text)

def triple_dots(text):
    from nijiconf import DOT
    return re.sub('\.\.\.', lambda m: DOT * 3, text)

def tripple_minus(text):
    from nijiconf import MINUS
    return re.sub('---', lambda m: MINUS * 3, text)

def forge(text):
    return tripple_minus(triple_dots(leading_spaces(escape(text))))
