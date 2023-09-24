from datetime import datetime


def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def get_datetime_printable():
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


def get_datetime_safe():
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    return dt_string


def main():
    print(get_datetime_printable())
    print(get_datetime_safe())


if __name__ == '__main__':
    main()
