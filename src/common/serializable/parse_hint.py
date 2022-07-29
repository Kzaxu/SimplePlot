from typing import List, get_origin, get_args
Alias = type(List)


def parse_alias(alias:Alias):

    cls = get_origin(alias)
    args = get_args(alias)

    if cls is list:
        if len(args) != 1:
            raise TypeError("num of List args can only be 1")
        return list, args
    elif cls is dict:
        if len(args) != 2:
            raise TypeError("num of Dict args can only be 2")
        return dict, args        
    else:
        raise TypeError("only support Dict or List alias")

