from typing import get_type_hints
from .parse_hint import parse_alias, Alias


class Jsonable:

    def to_json(self) -> dict:
        res = {}
        annotations = get_type_hints(self.__class__)
        for var_name, var_type in annotations.items():
            var_value = getattr(self, var_name, None)
            if var_value is None:
                res.update({var_name:var_value})
                continue
            
            res.update({var_name:to_json(var_value, var_type)})

        return res

    def __repr__(self) -> str:
        return repr(self.to_json())

    @classmethod
    def load_from_json(cls, json_obj:dict):
        
        ins = object.__new__(cls)
        annotations = get_type_hints(cls)
        for var_name, var_type in annotations.items():
            var_value = json_obj.get(var_name)
            if var_value is None:
                setattr(ins, var_name, None)
                continue

            setattr(ins, var_name, load_type(var_value, var_type))
        return ins


def load_type(data, _type):

    def raise_error(input_type, expect_type, actually_type):
        raise TypeError(f"{input_type} expect data type to be {expect_type}, "
                        f"actually type {actually_type}")


    if isinstance(_type, Alias):
        s_type, args = parse_alias(_type)
        if not isinstance(data, s_type):
            raise_error(_type, s_type, type(data)) 
        if s_type is list:
            return [
                load_type(d, args[0])
                for d in data
            ]
        if s_type is dict:
            return {
                k:load_type(v, args[1])
                for k,v in data.items()
            }
        
        raise TypeError("Alias only support Dict and List!")

    elif issubclass(_type, Jsonable):
        if not isinstance(data, dict):
            raise_error(_type, dict, type(data))
        return _type.load_from_json(data)

    else:
        if not isinstance(data, _type):
            raise_error(_type, _type, type(data))
        return data


def to_json(data, _type):
    if isinstance(_type, Alias):
        s_type, args = parse_alias(_type)
        if s_type is list:
            return [
                to_json(d, args[0])
                for d in data
            ]
        if s_type is dict:
            return {
                k:to_json(v, args[1])
                for k,v in data.items()
            }
        
        raise TypeError("Alias only support Dict and List!")    
    elif issubclass(_type, Jsonable):
        return data.to_json()

    else:
        return data    