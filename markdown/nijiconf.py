AND = '&amp;'
SPACE = '&nbsp;'
MINUS = '&#45;'
SQUOT = '&#39;'
DQUOT = '&#34;'
LT = '&lt;'
GT = '&gt;'

BR = '<br/>'

BOLD_BEGIN = '''<strong class='ntstrong'>'''
BOLD_END = '''</strong>'''

ITALIC_BEGIN = '''<i class='ntitalic'>'''
ITALIC_END = '''</i>'''

STROKE_BEGIN = '''<s class='ntstroke'>'''
STROKE_END = '''</s>'''

MONO_BEGIN = '''<tt><code class='ntinlinecode'>'''
MONO_END = '''</code></tt>'''

LINK_BEGIN = '''<a href='%s' class='ntlink'>'''
LINK_END = '''</a>'''

SUP_BEGIN = '''<sup class='ntsup'>'''
SUP_END = '''</sup>'''
SUB_BEGIN = '''<sub class='ntsub'>'''
SUB_END = '''</sub>'''

IMAGE = '''<img src='%s' class='ntimg'/>'''

UL_BEGIN = '''<ul class='ntul'>'''
UL_END = '</ul>'
OL_BEGIN = '''<ol class='ntol'>'''
OL_END = '</ol>'
LI_BEGIN = '''<li class='ntli'>'''
LI_END = '</li>'

H1_BEGIN = '''<h1 class='nth1'>'''
H1_END = '</h1>'
H2_BEGIN = '''<h2 class='nth2'>'''
H2_END = '</h2>'
H3_BEGIN = '''<h3 class='nth3'>'''
H3_END = '</h3>'

MONO_BLOCK_BEGIN = '''<p class='ntblockcode'><tt><code>'''
MONO_BLOCK_END = '</code></tt></p>'

AA_BEGIN = '''<p class='ntaa'><tt><code>'''
AA_END = '</code></tt></p>'

TABLE_BEGIN = '''<table class='nttable'>'''
TABLE_END = '</table>'

ROW_BEGIN = '''<tr class='nttr'>'''
ROW_END = '</tr>'

CELL_BEGIN = '''<td%s class='nttd'>%s'''
CELL_END = '</td>'

CELL_COL_SPAN = ''' colspan='%s' '''
CELL_ROW_SPAN = ''' rowspan='%s' '''
CELL_HORI_ALGN = ''' align='%s' '''
CELL_VERT_ALGN = ''' valign='%s' '''

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
