import json
import pathlib
# from py.comm.comm_log import LOG
from collections import defaultdict

from comm.comm_files import check_file_exists
from comm.comm_files import create_directory_if_not_exists


def defaultdict_to_dict(d: defaultdict):
    return {k: v for k, v in d.items()}


def merge_dict_int(pre_source_cnt, pre_staging_cnt):
    pre_cnt = defaultdict(int)
    for k, v in pre_source_cnt.items():
        pre_cnt[k] += v
    for k, v in pre_staging_cnt.items():
        pre_cnt[k] += v
    return pre_cnt


def update_json_file(path, new_content):
    """append @new_content to json at @path"""

    content = load_json(path)

    for k, v in new_content.items():
        content[k] = v

    write_json(path, content)


def load_json(json_file: pathlib.Path):
    if not check_file_exists(json_file):
        raise NotImplementedError

    with open(json_file, encoding="utf-8") as f:

        if json_file.stat().st_size == 0:
            return json.loads("{}")

        return json.loads(f.read())


def write_json(destination: pathlib.Path, content_as_dict: object):
    """assumes that it is checked that it writes to correct file"""

    if not destination.parent.exists():
        create_directory_if_not_exists(destination.parent)

    with open(destination, 'w+', encoding='utf8') as json_file:
        json.dump(content_as_dict, json_file, indent=4, ensure_ascii=False)


def unsafe_init_empty_json_file(destination):
    """assumes that it is checked that it writes to correct file
    init or clear
    """

    with open(destination, 'w+', encoding='utf8') as json_file:
        json.dump({}, json_file, indent=4, ensure_ascii=False)
