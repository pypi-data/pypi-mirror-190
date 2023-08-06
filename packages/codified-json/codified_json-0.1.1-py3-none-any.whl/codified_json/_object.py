import json
from codified_json._structures import *

STRUCTURES = 's'
BODY = 'b'

INDEX = 'i'
VALUE = 'v'

class CJsonObject:
    def __init__(self, structures, content=None):
        self.structures = structures
        self.content = content


def decode(cjson_str):
    
    def cjson_str_to_cjson_obj(cjson_str):
        json_object = json.loads(cjson_str)
        structures = CJsonStructures(json_object[STRUCTURES])
        return CJsonObject(structures, json_object[BODY])

    def get_decoded_children(children, structures):
        list_obj = []
        for child in children:
            new_node = CJsonObject(structures, child)
            list_obj.append(decode_helper(new_node))
        return list_obj

    def decode_helper(cjson_obj):
        if type(cjson_obj.content) in [type(None), bool, str, int, float] or cjson_obj.content == {}:
            return cjson_obj.content
        elif type(cjson_obj.content) in [list, tuple]:
            return get_decoded_children(cjson_obj.content, cjson_obj.structures)
        else:
            json_dict = {}
            keys = cjson_obj.structures.get_struct_from_id(cjson_obj.content[INDEX])
            values = get_decoded_children(cjson_obj.content[VALUE], cjson_obj.structures)
            for k, v in zip(keys, values):
                json_dict[k] = v
            return json_dict

    return decode_helper(cjson_str_to_cjson_obj(cjson_str))


def encode(obj, structures_as_array=False):
    structures = get_structures(obj)

    def get_encoded_children(children, transformer=lambda x: x):
        content = []
        for child in children:
            new_node = encode_helper(transformer(child))
            content.append(new_node.content)
        return content

    def encode_helper(obj):
        node = CJsonObject(structures)
        if type(obj) in [type(None), bool, str, int, float] or obj == {}:
            node.content = obj
        elif type(obj) in [list, tuple]:
            node.content = get_encoded_children(obj)
        elif type(obj) == dict:
            struct = structures.make_struct_from_dict(obj)
            body = get_encoded_children(struct, lambda x: obj[x])
            node.content = {INDEX: structures.index_by_struct[struct], VALUE: body}
        else:
            raise TypeError(f'Object of type {obj.__class__.__name__} cannot be encoded as codified-JSON')
        return node

    def cjson_obj_to_cjson_str(cjson_obj, structures_as_array):
        json_value = cjson_obj.structures.to_json_array()
        if not structures_as_array:
            json_value = { str(idx):val for idx, val in enumerate(json_value) }
        return json.dumps({ STRUCTURES: json_value, BODY: cjson_obj.content }, separators=(',', ':'))

    return cjson_obj_to_cjson_str(encode_helper(obj), structures_as_array)
