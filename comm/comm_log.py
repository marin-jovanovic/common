from datetime import datetime

from src_py.config.loader import get_configuration_controller, \
    get_configuration_controller_file_path

from comm.comm_files import create_dirs, safe_create_file
from comm.comm_json import update_json_file
from comm.comm_root import get_root_path


def get_log_path():
    # todo extract to separate config file

    global_config = get_configuration_controller()

    default_config = {
        'relativeLogFolder': 'resources/log',
        "constructableLogFile": 'log.txt',
    }

    for k, v in default_config.items():
        if k not in global_config:
            global_config[k] = v

    update_json_file(get_configuration_controller_file_path(), global_config)

    root = get_root_path()

    relative_log_folder = global_config['relativeLogFolder']
    create_dirs([root / relative_log_folder])

    absolute_log_folder = root / relative_log_folder
    constructable_log_file = global_config['constructableLogFile']

    out_log_file = safe_create_file(constructable_log_file, absolute_log_folder)

    return out_log_file


class Log:

    def __init__(self):
        self.generation_id = 0
        self.entry_id = 0
        self.root = get_root_path()

        self.log_file = get_log_path()

    def append(self, *payload):
        formatted_payload = " ".join([str(i) for i in payload])

        # dd/mm/YY H:M:S
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        newline_separator = "\n"

        with open(self.log_file, "a") as f:
            f.write(
                f"{self.generation_id};"
                f"{self.entry_id};"
                f"{dt_string};"
                f"{formatted_payload}"
                f"{newline_separator}"
            )

        self.entry_id += 1


def print_err(*payload):
    formatted_payload = " ".join([str(i) for i in payload])
    print(f'[err] {formatted_payload}')


LOG = Log()


def main():
    log = Log()

    log.append(1)
    log.append(1, 2)
    log.append(1, 2, 3)


if __name__ == '__main__':
    main()
