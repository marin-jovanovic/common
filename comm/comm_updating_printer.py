from comm.comm_time import get_time


class Updater:

    def get_ladders(self, current_percentage):
        return int(
            current_percentage / self.percentage_increment
        )

    def get_percentage(self, current_progress):
        if self.total == 0:
            return 100

        return int(current_progress / self.total * 100)

    def __init__(self, total, percentage_increment, current_progress):
        self.total = total
        self.percentage_increment = percentage_increment

        self.current_progress = current_progress
        self.current_percentage = self.get_percentage(self.current_progress)
        self.current_total_ladders = self.get_ladders(self.current_percentage)

        self.max_ladders = int(100 / self.percentage_increment)

        self.max_printed = False

        true_ratio = f"({self.current_progress} / {self.total})"
        current_time = get_time()
        string_builder = "[" + self.current_total_ladders * "#" + (
                self.max_ladders - self.current_total_ladders) * " " + \
                         f"] {self.current_percentage}% {true_ratio} " \
                         f"{current_time=} (start)"

        print(string_builder)

    def update(self, new_increment=1):
        previous_total_ladders = self.current_total_ladders

        self.current_progress += new_increment
        self.current_percentage = self.get_percentage(self.current_progress)
        self.current_total_ladders = self.get_ladders(self.current_percentage)

        true_ratio = f"({self.current_progress} / {self.total})"

        current_time = get_time()

        if self.current_progress == self.total and not self.max_printed:
            string_builder = "[" + self.max_ladders * "#" + "]" + (
                    self.current_total_ladders - self.max_ladders) * "#" + \
                             f" {self.current_percentage}%"
            print(string_builder + f" {true_ratio} done! {current_time=}")
            self.max_printed = True

        elif self.current_total_ladders > self.max_ladders or (
                self.current_progress > self.total):

            string_builder = "[" + self.max_ladders * "#" + "]" + (
                    self.current_total_ladders - self.max_ladders) * "#" + \
                             f" {self.current_progress / self.total * 100}%"
            print(string_builder + f" {true_ratio} overflow! {current_time=}")

        elif self.current_total_ladders > previous_total_ladders:

            string_builder = "[" + self.current_total_ladders * "#" + (
                    self.max_ladders - self.current_total_ladders) * " " + \
                             f"] {self.current_percentage}% {true_ratio} " \
                             f"{current_time=}"
            print(string_builder)


def main():
    """
    ..... .....   %0
    #....         %10
    [##### #####] %20
    """

    total = 100
    current = 28

    updater = Updater(total=total, current_progress=current,
                      percentage_increment=10)

    for i in range(20):
        updater.update(5)
    print()

    return

    total = 200
    updater = Updater(total=total, current_progress=0,
                      percentage_increment=10)

    for i in range(total):
        updater.update(1)
    print()

    total = 200
    updater = Updater(total=total, current_progress=0,
                      percentage_increment=20)

    for i in range(total):
        updater.update(1)
    print()

    total = 200
    updater = Updater(total=total, current_progress=0,
                      percentage_increment=9)

    for i in range(total):
        updater.update(1)
    print()

    total = 200
    updater = Updater(total=total, current_progress=0,
                      percentage_increment=3)

    for i in range(int(total * 10 / 4) + 15):
        updater.update(0.4)
    print()


if __name__ == '__main__':
    main()
