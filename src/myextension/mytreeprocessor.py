from markdown.treeprocessors import Treeprocessor

class MyTreeprocessor(Treeprocessor):
    def run(self, root):
        root.text = 'modified content'
        # No return statement is same as `return None`