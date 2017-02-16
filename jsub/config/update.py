import copy

from jsub.config.error import UnknownUpdateMethodError

def update_replace(origin, new):
    return copy.deepcopy(new)

def update_list_merge(origin, new):
    origin_temp = copy.deepcopy(origin)
    origin_list = origin_temp if isinstance(origin_temp, list) else [origin_temp]
    new_temp = copy.deepcopy(new)
    new_list = new_temp if isinstance(new_temp, list) else [new_temp]
    return origin_list + new_list

def update_dict_merge_level1(origin, new):
    final_dict = copy.deepcopy(origin)
    final_dict.update(new)
    return final_dict

def update_dict_merge_level2(origin, new):
    final_dict = copy.deepcopy(origin)
    for k, v in new.items():
        if isinstance(v, dict) and k in final_dict and isinstance(final_dict[k], dict):
            final_dict[k].update(v)
        else:
            final_dict[k] = v
    return final_dict

def update_dict_merge_recursive(origin, new):
    final_dict = copy.deepcopy(origin)
    for k, v in new.items():
        if isinstance(v, dict) and k in final_dict and isinstance(final_dict[k], dict):
            r = update_dict_merge_recursive(final_dict.get(k, {}), v)
            final_dict[k] = r
        else:
            final_dict[k] = v
    return final_dict


def update(origin, new, method):
    method_func = 'update_' + method.lower().replace('-', '_')
    if method_func not in globals() or not callable(globals()[method_func]):
        raise UnknownUpdateMethodError('Unknown update method: %s' % method)
    return globals()[method_func](origin, new)
