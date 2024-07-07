import sys
import urllib.request

from urllib.request import Request


def extract_from_dom(dom, element, attribute):
    extracted_value = []
    for ind in dom.find(element, ('class', attribute)):
        ext_single_val = ind.text()
        extracted_value.append(ext_single_val)

    return extracted_value


def scrape_page(url, headers=None):
    req = Request(url)

    if headers:
        for k, v in headers.items():
            req.add_header(k, v)

    # try:

    # todo handle urllib.error.HTTPError: HTTP Error 404: Not Found
    with urllib.request.urlopen(req) as fp:
        str_content = fp.read().decode("utf8")

    # except urllib.error.:

    if not str_content:
        sys.exit(-1)

    return str_content
