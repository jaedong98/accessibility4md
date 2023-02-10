import markdown
from myextension import MyExtension
print(markdown.markdown('foo bar', extensions=[MyExtension()]))

#html = markdown.markdown("# Hello World!\n NO RENDER", extensions=[NoRender()])
#print(html)