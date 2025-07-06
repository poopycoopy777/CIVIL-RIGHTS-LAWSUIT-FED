import re
from pathlib import Path
from typing import List


def extract_ips(log_text: str) -> List[str]:
    """Extract all IPv4 addresses from the given log text."""
    ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    return re.findall(ip_pattern, log_text)


def parse_log_file(path: Path) -> List[str]:
    """Read a log file and return all IP addresses found."""
    text = path.read_text(errors="ignore")
    return extract_ips(text)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract IP addresses from a log file")
    parser.add_argument("logfile", type=Path)
    args = parser.parse_args()

    ips = parse_log_file(args.logfile)
    for ip in ips:
        print(ip)
