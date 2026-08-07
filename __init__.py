"""
XML2 (official name) / xml2 (module name) - An XML parser I made.
I was bored. It is LIGHTWEIGHT, and doesn't even use any external modules that aren't in the standard library.
It is designed to be SUPER FAST, for a Python lexer. It won't beat lxml or the actual xml module, BUT it can
go really fast. Hence the lexing in the __init__.
"""
from copy import deepcopy
__all__ = {"XML",}
_deescape = lambda xml: xml.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&apos;", "'")
_escape = lambda xml: xml.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")

def _split(text, separator): #i used AI to make this _split(). what are you gonna do? say i mistreated god?
    parts = []
    current = []

    in_quotes = False
    quote_char = None

    for c in text:
        if c in "\"'":
            if not in_quotes:
                in_quotes = True
                quote_char = c
            elif c == quote_char:
                in_quotes = False
                quote_char = None

            current.append(c)
            continue

        if c == separator and not in_quotes:
            parts.append("".join(current))
            current.clear()
        else:
            current.append(c)

    parts.append("".join(current))
    return parts

class XML: #this is just a fancy class for a str lol
    def __init__(self, *args, **kwargs):
        self.super = str(*args, **kwargs)
        self.value = self.super
        self.lexed = self.lex()
        
    def parse(self):
        root_tag = None
        if self.super != self.value:
            self.lexed = self.lex() #updates the lexed
        thing = self.lexed
        
        stack = []
        for identifier, value in thing:
            
            if identifier == "START_TAG":
                thing2 = _split(value, " ")
                name = thing2[0]
                node = {"tag": name, "values": [], "attributes": {}}
                if len(thing2) > 1:
                    for i in thing2[1:]:
                        if i:
                            thing3 = _split(i, "=")
                            node["attributes"][thing3[0]] = _deescape(thing3[1].strip('"').strip("'"))
                        
                if root_tag is None:
                    root_tag = name
                stack.append(node)
            
            elif identifier == "TEXT":
                if stack:
                    stack[-1]["values"].append(value)
                    
            elif identifier == "END_TAG":
                if not stack:
                    continue
                if root_tag == value[1:]:
                    root_tag = None
                    continue
                the_node = stack.pop()
                stack[-1]["values"].append(the_node)
                
        return _XMLAST(stack)
    
    def lex(self):
        xml = self.super.__str__()
        buffer1 = ""
        output = []
        for index, i in enumerate(xml):
            if i == "<":
                output.append(("TEXT", _deescape(buffer1)))
                buffer1 = ""
            elif i == ">":
                if buffer1.startswith("/"):
                    output.append(("END_TAG", buffer1))
                else:
                    output.append(("START_TAG", buffer1))
                buffer1 = ""
            else:
                buffer1 += i
                
        if buffer1:
            output.append(("TEXT", _deescape(buffer1)))
        
        return output
    
    def __repr__(self):
        return "<XML object>"
    
    def __str__(self):
        return self.super.__str__()
    
    def escape(self):
        return _escape(self.super.__str__())
    
    def deescape(self):
        return _deescape(self.super.__str__())

class _XMLAST(list): #fancy list class lol
    def __repr__(self):
        return "<XML AST>"
    
    def __str__(self):
        return super().__repr__() #returns the true list
    
    def walk(self):
        for node in self:
            yield node
            yield from self._walk_node(node)

    def _walk_node(self, node):
        for child in node["values"]:
            if isinstance(child, dict):      # nested node
                yield child
                yield from self._walk_node(child)
            else:
                yield child                  # text node
                
    def _clean_node(self, node):
        new_node = {"tag": node["tag"], "attributes": node["attributes"], "values": []}
        for i in node["values"]:
            if isinstance(i, dict):
                new_node["values"].append(self._clean_node(i))
            elif i == "":
                continue
            else:
                new_node["values"].append(i)
                
        return new_node
    
    def clean(self):
        thing = deepcopy(self)
        output = []
        for i in thing:
            output.append(self._clean_node(i))
        
        return _XMLAST(output)


        
if __name__ == "__main__":                
    print(str(XML("<hello></hello>").parse().clean())) 
