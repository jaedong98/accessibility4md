from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern
from element_visitor import ElememntVisitor
import logging



class TitleCheckProcessor(Treeprocessor):
    def run(self, root):
        if root.text == '\n':
            logging.info("[WCAG 2.1 - 2.4.2 Page Titled] No title found")


class TitleCheckExtension(Extension):
    def extendMarkdown(self, md):
        
        md.treeprocessors.register(TitleCheckProcessor(md), 'titlecheckprocessor', 1)

