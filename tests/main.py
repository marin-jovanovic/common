import pathlib

from comm.comm_files import get_all_directories_from_directory


def main():
    for f in get_all_directories_from_directory(
        pathlib.Path("/home/kim/Documents/github/marin-jovanovic/ocr/source_year")
    ):
        print(f)


if __name__ == '__main__':
    main()