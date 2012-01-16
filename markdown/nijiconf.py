BR = '<br />'

BOLD_BEGIN = '''<b>'''
BOLD_END = '''</b>'''

ITALIC_BEGIN = '''<i>'''
ITALIC_END = '''</i>'''

MONO_BEGIN = '''<tt><code>'''
MONO_END = '''</code></tt>'''

LINK_BEGIN = '''<a href='%s'>'''
LINK_END = '''</a>'''

SUP_BEGIN = '<sup>'
SUP_END = '</sup>'
SUB_BEGIN = '<sub>'
SUB_END = '</sub>'

IMAGE = '''<img src='%s'/>'''

AND = '&amp;'
SPACE = '&nbsp;'
DOT = '&#46;'
MINUS = '&#45;'
SQUOT = '&#39;'
DQUOT = '&#34;'
LT = '&lt;'
GT = '&gt;'

UL_BEGIN = '<ul>'
UL_END = '</ul>'
OL_BEGIN = '<ol>'
OL_END = '</ol>'
LI_BEGIN = '<li>'
LI_END = '</li>'

H1_BEGIN = '<h1>'
H1_END = '</h1>'
H2_BEGIN = '<h2>'
H2_END = '</h2>'
H3_BEGIN = '<h3>'
H3_END = '</h3>'

MONO_BLOCK_BEGIN = '''<pre><p><tt><code>'''
MONO_BLOCK_END = '''</code></tt></p></pre>'''

AA_BEGIN = '''<tt><code><p style='line-height: 96%; white-space: nowrap;'>'''
AA_END = '''</p></code></tt>'''

TABLE_BEGIN = '''<table border='1'>'''
TABLE_END = '</table>'

ROW_BEGIN = '<tr>'
ROW_END = '</tr>'

CELL_BEGIN = '<td%s>%s'
CELL_END = '</td>'

CELL_COL_SPAN = ' colspan="%s"'
CELL_ROW_SPAN = ' rowspan="%s"'
CELL_HORI_ALGN = ' align="%s"'
CELL_VERT_ALGN = ' valign="%s"'

CELL_HORI_ALIGNMENT_MAP = {
    'l': 'left',
    'r': 'right',
    'j': 'justify',
    'c': 'center',
}

CELL_VERT_ALIGNMENT_MAP = {
    't': 'top',
    'm': 'middle',
    'b': 'bottom',
    'l': 'baseline',
}

CELL_ATTR_MAP = {
    'c': lambda x: CELL_COL_SPAN % x,
    'r': lambda x: CELL_ROW_SPAN % x,
    'h': lambda x: CELL_HORI_ALGN % CELL_HORI_ALIGNMENT_MAP[x],
    'v': lambda x: CELL_VERT_ALGN % CELL_VERT_ALIGNMENT_MAP[x],
}
