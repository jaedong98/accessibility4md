from markdown.treeprocessors import Treeprocessor
import logging
logging.basicConfig(level=logging.DEBUG)

class MyTreeprocessor(Treeprocessor):
    def run(self, root):
        logging.info('MyTreeprocessor.run()')
        root.text = 'modified content'
        # No return statement is same as `return None`