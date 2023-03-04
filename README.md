# Accessibility4md

This repository contains a set of extensions for [Python-Markdown](https://github.com/Python-Markdown/markdown), focusing on the accessibility on the markdown file.

This project aim to demonstrate that the authors can improve the accessibility before publishing documents. This projects uses the visitor pattern to visit and check the each nodes parsed by python-markdown library and provides the feedback in console. 

# Prerequisite
```bash
pip install markdown
```

# Extension installation
```bash
cd src/extensions
python setup install
```

# Examples
## Check if alternative text is missing or duplicate.
```python
import markdown
from extensions.altcheckextension import AltCheckExtension
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO)
SRC_FOLDER = Path("src/samples")

with open(SRC_FOLDER / 'sample.md', 'r') as f:
    logging.debug(markdown.markdown(f.read(), extensions=[AltCheckExtension()]))
```
Output:
```bash
INFO:root:[WCAG 2.1 - 1.1.1 Non-text Content] Found an image with empty alt text for badcontrast1.png
INFO:root:[WCAG 2.1 - 1.1.1 Non-text Content] Found an image with duplicate alt text(same-alt-text-nearby) for badcontrast3.png
```

## Chain of extensions to produce HTML with attributes
The `AriaTableExtension` converts the markdown table into HTML format, and `AriaTableIndexExtension` adds the attributes for accessibility.
```python
import markdown
from extensions.aria_table_extension import AriaTableExtension, AriaTableIndexExtension
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO)

with open(SRC_FOLDER / 'table_sample.md', 'r') as f:
    print(markdown.markdown(f.read(), extensions=[AriaTableExtension(), AriaTableIndexExtension()]))
```
Output:
```html
<table aria-rowcount="3" role="table">
    <thead role="rowgroup">
        <tr aria-rowindex="None" role="row">
            <th role="columnheader">Header1</th>
            <th role="columnheader">Header2</th>
            <th role="columnheader">Header3</th>
        </tr>
    </thead>
    <tbody role="rowgroup">
        <tr aria-rowindex="1" role="row">
            <td role="cell">Row0 Cell1</td>
            <td role="cell">Row0 Cell2</td>
            <td role="cell">Row0 Cell3</td>
        </tr>
        <tr aria-rowindex="2" role="row">
            <td role="cell">Row1 Cell1</td>
            <td role="cell">Row1 Cell2</td>
            <td role="cell">Row1 Cell3</td>
        </tr>
        <tr aria-rowindex="3" role="row">
            <td role="cell">Row2 Cell1</td>
            <td role="cell">Row2 Cell2</td>
            <td role="cell">Row2 Cell3</td>
        </tr>
    </tbody>
</table>
```

## Other extensions developed
* TitleCheckExtension
* ImageContrastExtension[WIP]