import pathlib
from typing import Dict

from src_py.comm_wrapper.comm_root import get_root_path


def deconstruct_path(
        p: pathlib.Path,
        root=get_root_path()
) -> Dict:
    """
    in case @p is relative to @root
        return {
            'flag_relative_or_absolute': True,
            'path': [root, relative_path]
        }
    else
        return {
            'flag_relative_or_absolute': False,
            'path': [p]
        }
    """

    if root in p.parents:
        """contained in this git repository / project"""

        relative_path = p.relative_to(root)

        return {
            'flag_relative_or_absolute': True,
            'path': [root, relative_path]
        }

    else:
        """must be absolute"""

        return {
            'flag_relative_or_absolute': False,
            'path': [p]
        }


def main():
    print(deconstruct_path(
        pathlib.Path('/src_py/comm/comm_path.py')
    ))

    # print(root in p.parents)
    #
    # print(p.relative_to(root))


if __name__ == '__main__':
    main()
