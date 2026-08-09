# XML2

XML2 (official name) / `xml2` (module name) - An XML parser I made.
I was bored. It is LIGHTWEIGHT, and doesn't even use any external modules that aren't in the standard library.
It is designed to be SUPER FAST, for a Python lexer. It can beat `lxml` or the actual `xml` module, BUT only on
small XML files.. Hence the lexing in the `__init__`. It is recommended for small XML files, that's where it goes
faster than `lxml` or `xml`.

You can download it by running `pip install git+https://github.com/Sys67654tdcm/XML2---A-lightweight-Python-module-for-parsing-XML.git#egg=xml2` in your terminal.

If you would like to parse XML, you need to run something like this:
```python
from xml2 import XML
print(XML("<hello><world>!</world></hello>").parse())
```
All the logic is stored in the `XML` class.
For XML like `<hello><world>!</world></hello>`, `XML.parse` should return
```python
[{
  "tag": "hello",
  "values": [
    {"tag": "world",
      "values": ["!"]
    }
  ],
  "attributes": {}
}]
```
Please note that you can call `XML.clean()` on the return value from `XML.parse`.
