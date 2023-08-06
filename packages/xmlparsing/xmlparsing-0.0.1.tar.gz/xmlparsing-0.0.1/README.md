![XMLParsing thumb](https://trinket-user-assets.trinket.io/6941b07c401d1545ca2798872d963cbc23b46221-63e29e94459c0b3016cbf3ea.png)

XMLParsing is an easy-to-use Python 3 parser for compiling, transforming, encoding and decoding XML files and text.

# XMLParsing installation:

**Run this in your command prompt/shell**

```
pip install xmlparsing
```

# XMLParsing convert dictionary:
*xmlparsing.dict2xml*

**INPUT:**

```python
import xmlparsing

myDict = {"numbers": [1, 2, 3], "letters": ["a", "b", "c"], "text": "Lorem ipsum dolor sit amet"} 
print(xmlparsing.dict2xml(myDict, title="all"))
```

**OUTPUT**:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<all>
    <numbers>
        <item i="0">1</item>
        <item i="1">2</item>
        <item i="2">3</item>
    </numbers>
    <letters>
        <item i="0">a</item>
        <item i="1">b</item>
        <item i="2">c</item>
    </letters>
    <text>Lorem ipsum dolor sit amet</text>
</all>
```

In the above, you can see that the "title" attribute in xmlparsing.dict2xml is what defines the tag that your entire document will be inside.

# XMLParsing convert JSON file:
*xmlparsing.jsonfil2xml*

**INPUT:**

```python
import xmlparsing

print(xmlparsing.jsonfile2xml('myStorage.json')
```

**The file "myStorage.json":**

```json
{
    "numbers": [
        1,
        2,
        3
    ],
    "letters": [
        "a",
        "b",
        "c"
    ],
    "text": "Lorem ipsum dolor sit amet"
}
```

**OUTPUT:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<myStorage>
    <numbers>
        <item i="0">1</item>
        <item i="1">2</item>
        <item i="2">3</item>
    </numbers>
    <letters>
        <item i="0">a</item>
        <item i="1">b</item>
        <item i="2">c</item>
    </letters>
    <text>Lorem ipsum dolor sit amet</text>
</myStorage>
```

# XMLParsing format XML:
*xmlparsing.formatxml*

**INPUT:**

```python
import xmlparsing

print(xmlparsing.formatxml('<?xml version="1.0" encoding="UTF-8"?> <all> <numbers> <item i="0">1</item> <item i="1">2</item> <item i="2">3</item> </numbers> <letters> <item i="0">a</item> <item i="1">b</item> <item i="2">c</item> </letters> <text>Lorem ipsum dolor sit amet</text> </all>'))
```

**OUTPUT:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<all>
    <numbers>
        <item i="0">1</item>
        <item i="1">2</item>
        <item i="2">3</item>
    </numbers>
    <letters>
        <item i="0">a</item>
        <item i="1">b</item>
        <item i="2">c</item>
    </letters>
    <text>Lorem ipsum dolor sit amet</text>
</all>
```

The code above cleans up XML.

# XMLParsing convert XML to dictionary:
*xmlparsing.xml2dict*

**INPUT:**

```python
import xmlparsing

print(xmlparsing.xml2dict('''
<all>
    <numbers>
        <item i="0">1</item>
        <item i="1">2</item>
        <item i="2">3</item>
    </numbers>
    <letters>
        <item i="0">a</item>
        <item i="1">b</item>
        <item i="2">c</item>
    </letters>
    <text>Lorem ipsum dolor sit amet</text>
</all>
'''))
```

**OUTPUT:**

```python
{'all': {'numbers': {'item': [{'@i': '0', '#text': '1'}, {'@i': '1', '#text': '2'}, {'@i': '2', '#text': '3'}]}, 'letters': {'item': [{'@i': '0', '#text': 'a'}, {'@i': '1', '#text': 'b'}, {'@i': '2', '#text': 'c'}]}, 'text': 'Lorem ipsum dolor sit amet'}}
```

# XMLParsing convert XML to JSON:
*xmlparsing.xml2json*

**INPUT:**

```python
import xmlparsing

print(xmlparsing.xml2json('''
<all>
    <numbers>
        <item i="0">1</item>
        <item i="1">2</item>
        <item i="2">3</item>
    </numbers>
    <letters>
        <item i="0">a</item>
        <item i="1">b</item>
        <item i="2">c</item>
    </letters>
    <text>Lorem ipsum dolor sit amet</text>
</all>
'''))
```

**OUTPUT:**

```json
{
    "all": {
        "letters": {
            "item": [
                {
                    "#text": "a",
                    "@i": "0"
                },
                {
                    "#text": "b",
                    "@i": "1"
                },
                {
                    "#text": "c",
                    "@i": "2"
                }
            ]
        },
        "numbers": {
            "item": [
                {
                    "#text": "1",
                    "@i": "0"
                },
                {
                    "#text": "2",
                    "@i": "1"
                },
                {
                    "#text": "3",
                    "@i": "2"
                }
            ]
        },
        "text": "Lorem ipsum dolor sit amet"
    }
}
```

# THE END!
# Enjoy using XMLParsing!
