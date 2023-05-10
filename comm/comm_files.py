import hashlib
import os
import pathlib
import re
import shutil
import sys
from pathlib import Path

from comm.comm_root import get_root_path


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



def get_all_files_from_directory(
        folder_path,
        file_types_included,
        file_types_excluded,
        skip_folders=False,
        directories_exclude=None
):
    """
        files = get_all_files_from_directory(os.path.abspath(t), ["*"], [])
    Args:
        folder_path:
        file_types_included:
        file_types_excluded:
        skip_folders:

    temporary_directory
    Returns:
    """

    if not directories_exclude:
        directories_exclude = []

    files = set()

    files = set()

    t = pathlib.Path(folder_path).iterdir()

    if not any(t):
        return files

    for f in t:

        if f.is_dir():

            if not skip_folders:
                if f.name in directories_exclude:
                    continue

                [files.add(i) for i in
                 get_all_files_from_directory(
                     f,
                     file_types_included,
                     file_types_excluded
                 )]

        else:
            suffix = pathlib.Path(f).suffix

            if "*" not in file_types_excluded and \
                    suffix not in file_types_excluded:

                if "*" in file_types_included or suffix in file_types_included:
                    files.add(f)

    return files

def get_all_files_from_directory_simple(folder_path:pathlib.Path) -> set:
    return get_all_files_from_directory(folder_path, ["*"], [])

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

    if pathlib.Path(destination_absolute_path).is_file():
        print(
            "integrity err pathlib.Path(destination_absolute_path).is_file():")
        sys.exit()

    with open(destination_absolute_path, "w"):
        pass

    return destination_absolute_path


def check_file_exists(path: pathlib.Path):
    c = 0
    # not_exists = False

    if not os.path.isfile(path):
        print(f'[err] 1 not exist: {path}')
        # not_exists = True
        c += 1

    if not path.is_file():
        print(f'[err] 2 not exist: {path}')
        # not_exists = True
        c += 1

    # if not_exists:
    #     sys.exit(-1)
    # print(path.exists())
    #
    # with open(path, "r") as f:
    #     print(f.read())

    if c == 0:
        return True

    if c == 1:
        sys.exit(-1)

    return False


def safe_delete_directory(f):
    try:
        shutil.rmtree(f)
    except FileNotFoundError:
        raise NotImplementedError


def safe_create_directory(create_dest_dir, name, check_against):
    """check if that folder exists in @check_against"""

    c = 2

    if check_against not in os.listdir(pathlib.Path(check_against).parent):
        pass

    else:

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

    shutil.copy2(source_file, destination_folder / tmp_n)

    return destination_folder / tmp_n

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
        print("no hash")
        return

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
            # try:
            while True:

                try:
                    data = f.read(bytes_block)
                except PermissionError:
                    return -1

                if not data:
                    break

                h.update(data)
            # except Exception as e:
            #     print(e)
            #     print(f"{file=}")
            #     raise NotImplementedError

    return h.hexdigest()


def empty_directory(out_folder):
    safe_delete_directory(out_folder)
    os.makedirs(out_folder, exist_ok=True)


def safe_move_file(source_file, destination_folder, destination_name=None):
    if not destination_name:

        source_file = pathlib.Path(source_file)
        destination_folder = pathlib.Path(destination_folder)

        c = 1
        tmp_n = source_file.name

        name = source_file.stem
        suffix = source_file.suffix

        while os.path.exists(destination_folder / tmp_n):
            c += 1
            tmp_n = f"{name}_{c}{suffix}"

        shutil.move(source_file, destination_folder / tmp_n)

    else:

        source_file = pathlib.Path(source_file)
        destination_folder = pathlib.Path(destination_folder)

        c = 1
        suffix = source_file.suffix
        tmp_n = f"{destination_name}{suffix}"

        while os.path.exists(destination_folder / tmp_n):
            c += 1
            tmp_n = f"{destination_name}_{c}{suffix}"

        if not source_file.exists():
            print("source not exists")
            raise NotImplementedError

        if not destination_folder.exists():
            print("destination not exists")

            # alternative_destination = destination_folder.parent

            t = safe_move_file(
                source_file=source_file,
                destination_folder=destination_folder.parent,
                destination_name=destination_name

            )

            print(f"moved to {t=}")

            # shutil.move(source_file, alternative_destination / tmp_n)
            return

        shutil.move(source_file, destination_folder / tmp_n)

        return destination_folder / tmp_n


def get_file_count(p: pathlib.Path):
    """include subdirectories"""

    # if p.exists():

    return len(get_all_files_from_directory(p, ["*"], []))

    # else:
    #     return 0


def join_with_curr_working_dir(p):
    working_dir = pathlib.Path(__file__).parent.resolve()
    return os.path.join(working_dir, p)


def create_directory_if_not_exists(target_dir, log_name=None):
    if not log_name:
        log_name = target_dir

    if os.path.isdir(target_dir):
        print(f"[log] directory exist {log_name}")

    else:
        print(f"[log] creating directory {log_name}")
        print(f"{target_dir=}")
        target_dir = pathlib.Path(target_dir)

        try:
            Path(target_dir).mkdir(parents=True, exist_ok=True)
        except:
            # todo
            pass

    # print(f"creating \"{log_name}\" directory")
    # try:
    #     os.makedirs(path, exist_ok=False)
    # except FileExistsError:
    #     print(f"\"{log_name}\" directory already exists")
    # print()


def create_file_clear(full_path: Path) -> bool:
    """
    if file exists then clear content
    if file not exists: create it

    :param full_path:
    :return:
    """

    try:
        with open(full_path, 'r') as _:
            print(f"[log] File Exists {full_path}")

        return False

    except IOError:
        with     open(full_path, 'w+') as _:
            print(f"[log] File Created {full_path}")

        return True


def create_source_directory():
    return create_source_directory(in_root_path=config('SOURCE_PATH'))


def _create_name(prefix, prefix_count):
    return f"{prefix}_{prefix_count}"


def deconstruct_name(name):
    """works with @_create_name"""

    t = name.split('_', 1)
    return t[0], int(t[1])


def create_temporary_directory(root_path, prefix='default'):
    """
    in @root_path put all @prefix dirs
    contains subdirectories with maximum capacity
    when capacity is full then creates another directory

    :return:
    """

    #
    # def create_in_root(in_root_path):
    #     working_dir = get_root_path()
    #     full_path = working_dir / in_root_path
    #     create_directory_if_not_exists(target_dir=full_path)
    #     return full_path
    #

    # temporary_root_path = create_in_root(in_root_path=root_path)
    create_directory_if_not_exists(root_path)
    temporary_root_path = root_path

    prefix_count = 0

    max_files_per_dir = 100

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

    first_dir = _create_name(temporary_root_path / prefix, prefix_count)

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

    total_file_count = len(get_all_files_from_directory(
        folder_path=max_dir,
        file_types_included=['*'],
        file_types_excluded=[],
        skip_folders=True
    ))

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
        print('max')

        prefix, prefix_count = deconstruct_name(max_dir.name)

        to_create = temporary_root_path / _create_name(prefix, prefix_count + 1)

        create_directory_if_not_exists(to_create)

        return to_create

    elif total_file_count > max_files_per_dir:
        print('integrity error')
        print('todo perform restructuring (auto)')
        sys.exit(-1)

    else:
        print('can create in this directory')

        return max_dir


from bisect import insort


def get_max_dir_path(
        directory: pathlib.Path, prefix: str,
        flag_global_or_continous=True) -> pathlib.Path:
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

    :param prefix:
    :return:
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

    directory_as_str = "products_id"
    directory = os.fsencode(directory_as_str)
    s = 0
    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        full_path = os.path.join(directory_as_str, filename)
        with open(full_path, "r") as f:
            str_content = f.read()

        c = len(str_content.split("\n"))
        print(c)
        s += c - 1

    print("sum", s)


def get_all_subdirs(folder_path):
    files = set()

    for f in os.listdir(folder_path):
        f_path = os.path.join(os.path.abspath(folder_path), f)

        if not os.path.isfile(f_path):
            files.add(pathlib.Path(f_path))

    return files
