#!/usr/bin/env python
from contextlib import suppress
import re
from typing import Dict, List

import plugins
import requests


class Plugin(plugins.BasePlugin):
    __name__ = "vb5version"

    def __init__(self, current_file=None, latest_uri=None):
        self.current_file: str = current_file or "/var/www/html/index.php"
        self.latest_uri: str = latest_uri or "https://forum.vbulletin.com/forum/vbulletin-announcements/vbulletin-announcements_aa"

    def run(self, *_) -> Dict[str, float]:
        _current = self.to_float(self.current()) or "-1"
        _latest = self.to_float(self.latest()) or "-1"
        _using_latest = self.using_latest(_current, _latest)
        return {"current": _current, "latest": _latest, "using_latest": _using_latest}

    def to_float(self, version: str) -> str:
        """Convert version to Nixstats-compatible data type, float in str format."""
        try:
            split = version.split(".")
            return f"{split[0]}.{split[1]}{split[2]}"
        except (ValueError, TypeError):
            return version

    def using_latest(self, _current, _latest) -> str:
        return str(
            int(
                all([_current == _latest, _current != "-1", _latest != "-1"])
            )
        )

    def current(self) -> str:
        """Capture current vBulletin 5 in use."""
        with open(self.current_file) as fh:
            for line in fh.readlines():
                if "vbulletin 5" in line.lower():
                    return line.split()[3]

    def latest(self) -> str:
        """Fetch latest vBulletin Connect full version and/or latest Security Patch level."""
        base = re.compile(r"(5\.\d+\.\d+)")
        sec = re.compile(r"(?<=Security Patch Level )(\d+)")
        for line in requests.get(self.latest_uri).text.splitlines():
            if "vbulletin connect" in line.lower():
                match = base.search(line)
                if match:
                    return match.group(0)
            if "vbulletin" in line.lower() and "security patch" in line.lower():
                match = base.search(line)
                sec_match = sec.search(line)
                if match and sec_match:
                    return match.group(0) + sec_match.group(0)


if __name__ == "__main__":
    Plugin().execute()
