import re

_MONOSPACE_RE = '``(?P<monospace>([^`]|`[^`])*)``'
_BOLD_RE = '\*\*(?P<bold>([^\*]|\*[^\*])*)\*\*'
_ITALIC_RE = '///(?P<italic>([^/]|/[^/]|//[^/])*)///'
_ESCAPE_RE = '\\\\(?P<esc>[-`*/,:;=|@#$%&\\^\\[\\]\\{\\}\\(\\)\\\\])'

def esc_back_slash(text):
    return re.sub(_ESCAPE_RE, lambda m: m.group('esc'), text)

def plain(text):
    def monospace(text):
        return re.sub(_MONOSPACE_RE, lambda m: m.group('monospace'), text)

    def bold(text):
        return re.sub(_BOLD_RE, lambda m: m.group('bold'), text)

    def italic(text):
        return re.sub(_ITALIC_RE, lambda m: m.group('italic'), text)

    return esc_back_slash(italic(bold(monospace(text))))

def forge(text):
    def monospace(text):
        from nijiconf import MONO_BEGIN, MONO_END
        return re.sub(_MONOSPACE_RE
                    , lambda m: MONO_BEGIN + m.group('monospace') + MONO_END
                    , text)

    def bold(text):
        from nijiconf import BOLD_BEGIN, BOLD_END
        return re.sub(_BOLD_RE
                    , lambda m: BOLD_BEGIN + m.group('bold') + BOLD_END
                    , text)

    def italic(text):
        from nijiconf import ITALIC_BEGIN, ITALIC_END
        return re.sub(_ITALIC_RE
                    , lambda m: ITALIC_BEGIN + m.group('italic') + ITALIC_END
                    , text)

    def stroke(text):
        from nijiconf import STROKE_BEGIN, STROKE_END
        return re.sub('--(?P<s>([^-]|-[^-])*)--'
                    , lambda m: STROKE_BEGIN + m.group('s') + STROKE_END
                    , text)

    def link(text):
        from nijiconf import LINK_BEGIN, LINK_END
        return re.sub('@@(?P<url>([^@ ]+))@(?P<text>(([^@]|@[^@])+))@@'
                    , lambda m: (LINK_BEGIN % m.group('url')) + m.group('text')
                               + LINK_END
                    , text)

    def sup(text):
        from nijiconf import SUP_BEGIN, SUP_END
        return re.sub('\^\^(?P<sup>([^\^]|\^[^\^])*)\^\^'
                    , lambda m: SUP_BEGIN + m.group('sup') + SUP_END
                    , text)

    def sub(text):
        from nijiconf import SUB_BEGIN, SUB_END
        return re.sub(',,(?P<sub>([^,]|,[^,])*),,'
                    , lambda m: SUB_BEGIN + m.group('sub') + SUB_END
                    , text)

    def img(text):
        from nijiconf import IMAGE
        return re.sub('\[\[img (?P<img>([^\]]|,[^\]])*)]]'
                    , lambda m: IMAGE % m.group('img').strip()
                    , text)

    return esc_back_slash(
            img(sub(sup(link(stroke(italic(bold(monospace(text)))))))))
