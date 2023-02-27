from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern
from extensions.element_visitor import ElementVisitor
import logging


class AltMissingFinder(ElementVisitor):

    def visit_img(self, element, *args, **kwargs):
        if element.get('alt') is None:
            logging.info("[WCAG 2.1 - 1.1.1 Non-text Content] Found an image with no alt text for %s" % element.get('src'))
            element.set('alt', 'No alt text provided')
        elif element.get('alt') == '':
            logging.info("[WCAG 2.1 - 1.1.1 Non-text Content] Found an image with empty alt text for %s" % element.get('src'))
            element.set('alt', 'No alt text provided')   

   
class AltNearbyVisitor(ElementVisitor):

    def visit_p(self, element, *args, **kwargs):
        alt_texts = set()
        for child in element:
            if child.tag == 'img':
                if 'alt' in child.attrib:
                    if child.get('alt') in alt_texts:
                        logging.info("[WCAG 2.1 - 1.1.1 Non-text Content] Found an image with duplicate alt text(%s) for %s" % (child.get('alt'), child.get('src')))
                    else:
                        alt_texts.add(child.get('alt'))


class AltCheckProcessor(Treeprocessor):
    def run(self, root):
        AltMissingFinder().visit(root)
        AltNearbyVisitor().visit(root)


DEL_RE = r'(--)(.*?)--'
class AltCheckExtension(Extension):
    def extendMarkdown(self, md):
        
        md.treeprocessors.register(AltCheckProcessor(md), 'altcheckprocessor', 1)
        # Create the del pattern
        del_tag = SimpleTagPattern(DEL_RE, 'del')
        # Insert del pattern into markdown parser
        md.inlinePatterns.register(del_tag, 'del', 75)

