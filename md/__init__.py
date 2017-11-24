import nijitext.entire_doc
import zmark.render

class MarkdownConvert(object):
    def __init__(self, head_title, display_title, content, preview):
        """
        head_title: escape the title for the <head><title> tag
        content: escape the title and the content which will be shown in the page
        preview: text preview
        """
        self.head_title = head_title
        self.display_title = display_title
        self.content = content
        self.preview = preview

    def process_multilines(self, content):
        return ''.join(self.content(content))

    def generate_preview(self, content):
        return ''.join(self.preview(content, 1729))

    def process_post(self, post):
        post.title = self.display_title(post.title)
        content = post.content
        post.content = self.process_multilines(content)
        post.preview = self.generate_preview(content)
        return post

__nijitext = MarkdownConvert(
    nijitext.entire_doc.plain_title,
    nijitext.entire_doc.display_title,
    nijitext.entire_doc.forge,
    nijitext.entire_doc.generate_preview,
)

__zmark = MarkdownConvert(
    zmark.render.plain_title,
    zmark.render.display_title,
    zmark.render.forge,
    zmark.render.generate_preview,
)

__markmap = {
    # Since v1.1.0
    None: __nijitext,
    'nijitext': __nijitext,
    'zmark': __zmark,
}

def get(t):
    return __markmap[t]

def process(text, markdown):
    m = get(markdown)
    return ''.join(m.content(text))
