import re

def escape(text):
    from nijiconf import AND, LT, GT, SQUOT, DQUOT
    escape_dict = {'&' : AND , '<' : LT, '>' : GT, '"' : DQUOT, "'" : SQUOT}
    return re.sub('''&|<|>|[']|["]''', lambda m: escape_dict[m.group(0)], text)

def leading_spaces(text):
    from nijiconf import SPACE
    return re.sub('^[ ]+', lambda m: len(m.group(0)) * SPACE, text)

def tripple_minus(text):
    from nijiconf import MINUS
    return re.sub('---', lambda m: MINUS * 3, text)

def forge(text):
    return tripple_minus(leading_spaces(escape(text)))
