import re


def extract_indicators(file_path):
    with open(file_path, "rb") as file:
        data = file.read()

    text = data.decode("utf-8", errors="ignore")

    urls = re.findall(
        r"https?://[^\s\"'<>]+",
        text)

    ip_addresses = re.findall(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        text)

    return {
        "urls": urls,
        "ip_addresses": ip_addresses
    }
