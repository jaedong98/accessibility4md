from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import tables
from element_visitor import ElememntVisitor
import logging

class TableRoleSetter(ElememntVisitor):

    def visit_table(self, element):
        element.set('role', 'table')
        element.set('aria-rowcount', str(len(element)))
    
class TableRowIndexer(ElememntVisitor):

    #def visit_table(self, element):
    #    element.set('role', 'table')
    #    element.set('aria-rowcount', str(len(element)))
    
    def visit_thead(self, element):
        element.set('role', 'rowgroup')
        for row in element:
            self.visit(row)
    
    def visit_tbody(self, element):
        element.set('role', 'rowgroup')
        for i, row in enumerate(element, start=1):
            self.visit(row)
    
    def visit_tr(self, element):
        element.set('role', 'row')
        #element.set('aria-rowindex', str(index))
        for td in element:
            self.visit(td)
    
    def visit_td(self, element):
        element.set('role', 'cell')
        
    def visit_th(self, element):
        element.set('role', 'columnheader')


class AriaTableRoleProcessor(tables.TableProcessor):

    def run(self, parent, blocks):
        super().run(parent, blocks)
        TableRoleSetter().visit(parent)
        #print(parent.text)

class AriaTableIndexProcessor(Treeprocessor):

    def run(self, root):
        TableRowIndexer().visit(root)
        #print(parent.text)


class AriaTableExtension(Extension):
    """ Add tables to Markdown. """

    def __init__(self, **kwargs):
        self.config = {
            'use_align_attribute': [False, 'True to use align attribute instead of style.'],
        }

        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        """ Add an instance of TableProcessor to BlockParser. """
        if '|' not in md.ESCAPED_CHARS:
            md.ESCAPED_CHARS.append('|')
        processor = AriaTableRoleProcessor(md.parser, self.getConfigs())
        md.parser.blockprocessors.register(processor, 'areatableroleprocessor', 75)

class AriaTableIndexExtension(Extension):
    """ Add tables to Markdown. """

    def __init__(self, **kwargs):
        self.config = {
            'use_align_attribute': [False, 'True to use align attribute instead of style.'],
        }

        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        """ Add an instance of TableProcessor. """
        if '|' not in md.ESCAPED_CHARS:
            md.ESCAPED_CHARS.append('|')
        processor = AriaTableIndexProcessor()
        md.treeprocessors.register(processor, 'areatableindexprocessor', 75)


def makeExtension(**kwargs):  # pragma: no cover
    return AriaTableIndexExtension(**kwargs)