import bisect
import hashlib
import os
import pathlib
import re
import shutil
import sys
from bisect import insort
from collections import defaultdict
from pathlib import Path

from comm.comm_root import get_root_path


def get_file_hash(
        file, bytes_block, algorithm, choice_first_block_or_whole=True):
    """
                        hash_ = get_file_hash(file=file, bytes_block=65536,
                                          algorithm="md5",
                                          choice_first_block_or_whole=True)

                                          if permission error, return -1
    """

    assert os.path.isfile(file), f"{file}"
    assert pathlib.Path(file).is_file(), f"{file}"

    if algorithm not in ["md5", "sha1"]:
        raise NotImplementedError

    h = None

    if algorithm == "md5":
        h = hashlib.md5()

    elif algorithm == "sha1":
        h = hashlib.sha1()

    with open(file, 'rb') as f:

        if choice_first_block_or_whole:
            try:

                data = f.read(bytes_block)
            except PermissionError:
                return -1

            h.update(data)

        else:
            while True:

                try:
                    data = f.read(bytes_block)
                except PermissionError:
                    return -1

                if not data:
                    break

                h.update(data)

    return h.hexdigest()


def get_extension_dotted(p: pathlib.Path):
    return p.suffix


def get_extension_undotted(p: pathlib.Path):
    return get_extension_dotted(p)[1:]


def get_extension_undotted_normalized(p: pathlib.Path):
    """
    p.suffix[1:].lower()
    :param p:
    :return:
    """
    return get_extension_undotted(p).lower()


def get_all_existing_extension_undotted(files: list) -> set:
    """return undotted set of existing extension (from list of @files)"""

    return {get_extension_undotted_normalized(p) for p in files}


def get_size(p: pathlib.Path):
    return os.path.getsize(p)


def get_sha1_small(p: pathlib.Path):
    """small portion of file, first 65536 bytes"""

    return get_file_hash(
        file=p,
        bytes_block=65536,
        algorithm="sha1",
        choice_first_block_or_whole=True
    )


def get_extension_counts(source_folder):
    pre_source_cnt = defaultdict(int)
    for f in get_all_files_from_directory(source_folder, [RegexElements.ALL], []):
        pre_source_cnt[get_extension_undotted_normalized(f)] += 1

    return pre_source_cnt


def get_md5_big(p: pathlib.Path):
    return get_file_hash(
        file=p,
        bytes_block=65536,
        algorithm="md5",
        choice_first_block_or_whole=False
    )


def create_nested_directory(p: pathlib.Path):
    """

    return bool: directory already exists?
    """

    # if not p.is_dir():
    #     print(f"not directory {p=}")
    #     raise NotImplementedError

    if p.exists():
        return True

    p.mkdir(parents=True, exist_ok=False)
    return False


def get_file_content(p: pathlib.Path) -> str:
    with open(p, "r") as f:
        return f.read()


def unsafe_write_to_file(path: pathlib.Path, content: str):
    with open(path, "w") as f:
        f.write(content)


def create_dirs(dirs: list):
    """
    create directory if not exists
    """

    for i in dirs:
        if not os.path.exists(i):
            print('trying to create', i)
            os.makedirs(i)


def get_all_directories_from_directory(target_directory: pathlib.Path):
    r = []
    for f in os.listdir(target_directory):

        f_path = target_directory / f

        if f_path.is_dir():
            r.append(f_path)

    return r


def copy_directory_content(
        destination_directory_path: pathlib.Path,
        source_directory_path: pathlib.Path,
        to_skip=None,
        copy_empty_directories=False
):
    """
        preserve tree structure
        by default does not copy empty directories
    """

    if to_skip is None:
        to_skip = []

    directories_to_skip = [i for i in to_skip if i.is_dir()]
    files_to_skip = [i for i in to_skip if i.is_file()]

    all_files = get_all_files_from_directory_simple(
        folder_path=source_directory_path
    )

    files_relative_to_source_directory_path = []
    for i in all_files:

        if i in files_to_skip:
            continue

        t = any(i.is_relative_to(j) for j in directories_to_skip)
        if t:
            continue

        files_relative_to_source_directory_path.append(
            i.relative_to(source_directory_path)
        )

    for i in files_relative_to_source_directory_path:

        this_destination = destination_directory_path

        if i.parent:
            this_destination = destination_directory_path / i.parent

            create_directory_if_not_exists(this_destination)

        safe_copy_file(
            source_file=source_directory_path / i,
            destination_folder=this_destination
        )


from enum import Enum

class RegexElements(Enum):
    ALL = "*"


def get_all_files_from_directory(
    directory_path: pathlib.Path,
    file_types_included: list,
    file_types_excluded: list,
    skip_directories=False,
    excluded_directories=None
):
    """
        files = get_all_files_from_directory(os.path.abspath(t), [], [])
    Args:
        directory_path:
        file_types_included:
        file_types_excluded:
        skip_directories:

    temporary_directory
    Returns:
    """

    if not excluded_directories:
        excluded_directories = []

    files = []

    dir_sub_obj = [i for i in directory_path.iterdir()]

    if not any(dir_sub_obj):
        return files

    for f in dir_sub_obj:

        if f.is_dir() and not skip_directories:
            if f.name in excluded_directories:
                continue

            for i in get_all_files_from_directory(
                f,
                file_types_included,
                file_types_excluded
            ):
                bisect.insort(files, i)

        elif not f.is_dir():
            suffix = pathlib.Path(f).suffix

            if RegexElements.ALL not in file_types_excluded and \
                    suffix not in file_types_excluded:

                if RegexElements.ALL in file_types_included or suffix in file_types_included:
                    bisect.insort(files, f)

    # if len(files) == 0:
    #     # possible if dir is empty
    #     raise NotImplementedError

    return files




def get_all_files_from_directory_simple(folder_path: pathlib.Path) -> set:
    return get_all_files_from_directory(folder_path, [RegexElements.ALL], [])


def unsafe_create_file(full_path: pathlib.Path):
    """
    test if file or directory

    if exists
        if file
            return

        if directory
            create file with different name (safely)
            return

    else
        # tests for file and directory are not performing as expected, must make assumptions
        # assumption: argument that is provided expects to have /../filename as a file


    todo rename
    just create file, no checking if name exists
    if you want that behaviour check safe_create_file
    """

    is_directory = full_path.is_dir()

    is_file = full_path.is_file()

    if full_path.exists():
        if is_file == is_directory:
            print('logical err  (is_file == is_directory)')
            raise NotImplementedError

        if is_directory:
            """need to create file with new name"""
            dir_with_same_name_exists = safe_create_file(full_path.name,
                                                         full_path.parent)
            print(f'{dir_with_same_name_exists=}')
            return dir_with_same_name_exists

        else:
            # assumption: it is file
            return full_path

    else:

        # if is_directory:
        #
        #     print('logical error, you must pass file')
        #     sys.exit(-1)

        # if not full_path.exists() and is_file:
        """create file"""
        parent = full_path.parent

        create_dirs([parent])

        """should return @full_path because we tested that this path does not exist"""
        return safe_create_file(full_path.name, full_path.parent)


def safe_create_file(filename, destination_folder):
    """
    generate with new name
    Args:
        filename: file name + file suffix
        destination_folder:

    Returns:

    """

    create_nested_directory(destination_folder)

    filename = pathlib.Path(filename)
    destination_folder = pathlib.Path(destination_folder).absolute()

    c = 1
    tmp_n = filename.name

    name = filename.stem
    suffix = filename.suffix

    while os.path.exists(destination_folder / tmp_n):
        c += 1
        tmp_n = f"{name}_{c}{suffix}"

    destination_absolute_path = destination_folder / tmp_n

    if destination_absolute_path.is_file():
        print("integrity err destination_absolute_path.is_file()")
        sys.exit()

    with open(destination_absolute_path, "w"):
        pass

    return destination_absolute_path


def check_file_exists(path: pathlib.Path):
    assert os.path.isfile(path) == path.is_file()

    # Check if the path exists and it's either a file or a directory
    if path.exists() and (path.is_file() or path.is_dir()):
        print(1, True)
        return True
    else:
        # If the path doesn't exist, check if a file without extension exists
        file_without_extension = path.with_suffix('')
        if file_without_extension.exists() and file_without_extension.is_file():
            return True
        else:
            return False

    if os.path.isfile(path) and path.is_file() and os.path.exists(path):
        return True

    elif not os.path.isfile(path) and not path.is_file() and not os.path.exists(
            path):
        return False

    else:
        print(f"{os.path.isfile(path)=}")
        print(f"{path.is_file()=}")
        print(f"{os.path.exists(path)=}")

        raise NotImplementedError


def safe_delete_directory(f):
    try:
        shutil.rmtree(f)
    except FileNotFoundError:
        raise NotImplementedError


def safe_create_directory(
        create_dest_dir: pathlib.Path,
        name: str,
        check_against: pathlib.Path
):
    """
    @create_dest_dir directory in which should directory with name @name placed

    check if that folder exists in @check_against
    """

    c = 2

    if name in os.listdir(check_against):

        while (name + "_" + str(c)) in os.listdir(check_against):
            c += 1

        name = name + "_" + str(c)

    os.makedirs(create_dest_dir / name, exist_ok=True)
    return create_dest_dir / name


def safe_copy_file(source_file, destination_folder):
    source_file = pathlib.Path(source_file)
    destination_folder = pathlib.Path(destination_folder)

    c = 1
    tmp_n = source_file.name

    name = source_file.stem
    suffix = source_file.suffix

    while os.path.exists(destination_folder / tmp_n):
        c += 1
        tmp_n = f"{name}_{c}{suffix}"

    shutil.copy2(source_file, destination_folder / tmp_n, follow_symlinks=False)

    return destination_folder / tmp_n


def empty_directory(out_folder):
    safe_delete_directory(out_folder)
    os.makedirs(out_folder, exist_ok=True)


def get_dotted_suffix(p: pathlib.Path):
    return p.suffix


def safe_move_file(
        source_file: pathlib.Path,
        destination_folder: pathlib.Path,
        destination_name=None
):
    if not isinstance(source_file, pathlib.Path):
        print(source_file)
        raise NotImplementedError

    if not isinstance(destination_folder, pathlib.Path):
        print(destination_folder)
        raise NotImplementedError

    if not check_file_exists(source_file):
        print(source_file)
        raise NotImplementedError

    if not destination_folder.exists():
        print("destination not exists")

        create_nested_directory(destination_folder)

    c = 1

    dotted_suffix = get_dotted_suffix(source_file)

    if not destination_name:
        destination_name = source_file.stem

    tmp_n = f"{destination_name}{dotted_suffix}"

    while check_file_exists(destination_folder / tmp_n):
        c += 1
        tmp_n = f"{destination_name}_{c}{dotted_suffix}"

    p = destination_folder / tmp_n

    shutil.move(source_file, p)

    return p


def get_file_count(p: pathlib.Path):
    """include subdirectories"""

    return len(get_all_files_from_directory(p, [RegexElements.ALL], []))


def join_with_curr_working_dir(p):
    working_dir = pathlib.Path(__file__).parent.resolve()
    return os.path.join(working_dir, p)


def create_directory_if_not_exists(target_dir: pathlib.Path):
    """
    create directory if not exists

    if exists pass
    creates parent directories if not exists


    """

    target_dir.mkdir(parents=True, exist_ok=True)


def create_file_clear(full_path: Path) -> bool:
    """
    if file exists then clear content
    if file not exists: create it

    :param full_path:
    :return:
    """

    try:
        with open(full_path, 'r') as _:
            # print(f"[log] File Exists {full_path}")
            pass
        return False

    except IOError:
        with     open(full_path, 'w+') as _:
            pass
            # print(f"[log] File Created {full_path}")

        return True


def create_source_directory():
    raise NotImplementedError
    # return create_source_directory(in_root_path=config('SOURCE_PATH'))


def _create_name(prefix, prefix_count):
    return f"{prefix}_{prefix_count}"


def deconstruct_name(name):
    """works with @_create_name"""

    t = name.rsplit('_', 1)
    return t[0], int(t[1])


def create_file_in_temporary_directory(
        file_template_name: str,
        temporary_directory_path: pathlib.Path,
        subdirectory_prefix: str,
        max_files_per_subdirectory=100
):
    temporary_directory = create_temporary_directory(
        root_path=temporary_directory_path,
        prefix=subdirectory_prefix,
        max_files_per_dir=max_files_per_subdirectory
    )

    f = safe_create_file(
        filename=file_template_name,
        destination_folder=temporary_directory,
    )

    return f


def create_temporary_directory(
        root_path,
        prefix='default',
        max_files_per_dir=100
):
    """
    in @root_path put all @prefix dirs
    contains subdirectories with maximum capacity
    when capacity is full then creates another directory

    :return:
    """

    # create_directory_if_not_exists(root_path)
    temporary_root_path = root_path

    prefix_count = 0

    # todo flag for this
    max_dirs_per_dir = 3
    """
    root
        dir1
            f1
            f2
        dir2
            f1
            f2

    root
        dir1
            dir1
                f1
                f2
            dir2
                f1
                f2
        dir2
            dir1
                f1
                f2
            dir2
                f1
                f2


    """

    first_dir = temporary_root_path / _create_name(prefix, prefix_count)

    create_directory_if_not_exists(first_dir)

    """
    assumption: zero dir exists

    check if is full
    """

    max_dir = get_max_dir_path(
        directory=temporary_root_path,
        prefix=prefix,
        flag_global_or_continous=True
    )

    total_file_count = get_file_count(max_dir)

    # todo not working as expected,
    """
    todo we need 3 types
        1.
            create file if not exists
            if exists clear content
        2.
            create file if not exists
            if exists raise exception
        3.
            check for name 
            if name exists create with new name

        todo check if this logic is ok
    """

    if total_file_count == max_files_per_dir:

        prefix, prefix_count = deconstruct_name(max_dir.name)

        to_create = temporary_root_path / _create_name(prefix, prefix_count + 1)

        create_directory_if_not_exists(to_create)

        return to_create

    elif total_file_count > max_files_per_dir:
        sys.exit(-1)

    else:

        return max_dir


def get_max_dir_path(
        directory: pathlib.Path,
        prefix: str,
        flag_global_or_continous=True
) -> pathlib.Path:
    """
    assume that prefix = /dir1/dir2/base_

    and file structure looks like this

    /dir1
        /dir2
            /base_0
            /base_1
            /tmp_2
            /base_4

    will return /dir1/dir2/base_1

    todo check if you want to return base_4 or base_1

    we want to return base_4, not handled yet

    """

    connector = '_'

    directories = get_all_directories_from_directory(target_directory=directory)
    regex = f'{prefix}{connector}(\d+)'
    pattern = re.compile(regex)

    existing_suffixes = []

    for i in directories:

        tmp = pattern.match(i.stem)

        if tmp:
            insort(existing_suffixes, int(tmp.group(1)))

    max_global = existing_suffixes[-1]
    max_continuous = -1
    for i in existing_suffixes:
        if i == max_continuous + 1:
            max_continuous = i

    if flag_global_or_continous:
        return directory / _create_name(prefix, max_global)
    else:
        return directory / _create_name(prefix, max_continuous)


def create_in_root(in_root_path):
    working_dir = get_root_path()
    full_path = working_dir / in_root_path
    create_directory_if_not_exists(target_dir=full_path)
    return full_path


def get_row_count():
    '''


    assumption
        provided directory is full path
        no nesting in provided directory

    :return: sum of number of lines for each file in provided directory
    '''
    raise NotImplementedError
    directory_as_str = "products_id"
    directory = os.fsencode(directory_as_str)
    s = 0
    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        full_path = os.path.join(directory_as_str, filename)
        with open(full_path, "r") as f:
            str_content = f.read()

        c = len(str_content.split("\n"))
        s += c - 1

    return s


def get_all_subdirs(folder_path):
    """
    only look at level 1, do not go into sub-subdirectories
    :param folder_path:
    :return:
    """

    files = set()

    for f in os.listdir(folder_path):
        f_path = os.path.join(os.path.abspath(folder_path), f)

        if not os.path.isfile(f_path):
            files.add(pathlib.Path(f_path))

    return files
