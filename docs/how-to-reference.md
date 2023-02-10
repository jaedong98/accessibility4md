## Introduction

In addition to providing a number of built-in extensions, Python-Markdown provides an application programming interface (API) which allows anyone to write their own extensions to alter the existing behavior and/or add new behavior. As the [API Documentation] can be a little overwhelming when starting out, the following tutorial will step you through the process of getting a simple Inline Processor extension working, then adding more features to it. Various steps will be repeated in different ways to demonstrate various parts of the API. 

[API Documentation]: https://python-markdown.github.io/extensions/api/

First, we need to establish the syntax we will be implementing. Rather than re-implement any existing Markdown syntax, lets create some different syntax that is not typical of Markdown. In fact, we'll implement  a subset of the inline syntax used by the [txt2tags] markup language. The syntax looks like this:

[txt2tags]: http://mostlylinux.wordpress.com/textanddocument/txt2tagscheatsheet/#inlinebold

* Two hyphens for strike: `--del--` => `<del>del</del>` => <del>del</del> 
* Two underscores for underline: `__ins__` => `<ins>ins</ins>` => <ins>ins</ins>
* Two asterisks for bold: `**strong**` => `<strong>strong</strong>` => <strong>strong</strong>.
* Two slashes for italic: `//emphasis//` => `<em>emphasis</em>` => <em>emphasis</em>.

## Boilerplate Code

The first step is to create the boilerplate code that will be required by any Python-Markdown Extension.

__Warning__: This tutorial is very generic and makes no assumptions about your development environment. Some of the commands below may generate errors on some (but not all) systems unless they are run by a user who has the correct permissions. To avoid these types of issues, it is suggested that [virtualenv][] be used for development in an environment isolated from your primary system; although doing so is certainly not required. As setting up an appropriate development environment applies to any Python development (developing Markdown extensions adds no additional requirements), it is beyond the scope of this tutorial. A basic understanding of Python development is expected.

[virtualenv]: http://virtualenv.readthedocs.org/en/latest/

First create a new directory to save your extension files to. From the commandline do the following:

```sh
mkdir myextension
cd myextension
```

Be sure to save all files within the "myextension" directory you just created. Note that we are naming the extension "myextension". You may use a different name, but be sure to use whatever name you chose consistently throughout. 

Create the first Python file, name it `myextension.py`, and add the following boilerplate code to it:

```python
from markdown.extensions import Extension

class MyExtension(Extension):
   def extendMarkdown(self, md):
       # Insert code here to change markdown's behavior.
       pass
```

After saving that file, create a second Python file, name it `setup.py`, and add the following code to it:

```python
from setuptools import setup
setup(
    name='myextension',
    version='1.0',
    py_modules=['myextension'],
    install_requires = ['markdown>=3.0'],
)
``` 

Finally, from the commandline run the following command to tell Python about your new extension:

```sh
python setup.py develop
```

Note that the `develop` subcommand was run rather than the `install` subcommand. As the plugin isn't finished yet, this special development mode sets up the path to run the plugin from the source file rather than Python's `site-packages` directory. That way, any changes made to the file will immediately take effect with no need to re-install the extension.

Also note that the setup script expects that [setuptools][st] is installed. While setuptools is not necessary (just do `from distutils.core import setup` instead), we only get the `develop` subcommand if we use setuptools. Any system which has [pip][] and/or [virtualenv][venv] installed (both recommended) will also have setuptools installed.

[st]: https://pypi.python.org/pypi/setuptools
[pip]: http://www.pip-installer.org/
[venv]: http://virtualenv.readthedocs.org/en/latest/

To ensure that everything is working correctly, try passing the extension to Markdown. Open a python interpreter and try the following:

```python
>>> import markdown
>>> from myextension import MyExtension
>>> markdown.markdown('foo bar', extensions=[MyExtension()])
'<p>foo bar</p>'
```

Obviously, the extension doesn't do anything useful, but now that we have it in place with no errors, we can actually start implementing our new syntax.

## Using Generic Patterns

To start, let's implement the one part of that syntax that doesn't overlap with Markdown's standard syntax; the `--del--` syntax, which will wrap the text in `<del>` tags.

The first step is to write a regular expression to match the del syntax.

```python
DEL_RE = r'(--)(.*?)--'
```

Note that the first set of hyphens (`(--)`) are grouped in parentheses, making our content the second group. This is because we will be using a generic pattern class provided by Python-Markdown. Specifically, the `SimpleTextPattern` which will modify the pattern to prepend another group, and then expects the text content to be found in `group(3)` of the new regular expression. We add the extra group to force the content we want into`group(3)`.

Also note that the content is matched using a non-greedy match `(.*?)`. Otherwise, everything between the first occurrence and the last would all be placed inside one `<del>` tag, which we do not want.

So, let's incorporate our regular expression into Markdown:

```python
from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern

DEL_RE = r'(--)(.*?)--'
    
class MyExtension(Extension):
    def extendMarkdown(self, md):
        # Create the del pattern
        del_tag = SimpleTagPattern(DEL_RE, 'del')
        # Insert del pattern into markdown parser
        md.inlinePatterns.add('del', del_tag, '>not_strong')
```

If you noticed, we added two lines. The first line creates an instance of a `markdown.inlinePatterns.SimpleTagPattern`. This generic pattern class takes two arguments; the regular expression to match against (in this case `DEL_RE`), and the name of the tag to insert the text of `group(3)` into (`'del'`).

The second line adds our new pattern to the Markdown parser. In the event that it is not obvious, the `extendMarkdown` method of any `markdown.Extension` class is passed "md", the instance of the `Markdown` class we want to modify. In this case, we are inserting a new inline pattern named `'del'`, using our pattern instance `del_tag` after the pattern named "not_strong" (thus the `'>not_strong'`).  

This time, we used the `add` method, even though it is deprecated.  In a future version, you will first need to determine the actual priority number, looking in [inline_patterns.py's build_inlinepatterns()](https://github.com/Python-Markdown/markdown/blob/master/markdown/inlinepatterns.py#L73), choosing 75 as a bit before "not_strong", and then using `md.inlinePatterns.register(del_tag, 'del', 75)`.

Now let's test our new extension. Open a python interpreter and try the following:

```python
>>> import markdown
>>> from myextension import MyExtension
>>> markdown.markdown('foo --deleted-- bar', extensions=[MyExtension()])
'<p>foo <del>deleted</del> bar</p>'
```

Notice that we imported the `MyExtension` class from the `'myextension'` module. We then passed an instance of that class to the `extensions` keyword of `markdown.markdown`.  We can also see the HTML returned, which would display in the browser as:

> <p>foo <del>deleted</del> bar</p>

Let's add our syntax for `__ins__`, which will use the `<ins>` tag.

```python
DEL_RE = r'(--)(.*?)--'
INS_RE = r'(__)(.*?)__'
    
class MyExtension(Extension):
    def extendMarkdown(self, md):
        del_tag = SimpleTagPattern(DEL_RE, 'del')
        md.inlinePatterns.add('del', del_tag, '>not_strong')
        ins_tag = SimpleTagPattern(INS_RE, 'ins')
        md.inlinePatterns.add('ins', ins_tag, '>del')
```

That should be self explanatory. We simply created a new pattern which matches our `'ins'` syntax and added it after the `'del'` pattern. 

We could be done with the `'ins'` syntax, except that we now have two possible results defined for text surrounded by double underscores. Recall that Markdown's existing bold syntax (`__bold__`) is still defined in the parser. However, as our new insert syntax was inserted in the `inlinePatterns` before the bold pattern, the insert pattern runs first and consumes the double underscore markup before the bold pattern ever has a chance to find it. Even so, the existing bold pattern is still being run against the text and slowing down the parser unnecessarily. Therefore, it is always good practice to remove any parts that are no longer needed.

However, as we will be defining our own new bold syntax, we can actually override or replace the old pattern with our new one. The same applies to our emphasis pattern.

First, we need to define our new regular expressions. We can use the same expressions from last time with a few modifications.

```python
STRONG_RE = r'(\*\*)(.*?)\*\*'
EMPH_RE = r'(\/\/)(.*?)\/\/'
```

Now we need to insert these into the markdown parser. However, unlike with insert and delete, we need to override the existing inline patterns. Markdown's strong and emphasis syntax is currently implemented with two inline patterns; `'em_strong'` (for asterixes) and `'em_strong2'` (for underscores).  

Let's override `'em_strong'` first.

```python
class MyExtension(Extension):
    def extendMarkdown(self, md):
        ...
        # Create new strong pattern
        strong_tag = SimpleTagPattern(STRONG_RE, 'strong')
        # Override existing strong pattern
        md.inlinePatterns['em_strong'] = strong_tag
```

Notice that rather than "add"ing a new pattern before or after an existing pattern, we simple reassigned the value of a pattern named `'em_strong'`. This is because the old pattern named '`strong'` already existed and we don't need to change its location in the parser. So we simply assign a new pattern instance to it.  Like, `add()`, this method is deprecated, so you may need to `md.inlinePatterns.register(strong_tag, 'em_strong', 60)` later.

We can set `'emphasis'` by assigning it as well.  It will get a default priority of very low:

```python
class MyExtension(Extension):
    def extendMarkdown(self, md):
        ...
        emph_tag = SimpleTagPattern(EMPH_RE, 'em')
        md.inlinePatterns['emphasis'] = emph_tag
```

Now we have one old pattern left, `'em_strong2'`. The `'em_strong2'` pattern just handled underscores, including the special case that `under_scored_words` are not emphasis, but as our new syntax requires double underscores, it's not needed any more. Therefore, we can delete it. With the Markdown syntax, due to both strong and emphasis using the same characters, special cases were needed to match the two nested together (i.e.: `___like this___` or `___like_this__`). Again this isn't needed for our new syntax. We can delete it by deregistering it:

```python
class MyExtension(markdown.Extension):
    def extendMarkdown(self, md):
        ...
        md.inlinePatterns.deregister('em_strong2')
```

That implements all of our new syntax. For completeness, the entire extension should look like this:

```python
from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern

DEL_RE = r'(--)(.*?)--'
INS_RE = r'(__)(.*?)__'
STRONG_RE = r'(\*\*)(.*?)\*\*'
EMPH_RE = r'(\/\/)(.*?)\/\/'

class MyExtension(Extension):
    def extendMarkdown(self, md):
        del_tag = SimpleTagPattern(DEL_RE, 'del')
        md.inlinePatterns.add('del', del_tag, '>not_strong')
        ins_tag = SimpleTagPattern(INS_RE, 'ins')
        md.inlinePatterns.add('ins', ins_tag, '>del')
        strong_tag = SimpleTagPattern(STRONG_RE, 'strong')
        md.inlinePatterns['em_strong'] = strong_tag
        emph_tag = SimpleTagPattern(EMPH_RE, 'em')
        md.inlinePatterns['emphasis'] = emph_tag
        md.inlinePatterns.deregister('em_strong2')
```
 
And to make sure it is working properly, run the following from the Python interpreter:

```python
>>> import markdown
>>> from myextension import MyExtension
>>> txt = """
... Some __underline__
... Some --strike--
... Some **bold**
... Some //italics//
... """
... 
>>> markdown.markdown(txt, extensions=[MyExtension()])
"<p>Some <ins>underline</ins>\nSome <del>strike</del>\nSome <strong>bold</strong>\nSome <em>italics</em>"
```

## Creating your own Pattern Class

However, you may notice that there is a lot of repetition in that code. In fact, all four of our new regular expressions could easily be condensed into one regular expression. And having only one pattern to run would be more performant that four.

Let's refactor our four regular expressions into one new expression:

```python
MULTI_RE = r'([*/_-]{2})(.*?)\2'
```

Note the regular expression will be modified to capture one group first, so this can be read as 'get two matching punctuation marks as group 2, the tagged text as group 3, and then another copy of the punctuation marks'.

As no generic pattern class exists that will be able to use that regular expression, we will need to define our own. All pattern classes should inherit from the `markdown.inlinepatterns.Pattern` base class. At the very least, our subclass should define a `handleMatch` method which accepts a regex [`MatchObject`][mo] and returns an ElementTree [`Element`][el].

[mo]: https://docs.python.org/3/library/re.html#match-objects
[el]: https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element

```python
from markdown.inlinepatterns import Pattern
from markdown.extensions import Extension
import xml.etree.ElementTree as etree

class MultiPattern(Pattern):
    def handleMatch(self, m):
        if m.group(2) == '**':
            # Bold
            tag = 'strong'
        elif m.group(2) == '//':
            # Italics
            tag = 'em'
        elif m.group(2) == '__':
            # Underline
            tag = 'ins'
        else:   # must be m.group(2) == '--':
            # Strike
            tag = 'del'
        # Create the Element
        el = etree.Element(tag)
        el.text = m.group(3)
        return el
```

Now we need to tell Markdown about our new pattern and delete the now unnecessary existing patterns:

```python
class MultiExtension(Extension):
    def extendMarkdown(self, md):
        # Delete the old patterns
        md.inlinePatterns.deregister('em_strong')
        md.inlinePatterns.deregister('em_strong2')
        md.inlinePatterns.deregister('not_strong')

        # Add our new MultiPattern
	multi = MultiPattern(MULTI_RE)
        md.inlinePatterns['multi'] = multi
```

For completeness, the newly added code should look like this:

```python
from markdown.inlinepatterns import Pattern
from markdown.extensions import Extension
import xml.etree.ElementTree as etree

MULTI_RE = r'([*/_-]{2})(.*?)\2'

class MultiPattern(Pattern):
    def handleMatch(self, m):
        if m.group(2) == '**':
            # Bold
            tag = 'strong'
        elif m.group(2) == '//':
            # Italics
            tag = 'em'
        elif m.group(2) == '__':
            # Underline
            tag = 'ins'        
        else:   # must be m.group(2) == '--':
            # Strike
            tag = 'del'
        # Create the Element
        el = etree.Element(tag)
        el.text = m.group(3)
        return el

class MultiExtension(Extension):
    def extendMarkdown(self, md):
        # Delete the old patterns
        md.inlinePatterns.deregister('em_strong')
        md.inlinePatterns.deregister('em_strong2')
        md.inlinePatterns.deregister('not_strong')

        # Add our new MultiPattern
        multi = MultiPattern(MULTI_RE)
        md.inlinePatterns['multi'] = multi
```

After adding that code to the `myextension.py` file, open the Python interpreter:

```python
>>> import markdown
>>> from myextension import MultiExtension
>>> txt = """
... Some __underline__
... Some --strike--
... Some **bold**
... Some //italics//
... """
... 
>>> markdown.markdown(txt, extensions=[MultiExtension()])
"<p>Some <ins>underline</ins>\nSome <del>strike</del>\nSome <strong>bold</strong>\nSome <em>italics</em>"
```

## Adding Config Options

Now suppose that we want to offer some configuration options to our extension. Perhaps we want to only offer the insert and delete syntax as an option which the user can turn on and off.

To start, let's break our regular expression into two:

```python
STRONG_EM_RE = r'([*/]{2})(.*?)\2'
INS_DEL_RE = r'([_-]{2})(.*?)\2'
```

Then, we need to define our config options on our newly renamed `Extension` subclass:

```python
class ConfigExtension(Extension):
    def __init__(self, **kwargs):
        # Define config options and defaults
        self.config = {
            'ins_del': [False, 'Enable Insert and Delete syntax.']
        }
        # Call the parent class's __init__ method to configure options
        super().__init__(**kwargs)
```

We defined our config options as the dict, `self.config` with keys being the names of the options. Each value is a two item list, the default value of the option and its description.  We use a list instead of a tuple because the `Extension` class requires `config` to be mutable.  

Finally, refactor the `extendMarkdown` method to account for the config option:

```python
    def extendMarkdown(self, md):
        ...
        # Add STRONG_EM pattern
        strong_em = MultiPattern(STRONG_EM_RE)
        md.inlinePatterns['strong_em'] = strong_em
        # Add INS_DEL pattern if active
        if self.getConfig('ins_del'):
            ins_del = MultiPattern(INS_DEL_RE)
            md.inlinePatterns['ins_del'] = ins_del
```

We simply created one instance of our `MultiPattern` class for strong and emphasis, and if the `'ins_del'` config option is `True`, we create a second instance of the `MultiPattern` class.

For completeness, all of the newly added code should look like this:

```python
STRONG_EM_RE = r'([*/]{2})(.*?)\2'
INS_DEL_RE = r'([_-]{2})(.*?)\2'

class ConfigExtension(Extension):
    def __init__(self, **kwargs):
        # Define config options and defaults
        self.config = {
            'ins_del': [False, 'Enable Insert and Delete syntax.']
        }
        # Call the parent class's __init__ method to configure options
        super().__init__(**kwargs)
        
    def extendMarkdown(self, md):
        # Delete the old patterns
        md.inlinePatterns.deregister('em_strong')
        md.inlinePatterns.deregister('em_strong2')
        md.inlinePatterns.deregister('not_strong')

        # Add STRONG_EM pattern
        strong_em = MultiPattern(STRONG_EM_RE)
        md.inlinePatterns['strong_em'] = strong_em
        # Add INS_DEL pattern if active
        if self.getConfig('ins_del'):
            ins_del = MultiPattern(INS_DEL_RE)
            md.inlinePatterns['ins_del'] = ins_del
```

After saving your changes, open the Python interpreter:

```python
>>> import markdown
>>> from myextension import ConfigExtension
>>> txt = """
... Some __underline__
... Some --strike--
... Some **bold**
... Some //italics//
... """
... 
>>> # First try it with ins_del set to True
>>> markdown.markdown(txt, extensions=[ConfigExtension(ins_del=True)])
"<p>Some <ins>underline</ins>\nSome <del>strike</del>\nSome <strong>bold</strong>\nSome <em>italics</em>"
>>> # Now try it with ins_del defaulting to False
>>> markdown.markdown(txt, extensions=[ConfigExtension()])
"<p>Some __underline__\nSome --strike--\nSome <strong>bold</strong>\nSome <em>italics</em>"
```

## Supporting Extension Names (as strings)

You may have noted that each time we tested our extension, we had to import the extension and pass in an instance of the `Extension` subclass. While this is the prefered way to call extensions, at times a user may need to call Markdown from the command line or a templating system, and may only be able to pass in strings. 

This feature is built-in for free. However, your users will need to know and use the import path (Python dot notation) of the Extension class you defined. For example, each of the three classes we defined above would be called like this:

```python
>>> markdown.markdown(txt, extensions=['myextension:MyExtension'])
>>> markdown.markdown(txt, extensions=['myextension:MultiExtension'])
>>> markdown.markdown(txt, extensions=['myextension:ConfigExtension'])
```

Note that a colon (`:`) must be used between the path and the Class. Whereas a dot (`.`) must be used for the rest of the path. Think of it as replacing the `import` part of the "from" import statement with the colon. For example, if you had an extension class, `FooExtension`, defined in the file `somepackage/extensions/foo.py`, then the import statement would be `from somepackage.extensions.foo import FooExtension` and the string based name would be `'somepackage.extensions.foo:FooExtension'`.

In fact, if you created a new class in each of the steps above rather than refactoring the previous one, all three extensions could live within the same module and still all be called separately. This works great when you have built a number of extensions as part of a larger project (perhaps a CMS, a static blog generator, etc) that will only be used internally.

However, if you intend to distribute your extension as a standalone module for others to incorporate into their projects, you may want to enable support for a shorter name. No doubt, `'myextension'` is easier for your users to type (and you to document) than `'myextension:MyExtension'`. And as all of the built-in extensions that ship with Python-Markdown work this way, users will likely expect the same. To enable this feature, add the following to the bottom of your extension:

```python
def makeExtension(**kwargs):
    return ConfigExtension(**kwargs)
```

Note that this module level function simply returns an instance of your `Extension` subclass. When Markdown is provided with a string, it expects that string to use Python's dot notation pointing to the importable path of the module. Then if no colon is found in the string, it calls the `makeExtension` function found in that module.

Let's test our extension by opening the python interpreter again:

```python
>>> import markdown
>>> txt = """
... Some __underline__
... Some --strike--
... Some **bold**
... Some //italics//
... """
... 
>>> markdown.markdown(txt, extensions=['myextension'])
"<p>Some __underline__\nSome --strike--\nSome <strong>bold</strong>\nSome <em>italics</em>"
```

As we used the ConfigExtension above, let's pass some config options to the extension:

```python
>>> markdown.markdown(
... 	txt, 
... 	extensions=['myextension'],
... 	extension_configs = {
... 		'myextension': {'ins_del': True}
... 	}
...	)
"<p>Some <ins>underline</ins>\nSome <del>strike</del>\nSome <strong>bold</strong>\nSome <em>italics</em>"
```

Notice that we got support for the extension_configs keyword with no extra work. See the documentation for a full explanation of the [extension_configs][ec] keyword.

[ec]: https://pythonhosted.org/Markdown/reference.html#extension_configs

## Preparing for Distribution

As a `setup.py` script has already been created, the most important part of preparing an extension for distribution is completed. However, the setup script was pretty basic. It is recommended that a little more metadata be included, in particular the developer's name, email address and a URL for the project (see the section [Writing the Setup Script][pydoc] of the Python documentation for an example). It is also suggested that at a minimum README and LICENCE files be included in the directory.

[pydoc]: https://docs.python.org/3/distutils/setupscript.html#setup-script

At this point, you could commit your code to a version control system (such as Git, Mercurial, Subversion or Bazaar) and upload it to a host which supports your system of choice. Then your users can easily use a [pip command][pipvcs] to download and install your extension. 

[pipvcs]: http://pip.readthedocs.org/en/latest/reference/pip_install.html#vcs-support

Or, for an even simpler command, you could upload your project to the [Python Package Index][PyPI]. Alternatively, you could use some of the subcommands (such as `sdist`) available on the setup.py script to create a file (such as a zip or tar file) to provide for your users to download. While the specifics are beyond the scope of this tutorial, the Python documentation on [Distributing Python Modules][distutils]  and the Setuptools Documentation on [Building and Distributing Packages][stbd] both offer explanations of the options available.

[PyPI]: https://pypi.python.org/pypi
[distutils]: https://docs.python.org/3/distutils/index.html
[stbd]: https://pythonhosted.org/setuptools/setuptools.html

## Conclusion

While this tutorial only demonstrated use of [Inline Processors], the extension API also includes support for [Preprocessors], [Block Processors], [Tree Processors] and [Postprocessors]. Even though each type of processor serves a different purpose---running at a different stage in the parsing process---the same basic principles apply to each type of processor. In fact, a single extension can alter multiple different types of processors.

[Preprocessors]: https://python-markdown.github.io/extensions/api#preprocessors
[Block Processors]: https://python-markdown.github.io/extensions/api#blockparser
[Tree Processors]: https://python-markdown.github.io/extensions/api#treeprocessors
[Inline Processors]: https://python-markdown.github.io/extensions/api#inlinepatterns
[Postprocessors]: https://python-markdown.github.io/extensions/api#postprocessors

Reviewing the [API Documentation] and the [source code] of the various built-in extensions should provide you with enough information to build you own great extensions. Of course, if you would like assistance, feel free to ask for help on the [mailing list]. And please, don't forget to list your extensions on the [wiki] so other people can find them.

[source code]: https://github.com/waylan/Python-Markdown
[mailing list]: http://lists.sourceforge.net/lists/listinfo/python-markdown-discuss
[wiki]: https://github.com/waylan/Python-Markdown/wiki/Third-Party-Extensions