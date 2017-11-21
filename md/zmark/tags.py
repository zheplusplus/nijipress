# encoding=utf-8

AND = '&amp;'
SPACE = '&nbsp;'
SQUOT = '&#39;'
DQUOT = '&#34;'
LT = '&lt;'
GT = '&gt;'

PARA_BEGIN = '''<section class='sec'>'''
PARA_END = '''</section>'''
PLINE_BEGIN = '''<p class='nt-p'>'''
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
ANCHOR = '''<a href='#%s' class='anchor'>%s</a>'''
MONOSPACE = '''<code class='codei'>%s</code>'''

HEADING = u'''<h{lvl} id='{anchor}' class='h{lvl} hx'>{text}</h{lvl}>'''

CODE_BLOCK_CAPTION = (u'''<div class='nt-code-snippet-caption'>代码清单 '''
                      '''{section}-{index}</div><hr>''')
CODE_BLOCK_BEGIN = ('''<div class='codeb'>'''
                    '''<code class='prettyprint lang-%s'>''')
CODE_BLOCK_BEGIN_MONOCHR = '''<div class='codeb'><code>'''
CODE_BLOCK_END = '</code></div>'

AA_BEGIN = '''<div class='aa'><pre><code>'''
AA_END = '</code></pre></div>'
