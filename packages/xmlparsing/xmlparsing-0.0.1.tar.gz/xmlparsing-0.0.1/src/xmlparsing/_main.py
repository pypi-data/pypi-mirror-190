import xmlformatter
import xml_to_dict
import json


def dict2xml(keys, indent=4, title="body"):
    out = f'<?xml version="1.0" encoding="UTF-8"?><{title}>'
    
    def init(txt):
        output = ''
        
        if type(txt) == dict:
            for i in txt:
                output += f"<{i}>"
                output += init(txt[i])
                output += f"</{i}>"
        elif type(txt) == list:
            for i in txt:
                output += f'<item i="{txt.index(i)}">'
                output += init(i)
                output += f"</item>"
        elif type(txt) == str:
            output += txt
        elif type(txt) == int:
            output += str(txt)
        elif type(txt) == bool:
            output += str(txt)
        elif type(txt) == type(None):
            output += str(txt)
        else:
            raise TypeError(f"cannot process unknown type of '{type(keys)}'")
        
        return output
    
    out += init(keys)
    
    out += f"</{title}>"
    
    return xmlformatter.Formatter(indent=indent).format_string(out).decode('utf-8')


def json2xml(text, indent=4, title="body"):
    return dict2xml(json.loads(text), indent=indent, title=title)


def jsonfile2xml(file, indent=4):
    if file.split('.')[len(file.split('.')) - 1] == "json":
        fs = open(file, 'r')
        content = fs.read()
        fs.close()
        
        n = file.split('.')
        n.pop(len(n) - 1)
        
        return json2xml(content, indent=indent, title='.'.join(n))
    else:
        raise NameError(f"content and extension name of file '{file}' did not match JSON requirements.")


def formatxml(text, indent=4):
    return xmlformatter.Formatter(indent=indent).format_string(text).decode('utf-8')


def xml2dict(text):
    return xml_to_dict.XMLtoDict().parse(text)


def xml2json(text, indent=4):
    return json.dumps(xml_to_dict.XMLtoDict().parse(text), indent=indent, sort_keys=True)


def exportxml(text, name="__default__"):
    global x
    x = 1
    
    def Download():
        global x
        
        try:
            fs = open(f'Download_{str(x).zfill(3)}.xml', 'x')
            fs.write(text)
            fs.close()
        except FileExistsError:
            x += 1
            Download()
        except Exception as e:
            raise e
    
    if name == "__default__":
        Download()
    else:
        fs = open(f'{name}.xml', 'x')
        fs.write(text)
        fs.close()
