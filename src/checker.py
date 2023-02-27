import markdown
from extensions.altcheckextension import AltCheckExtension
from extensions.titlecheckextension import TitleCheckExtension
from extensions.aria_role_extension import AriaRoleExtension
from extensions.aria_table_extension import AriaTableExtension, AriaTableIndexExtension
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO)
#print(markdown.markdown('foo --deleted-- bar', extensions=[MyExtension()]))

SRC_FOLDER = Path("src")

with open(SRC_FOLDER / 'sample.md', 'r') as f:
    logging.debug(markdown.markdown(f.read(), extensions=[AltCheckExtension()]))

with open(SRC_FOLDER / 'missing_header.md', 'r') as f:
    logging.debug(markdown.markdown(f.read(), extensions=[TitleCheckExtension()]))

with open(SRC_FOLDER / 'list_sample.md', 'r') as f:
    logging.debug(markdown.markdown(f.read(), extensions=[AriaRoleExtension()]))

with open(SRC_FOLDER / 'role_sample.md', 'r') as f:
    print(markdown.markdown(f.read(), extensions=[AriaRoleExtension()]))

with open(SRC_FOLDER / 'table_sample.md', 'r') as f:
    #print(markdown.markdown(f.read(), extensions=['markdown.extensions.tables']))
    print(markdown.markdown(f.read(), extensions=[AriaTableExtension(), AriaTableIndexExtension()]))