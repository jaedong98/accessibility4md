# Library References
- [Tutorial 1 Writie Extensions for Python Markdown](https://github.com/Python-Markdown/markdown/wiki/Tutorial-1---Writing-Extensions-for-Python-Markdown)
- [Extention Implementation](https://github.com/TankerHQ/python-markdown/blob/master/docs/extensions/api.md)
- [How to meet WCAG21](https://www.w3.org/WAI/WCAG21/quickref/?showtechniques=145%2C244#consistent-navigation)
- [Extention APIs](https://github.com/Python-Markdown/markdown/blob/master/docs/extensions/api.md)
- [ARIA guides](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/ARIA_Guides)
- [Web Accessibility Initiative - Accessible Rich Internet Applications(WAI-ARIA) Basics](https://developer.mozilla.org/en-US/docs/Learn/Accessibility/WAI-ARIA_basics)
- [Definition of ARIA Roles](https://www.w3.org/TR/wai-aria-1.1/#role_definitions)
- [Definition of ARIA States and Properties](https://www.w3.org/TR/wai-aria-1.1/#state_prop_def)
  
# Setup Dev
## virtualenv

To install :
```powershell
pip install --user virtualenv
```

To create a virtual environment (venv):
```powershell
python -m virtualenv venv
```

To activate:

On Windows, open powershell (in visual studio) and run 
```powershell
.\venv\Scripts\activate.bat
-- or --
/venv/Scripts/Activate.ps1
```

On Mac
```bash
source venv/bin/activate
```

to deactivate:

On Windows
```powershell
.\venv\Scripts\deactivate.bat
```

On Mac
```bash
deactivate
```

## Install packages

```powershell
(venv) PS ..\accessibility4md> pip install markdown
```

## Development flow

### Step 0. Create and activate the virtual environment.

### Step 1. Implement `Extension`

### Step 2. Update `setup.py` (One time for each extension)

### Step 3. Implement extension and install

## Install Extensions with `develop` option.

```powershell
(venv) PS ..\accessibility4md\src\myextension> python setup.py develop
```
Note that the `develop` subcommand was run rather than the install subcommand. As the plugin isn't finished yet, this special development mode sets up the path to run the plugin from the source file rather than Python's site-packages directory. That way, any changes made to the file will immediately take effect with no need to re-install the extension.