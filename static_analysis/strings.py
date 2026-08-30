import re


def extract_strings(file_path, min_length=4):
    with open(file_path, "rb") as file:
        data = file.read()

    strings = re.findall(
        rb"[\x20-\x7E]{%d,}" % min_length,
        data
    )

    return [
        string.decode("ascii", errors="ignore")
        for string in strings
    ]
