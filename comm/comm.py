from collections import defaultdict


def to_snake_case(i):
    return '_'.join(i.split())


def to_camel_case(i: str):
    i = i.replace(":", "").replace("-", "")

    return ''.join([str(i).capitalize() for i in i.split()])


def safe_append(di: dict, where, content):
    if where in di:
        if content not in di[where]:
            di[where].append(content)
    else:
        di[where] = [content]


def reverse_flatten_dict(in_dict):
    """
    "a": ["1"],
    "b": ["1"],

    ->

    "1": ["a", "b"]
    """

    out_dict = defaultdict(list)

    for k, v in in_dict.items():
        for i in v:
            out_dict[i].append(k)

    return out_dict


def replace_cro(i: str) -> str:
    """
    replace croatian letters with international
    """

    c = 'čćžšđČĆŽŠĐ'
    e = 'cczsdCCZSD'

    t = dict(zip(list(c), list(e)))

    for cro, eng in t.items():
        i = i.replace(cro, eng)

    return i
