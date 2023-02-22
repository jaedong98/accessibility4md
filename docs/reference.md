# Library References
- [Tutorial 1 Writie Extensions for Python Markdown](https://github.com/Python-Markdown/markdown/wiki/Tutorial-1---Writing-Extensions-for-Python-Markdown)
- [Extention Implementation](https://github.com/TankerHQ/python-markdown/blob/master/docs/extensions/api.md)
- [How to meet WCAG21](https://www.w3.org/WAI/WCAG21/quickref/?showtechniques=145%2C244#consistent-navigation)
- [Extention APIs](https://github.com/Python-Markdown/markdown/blob/master/docs/extensions/api.md)

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
On Windows
```powershell
.\venv\Scripts\activate.bat
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


## Install Extensions

```powershell
(venv) PS ..\accessibility4md\src\myextension> python setup.py develop
```
Note that the `develop` subcommand was run rather than the install subcommand. As the plugin isn't finished yet, this special development mode sets up the path to run the plugin from the source file rather than Python's site-packages directory. That way, any changes made to the file will immediately take effect with no need to re-install the extension.