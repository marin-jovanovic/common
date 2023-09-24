import pathlib

from comm.comm_files import get_all_files_from_directory, RegexElements


def main():

    t = pathlib.Path()
    raise NotImplementedError

    for i in get_all_files_from_directory(
        directory_path=t,
        file_types_excluded=[],
        file_types_included=[RegexElements.ALL]
    ):
        print(i)

    print(f"{RegexElements.ALL}")

if __name__ == '__main__':
    main()