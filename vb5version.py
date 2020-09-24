#!/usr/bin/env python
import re
from typing import Dict

import plugins
import requests


class Plugin(plugins.BasePlugin):
    __name__ = "vb5version"

    def run(self, *_) -> Dict[str, str]:
        _current = self.to_float(self.current()) or "-1"
        _latest = self.to_float(self.latest()) or "-1"
        using_latest = str(int(_current == _latest))
        return {"current": _current, "latest": _latest, "using_latest": using_latest}

    def to_float(self, version: str) -> str:
        parts = version.split(".")
        try:
            return "%s.%s%s" % (parts[0], parts[1], parts[2])
        except IndexError:
            return version

    def current(self) -> str:
        with open("/var/www/html/index.php") as fh:
            for line in fh.readlines():
                if "vBulletin 5" in line:
                    return line.split()[3]

    def latest(self) -> str:
        f = requests.get("https://www.vbulletin.com/download.php")
        myre = re.compile(r"(5\.\d+\.\d+)")
        for line in f.text.splitlines():
            if "Latest Version:" in line:
                matched = myre.search(line)
                if matched:
                    return matched.group(0)


if __name__ == "__main__":
    Plugin().execute()
