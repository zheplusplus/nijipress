AND = '&amp;'
SPACE = '&nbsp;'
SQUOT = '&#39;'
DQUOT = '&#34;'
LT = '&lt;'
GT = '&gt;'

PARA_BEGIN = '''<div class='zl-p'>'''
PARA_END = '''</div>'''
PLINE_BEGIN = '''<p class='zl-ln'>'''
PLINE_END = '''</p>'''
BR = '<br>'

UL_BEGIN = '''<ul>'''
UL_END = '</ul>'
OL_BEGIN = '''<ol>'''
OL_END = '</ol>'
LI_BEGIN = '''<li>'''
LI_END = '</li>'

BOLD = '''<b>%s</b>'''
ITALIC = '''<i>%s</i>'''
STROKE = '''<del>%s</del>'''
ANCHOR = '''<a href='#%s' class='zl-anchor'>%s</a>'''
MONOSPACE = '''<code class='zl-codei'>%s</code>'''

HEADING = u'''<h{lvl} id='{anchor}' class='zl-h{lvl}'>{text}</h{lvl}>'''
EXPRESSION = '''<div class='zl-expr'><div class='zl-expr-text'>%s</div>
<div class='zl-expr-data'>%s</div></div>'''

CODE_BLOCK_BEGIN = ('''<div class='zl-codeb'>'''
                    '''<code class='prettyprint lang-%s'>''')
CODE_BLOCK_BEGIN_MONOCHR = '''<div class='zl-codeb'><code>'''
CODE_BLOCK_END = '</code></div>'

AA_BEGIN = '''<div class='zl-aa'><code>'''
AA_END = '</code></div>'
