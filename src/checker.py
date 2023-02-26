import markdown
from extensions.altcheckextension import AltCheckExtension
import logging
logging.basicConfig(level=logging.INFO)
#print(markdown.markdown('foo --deleted-- bar', extensions=[MyExtension()]))

with open('src\sample.md', 'r') as f:
    logging.debug(markdown.markdown(f.read(), extensions=[AltCheckExtension()]))