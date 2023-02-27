from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from element_visitor import ElememntVisitor
import re
import logging

SUPORTED_ROLES = set("article banner complementary contentinfo definition document feed figure form main navigation region search section table".split())
ROLE_PATTERN = "==(.*?)=="
class RoleSetter(ElememntVisitor):

    def visit_h1(self, element, *args, **kwargs):
        g = re.search(ROLE_PATTERN, element.text)
        if g:
            role = g.group(1)
            if role not in SUPORTED_ROLES:
                return
            logging.debug("Setting role to %s" % g.group(1))
            element.set('role', g.group(1))
            element.text = re.sub(ROLE_PATTERN, '', element.text.strip())


class AriaAppendingProcessor(Treeprocessor):
    def run(self, root):
        RoleSetter().visit(root)


class AriaRoleExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(AriaAppendingProcessor(md), 'ariaappendingprocessor', 1)

