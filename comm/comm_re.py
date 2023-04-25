import re


def extract_with_regex(regex_list, input):
    for regex in regex_list:

        pattern = re.compile(regex)
        tmp = pattern.match(input)

        if tmp:
            return tmp.groups()

    return None
