import re
import cgi

import template
import tags
import mathcom.api

ESCAPE_RE = re.compile(r'\\(?P<esc>.)')
BOLD_RE = re.compile(r'\*\*\*(?P<bold>([^\*]|\*[^\*])*)\*\*')
ITALIC_RE = re.compile(r'///(?P<italic>([^/]|/[^/])*)//')
STROKE_RE = re.compile(r'---(?P<s>([^-]|-[^-])*)--')
MONOSPACE_RE = re.compile('```(?P<ms>([^`]|`[^`])*)``')

INLINE_EXPR_RE = re.compile(r'(?<!\\)\$(?P<expr>[^$]+)\$')
ANCHOR_RE = re.compile(r'(?<!\\)#(?P<a>([^#]+))#')
LINK_RE = re.compile(r'\[link (?P<uri>[^ \|\]]+)(?:\|(?P<text>[^\]]*))?]')
PAGE_RE = re.compile(r'\[p (?P<uri>[^ \|\]]+)(?:\|(?P<text>[^\]]*))?]')
IMG_RE = re.compile(r'\[img ([^]]*)]')
USER_RE = re.compile(r'@(?P<username>[A-Za-z]\w*)(?!\.\w)')


def forge(text):
    def render_page_title(uri, text):
        import models.page
        page = models.page.get_by_full_uri(uri)
        if page is None:
            return '-- PAGE IS MISSING --'
        return template.render(
            'markdown/page_link.html', uri=page['uri'],
            text=''.join(forge(text or page['title'])))

    def page(text):
        G = PAGE_RE.groups + 1
        split = PAGE_RE.split(text)
        result = link(split[0])
        for i in range(len(split) / G):
            result.append(render_page_title(
                split[i * G + 1], split[i * G + 2]))
            result.extend(link(split[i * G + G]))
        return result

    def render_link(uri, text):
        return template.render('markdown/link.html', uri=uri,
                               text=''.join(forge(text)) if text else uri)

    def link(text):
        G = LINK_RE.groups + 1
        split = LINK_RE.split(text)
        result = img(split[0])
        for i in range(len(split) / G):
            result.append(render_link(split[i * G + 1], split[i * G + 2]))
            result.extend(img(split[i * G + G]))
        return result

    def img(text):
        G = IMG_RE.groups + 1
        split = IMG_RE.split(text)
        result = inline_expr(split[0])
        for i in range(len(split) / G):
            result.extend(inline_expr(split[i * G + G]))
        return result

    def inline_expr(text):
        G = INLINE_EXPR_RE.groups + 1
        split = INLINE_EXPR_RE.split(text)
        result = [_convert_html_tags(split[0])]
        for i in range(len(split) / G):
            result.append(template.f_render_mathcom(
                mathcom.api.parse(split[i * G + 1])))
            result.append(_convert_html_tags(split[i * G + G]))
        return result

    return ''.join(page(text))


def esc_back_slash(text):
    return ESCAPE_RE.sub(lambda m: m.group('esc'), text)


def _convert_html_tags(text):
    def bold(text):
        return BOLD_RE.sub(lambda m: tags.BOLD % m.group('bold'), text)

    def italic(text):
        return ITALIC_RE.sub(lambda m: tags.ITALIC % m.group('italic'), text)

    def stroke(text):
        return STROKE_RE.sub(lambda m: tags.STROKE % m.group('s'), text)

    def anchor(text):
        return ANCHOR_RE.sub(
            lambda m: tags.ANCHOR % (template.f_encode_anchor(m.group('a')),
                                     m.group('a')),
            text)

    def monospace(text):
        return MONOSPACE_RE.sub(lambda m: tags.MONOSPACE % m.group('ms'), text)

    def user_ref(text):
        def render_user(username):
            import models.user
            u = models.user.get_by_username(username)
            if u is None:
                return '@' + username
            return template.f_render_user(u, 'markdown')
        return USER_RE.sub(lambda m: render_user(m.group('username')), text)

    return esc_back_slash(monospace(anchor(stroke(italic(bold(
        cgi.escape(text, quote=True)))))))
