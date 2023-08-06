# Codified-JSON

*Codified-JSON* is a new representation of *JSON* for transfering payloads as smaller sizes between software applications.

Please read the specifications for the *Codified-JSON* representation here: 

https://ty2huang.github.io/codified-json/

This library helps translate between python objects and the *Codified-JSON* representation (stored as string or compressed bytes).

## Installation

```
pip install --force-reinstall git+https://github.com/ty2huang/codified-json-python-library.git
```

## Getting started

Translating between JSON-compatible python objects and *Codified-JSON* is very easy.

```Python
import codified_json as cjson

data = [
    {"apple": "a", "clementine": 4, "banana": "e"}, 
    {"clementine": 4, "banana": 5, "apple": 34}, 
    {"banana": 4.5, "apple": False, "clementine": 4}, 
    {"clementine": 4, "apple": None, "banana": True}
]

# Encode into codified-json string using "cjson.as_str"
cjson_str = cjson.as_str(data)

# Decode back to python objects using "cjson.parse_str"
decoded_data = cjson.parse_str(cjson_str)

assert data == decoded_data
```

## Further Information

Following the example from the "Getting Started" section, if you print out `data` as JSON string vs *Codified-JSON* string, you'll find that the *Codified-JSON* representation is shorter.

```Python
import json

def test():
    json_str = json.dumps(data)
    print(f"As JSON (length {len(json_str)}):")
    print(json_str)
    print()
    print(f"As Codified-JSON (length {len(cjson_str)}):")
    print(cjson_str)

test()
```

Output is printed below. Size difference gets bigger as the JSON array size increases.

```json
As JSON (length 193):
[{"apple": "a", "clementine": 4, "banana": "e"}, {"clementine": 4, "banana": 5, "apple": 34}, {"banana": 4.5, "apple": false, "clementine": 4}, {"clementine": 4, "apple": null, "banana": true}]

As Codified-JSON (length 146):
{"s":{"0":["apple","banana","clementine"]},"b":[{"i":0,"v":["a","e",4]},{"i":0,"v":[34,5,4]},{"i":0,"v":[false,4.5,4]},{"i":0,"v":[null,true,4]}]}
```

## Tests

```
python setup.py pytest
```

## License

The "codified_json" module was written by Tim Huang, and is released under the MIT license.

See the file LICENSE for more details.
