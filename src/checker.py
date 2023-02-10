import markdown
from myextension import MyExtension
print(markdown.markdown('foo --deleted-- bar', extensions=[MyExtension()]))

#html = markdown.markdown("# Hello World!", extensions=[MyExtension()])
#print(html)