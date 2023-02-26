import markdown
from extensions.altcheckextension import AltCheckExtension
from extensions.titlecheckextension import TitleCheckExtension
from extensions.aria_role_extension import AriaRoleExtension
import logging
logging.basicConfig(level=logging.INFO)
#print(markdown.markdown('foo --deleted-- bar', extensions=[MyExtension()]))

with open('src\sample.md', 'r') as f:
    logging.debug(markdown.markdown(f.read(), extensions=[AltCheckExtension()]))

with open('src\missing_header.md', 'r') as f:
    logging.debug(markdown.markdown(f.read(), extensions=[TitleCheckExtension()]))

with open('src\list_sample.md', 'r') as f:
    logging.debug(markdown.markdown(f.read(), extensions=[AriaRoleExtension()]))

with open('src\\role_sample.md', 'r') as f:
    print(markdown.markdown(f.read(), extensions=[AriaRoleExtension()]))