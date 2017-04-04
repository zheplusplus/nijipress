import re

_MONOSPACE_RE = re.compile('``(?P<monospace>([^`]|`[^`])*)``')
_BOLD_RE = re.compile(r'\*\*(?P<bold>([^\*]|\*[^\*])*)\*\*')
_ITALIC_RE = re.compile('///(?P<italic>([^/]|/[^/]|//[^/])*)///')
_ESCAPE_RE = re.compile(r'\\(?P<esc>[-`*/,:;=|@#$%&^\[\]\{\}\(\)\\])')
_STROKE_RE = re.compile('--(?P<s>([^-]|-[^-])*)--')
_LINK_RE = re.compile('@@(?P<url>([^@ ]+))@(?P<text>(([^@]|@[^@])+))@@')
_SUPER_RE = re.compile(r'\^\^(?P<sup>([^\^]|\^[^\^])*)\^\^')
_SUB_RE = re.compile(',,(?P<sub>([^,]|,[^,])*),,')
_IMG_RE = re.compile('\[\[img (?P<img>([^\]]|,[^\]])*)]]')

def esc_back_slash(text):
    return _ESCAPE_RE.sub(lambda m: m.group('esc'), text)

def plain(text):
    def monospace(text):
        return _MONOSPACE_RE.sub(lambda m: m.group('monospace'), text)

    def bold(text):
        return _BOLD_RE.sub(lambda m: m.group('bold'), text)

    def italic(text):
        return _ITALIC_RE.sub(lambda m: m.group('italic'), text)

    return esc_back_slash(italic(bold(monospace(text))))

def forge(text):
    def monospace(text):
        from nijiconf import MONO_BEGIN, MONO_END
        return _MONOSPACE_RE.sub(
                lambda m: MONO_BEGIN + m.group('monospace') + MONO_END, text)

    def bold(text):
        from nijiconf import BOLD_BEGIN, BOLD_END
        return _BOLD_RE.sub(lambda m: BOLD_BEGIN + m.group('bold') + BOLD_END,
                            text)

    def italic(text):
        from nijiconf import ITALIC_BEGIN, ITALIC_END
        return _ITALIC_RE.sub(
                lambda m: ITALIC_BEGIN + m.group('italic') + ITALIC_END, text)

    def stroke(text):
        from nijiconf import STROKE_BEGIN, STROKE_END
        return _STROKE_RE.sub(
                lambda m: STROKE_BEGIN + m.group('s') + STROKE_END, text)

    def link(text):
        from nijiconf import LINK_BEGIN, LINK_END
        return _LINK_RE.sub(
                lambda m: (LINK_BEGIN % m.group('url')
                                ) + m.group('text') + LINK_END , text)

    def sup(text):
        from nijiconf import SUP_BEGIN, SUP_END
        return _SUPER_RE.sub(lambda m: SUP_BEGIN + m.group('sup') + SUP_END,
                             text)

    def sub(text):
        from nijiconf import SUB_BEGIN, SUB_END
        return _SUB_RE.sub(lambda m: SUB_BEGIN + m.group('sub') + SUB_END,
                           text)

    def img(text):
        from nijiconf import IMAGE
        return _IMG_RE.sub(lambda m: IMAGE % m.group('img').strip(), text)

    return esc_back_slash(
            img(sub(sup(link(stroke(italic(bold(monospace(text)))))))))
