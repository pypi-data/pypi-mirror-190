class CJsonStructures:
    def __init__(self, json_value = []):
        self.index_by_struct = {}
        self.structs_by_index = []
        if type(json_value) == dict:
            json_value = [x[1] for x in sorted((int(k), v) for k, v in json_value.items())]
        for struct in json_value:
            self.add_struct(tuple(struct))

    def make_struct_from_dict(self, dict_obj):
        return tuple(sorted(str(e) for e in dict_obj))

    def add_struct(self, struct):
        if struct not in self.index_by_struct:
            self.index_by_struct[struct] = len(self.structs_by_index)
            self.structs_by_index.append(struct)

    def add_struct_from_dict(self, dict_obj):
        struct = self.make_struct_from_dict(dict_obj)
        self.add_struct(struct)

    def join(self, other):
        for struct in other.index_by_struct:
            self.add_struct(struct)

    def get_struct_from_id(self, id):
        struct = self.structs_by_index[id]
        return struct
    
    def to_json_array(self):
        return self.structs_by_index


def get_structures(obj):
    structures = CJsonStructures()
    children = []

    if type(obj) == list:
        children = obj
    elif type(obj) == dict and obj != {}:
        structures.add_struct_from_dict(obj)
        children = obj.values()
    
    for child in children:
        new_structures = get_structures(child)
        structures.join(new_structures)
    
    return structures

