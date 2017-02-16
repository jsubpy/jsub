import pytest

from jsub.config.update import update
from jsub.config.error  import UnknownUpdateMethodError

str1 = 'str1'
str2 = 'str2'

list1 = [1, 2, 'aa']
list2 = [3, 4, 'bb']

dict1 = {
    'a': 1,
    'b': 2,
    'c': {'m': 13, 'n': 14},
    'd': 4,
}
dict2 = {
    'b': 22,
    'c': {'n': {'x': 24, 'y': 25}, 'o': 115},
    'd': 4,
    'e': 5,
}
dict3 = {
    'c': 3,
    'e': 5,
}
dict4 = {
    'b': 222,
    'c': {'n': {'y': 125, 'z': 126}},
    'e': 55,
}

dict101 = {
    'a': 1,
    'b': 22,
    'c': {'n': {'x': 24, 'y': 25}, 'o': 115},
    'd': 4,
    'e': 5,
}
dict102 = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
}
dict103 = {
    'a': 1,
    'b': 22,
    'c': {'m': 13, 'n': {'x': 24, 'y': 25}, 'o': 115},
    'd': 4,
    'e': 5,
}
dict104 = {
    'b': 222,
    'c': {'n': {'y': 125, 'z': 126}, 'o': 115},
    'd': 4,
    'e': 55,
}
dict105 = {
    'b': 222,
    'c': {'n': {'x': 24, 'y': 125, 'z': 126}, 'o': 115},
    'd': 4,
    'e': 55,
}
dict106 = {
    'b': 222,
    'c': {'n': {'y': 125, 'z': 126}},
    'e': 55,
}


def test_update_unknown():
    with pytest.raises(UnknownUpdateMethodError):
        update(str1, list1, 'UNKNOWN')

def test_update_replace():
    assert update(str1, list1, 'REPLACE') == list1
    assert update(dict1, dict2, 'RePlAcE') == dict2

def test_update_list_merge():
    assert update(str1, str2, 'list_merge') == ['str1', 'str2']
    assert update(str1, list1, 'list-merge') == ['str1', 1, 2, 'aa']
    assert update(list2, str2, 'list-MERGE') == [3, 4, 'bb', 'str2']
    assert update(list1, list2, 'LIST-MERGE') == [1, 2, 'aa', 3, 4, 'bb']

def test_update_dict_merge_level1():
    assert update(dict1, dict2, 'dict-MERGE_level1') == dict101
    assert update(dict1, dict3, 'dict_merge-LEVEL1') == dict102
    assert update(dict3, dict4, 'dict_merge-LEVEL1') == dict106

def test_update_dict_merge_level2():
    assert update(dict1, dict2, 'dict_merge_level2') == dict103
    assert update(dict1, dict3, 'dict_merge-LEVEL2') == dict102
    assert update(dict2, dict4, 'dict_merge_level2') == dict104
    assert update(dict3, dict4, 'dict_merge-LEVEL2') == dict106

def test_update_dict_merge_recursive():
    assert update(dict1, dict2, 'dict_merge_recursive') == dict103
    assert update(dict1, dict3, 'dict_merge-recursive') == dict102
    assert update(dict2, dict4, 'dict_merge_recursive') == dict105
    assert update(dict3, dict4, 'dict_merge-recursive') == dict106
