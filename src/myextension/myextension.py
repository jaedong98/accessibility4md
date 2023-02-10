from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern
from mytreeprocessor import MyTreeprocessor

DEL_RE = r'(--)(.*?)--'
    
class MyExtension(Extension):
    def extendMarkdown(self, md):
        
        md.treeprocessors.register(MyTreeprocessor(md), 'mytreeprocessor', 1)
        # Create the del pattern
        del_tag = SimpleTagPattern(DEL_RE, 'del')
        # Insert del pattern into markdown parser
        md.inlinePatterns.register(del_tag, 'del', 75)

        