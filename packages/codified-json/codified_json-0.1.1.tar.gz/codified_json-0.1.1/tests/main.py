import json
from codified_json import CJsonReader, CJsonWriter

obj = [
    {"apple": "a", "clementine": 4, "banana": "e"}, 
    {"clementine": 4, "banana": 5, "apple": 34}, 
    {"banana": 4.5, "apple": False, "clementine": 4}, 
    {"clementine": 4, "apple": None, "banana": True}
]
print(json.dumps(obj))

writer = CJsonWriter(obj)
cjson_str = writer.to_str()
print(cjson_str)

obj1 = CJsonReader().from_str(cjson_str)
print(json.dumps(obj1))

filename1 = 'test.cjson'
cjson = writer.to_file(filename1)
obj2 = CJsonReader().from_file(filename1)
print(json.dumps(obj2))

filename2 = 'test.cjson.zip'
cjson_bytes = writer.to_compressed_bytes_file(filename2)
obj3 = CJsonReader().from_compressed_bytes_file(filename2)
print(json.dumps(obj3))
