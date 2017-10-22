import os
import re
import jinja2

from document import DocumentForge
from inline import InlineForge, plain_text, display_title

SECTION_PAT = re.compile(r'^(?P<index>(\d)+)\.(?P<title>(.*))$')
TEMPL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views')

_env = jinja2.Environment(extensions=[
    'jinja2.ext.autoescape', 'jinja2.ext.loopcontrols', 'jinja2.ext.do',
], loader=jinja2.FileSystemLoader(TEMPL_DIR))

def render(filename, **kwargs):
    return _env.get_template(filename).render(**kwargs)

def makeDocForge():
    def render_table(caption, head_rows, body_rows):
        return render('table.html', caption=caption, head_rows=head_rows,
                      body_rows=body_rows)

    df = DocumentForge(render_table, InlineForge())
    df.set_section(0, 0, '')
    return df

def generate_preview(document, size):
    f = makeDocForge()
    return f.compile_partial(document, size)[0]

def forge(document):
    f = makeDocForge()
    body = f.compile_entire(document)
    footnotes = f.render_footnotes()
    return body + footnotes

plain_title = plain_text
