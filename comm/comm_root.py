from pathlib import Path


def get_root_path():
    # do not call it from here
    raise NotImplementedError
    return Path(__file__).resolve().parent.parent


if __name__ == '__main__':
    print(f"{get_root_path()=}")
