import re
import cgi

import tags
from md import html_tags

ESCAPE_RE = re.compile(r'\\(?P<esc>.)')
BOLD_RE = re.compile(r'(?<!\\)\*\*(?! )(?P<bold>([^*]|\\[*])+)(?<![\\| ])\*\*')
ITALIC_RE = re.compile(r'(?<!\\)/(?! )(?P<italic>([^/]|\\[/])+)(?<![\\| ])/'
                       r'(?![\\a-zA-Z0-9:/])')
STROKE_RE = re.compile(r'(?<!\\)~(?! )(?P<s>([^~]|\\[~])+)(?<![\\| ])~')
MONOSPACE_RE = re.compile(r'(?<!\\)`(?! )(?P<ms>([^`]|\\[`])+)(?<![\\| ])`')

INLINE_EXPR_RE = re.compile(r'(?<!\\)\$(?P<expr>[^$]+)\$')
ANCHOR_RE = re.compile(r'(?<!\\)#(?P<a>([^#]+))#')
LINK_RE = re.compile(r'\[link (?P<uri>[^ \|\]]+)(?:\|(?P<text>[^\]]*))?]')
PAGE_RE = re.compile(r'\[p (?P<uri>[^ \|\]]+)(?:\|(?P<text>[^\]]*))?]')
IMG_RE = re.compile(r'\[img (?P<uri>[^ \|\]]+)[ ]?(?P<opt>[^ \|\]]+)?]')

EXTERNAL_LINK_PROTOCOL_RE = re.compile('^[a-z]+://')


class InlineForge(object):
    def __init__(self):
        pass

    def render_page(self, page, text):
        return self.render_link('/?p=' + page, text)

    def render_link(self, uri, text):
        return ([html_tags.LINK_BEGIN % uri] + self.img(text) +
                [html_tags.LINK_END])

    def render_img(self, uri, opt):
        return ['[IMAGE NOT SUPPORT]']

    def page(self, text):
        G = PAGE_RE.groups + 1
        split = PAGE_RE.split(text)
        result = self.link(split[0])
        for i in range(len(split) / G):
            result.extend(self.render_page(split[i * G + 1], split[i * G + 2]))
            result.extend(self.link(split[i * G + G]))
        return result

    def link(self, text):
        G = LINK_RE.groups + 1
        split = LINK_RE.split(text)
        result = self.img(split[0])
        for i in range(len(split) / G):
            uri = split[i * G + 1]
            text = split[i * G + 2]
            if not EXTERNAL_LINK_PROTOCOL_RE.match(uri):
                uri = 'http://' + uri
            result.extend(self.render_link(uri, text))
            result.extend(self.img(split[i * G + G]))
        return result

    def img(self, text):
        G = IMG_RE.groups + 1
        split = IMG_RE.split(text)
        result = self.convert_html_tags(split[0])
        for i in range(len(split) / G):
            result.extend(self.render_img(split[i * G + 1], split[i * G + 2]))
            result.extend(self.convert_html_tags(split[i * G + G]))
        return result

    def convert_html_tags(self, text):
        def esc_back_slash(text):
            return ESCAPE_RE.sub(lambda m: m.group('esc'), text)

        def bold(text):
            return BOLD_RE.sub(lambda m: tags.BOLD % m.group('bold'), text)

        def italic(text):
            return ITALIC_RE.sub(lambda m: tags.ITALIC % m.group('italic'),
                                 text)

        def stroke(text):
            return STROKE_RE.sub(lambda m: tags.STROKE % m.group('s'), text)

        def monospace(text):
            return MONOSPACE_RE.sub(lambda m: tags.MONOSPACE % m.group('ms'),
                                    text)

        return [esc_back_slash(monospace(stroke(bold(italic(
            cgi.escape(text, quote=True))))))]

    def forge(self, text, ctx):
        return ''.join(self.page(text))

def plain_text(text):
    def esc_back_slash(text):
        return ESCAPE_RE.sub(lambda m: m.group('esc'), text)

    def bold(text):
        return BOLD_RE.sub(lambda m: m.group('bold'), text)

    def italic(text):
        return ITALIC_RE.sub(lambda m: m.group('italic'), text)

    def monospace(text):
        return MONOSPACE_RE.sub(lambda m: m.group('ms'), text)

    return esc_back_slash(monospace(bold(italic(cgi.escape(text, quote=True)))))

def display_title(text):
    def esc_back_slash(text):
        return ESCAPE_RE.sub(lambda m: m.group('esc'), text)

    def bold(text):
        return BOLD_RE.sub(lambda m: tags.BOLD % m.group('bold'), text)

    def italic(text):
        return ITALIC_RE.sub(lambda m: tags.ITALIC % m.group('italic'), text)

    def monospace(text):
        return MONOSPACE_RE.sub(lambda m: tags.MONOSPACE % m.group('ms'), text)

    return esc_back_slash(monospace(bold(italic(cgi.escape(text, quote=True)))))
