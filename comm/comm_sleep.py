import random
import time


def sleep_random_sec():
    duration = random.uniform(2, 5)
    time.sleep(duration)


if __name__ == '__main__':
    from collections import defaultdict

    d = defaultdict(int)
    for i in range(999999):
        t = int(random.uniform(2, 5))
        d[t] += 1
    for i in d.items():
        print(i)
