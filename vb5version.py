#!/usr/bin/env python
import plugins
import re
import requests


class Plugin(plugins.BasePlugin):
    __name__ = "vb5version"

    def run(self, *_):
        _current = to_float(current())
        _latest = to_float(latest())
        using_latest = str(int(_current == _latest))
        results = {"current": _current, "latest": _latest, "using_latest": using_latest}
        return results

def current():
    with open("/var/www/html/index.php") as fh:
        for line in fh.readlines():
            if "vBulletin 5" in line:
                return line.split()[3]
    return -1


def latest():
    f = requests.get("https://www.vbulletin.com/download.php")
    myre = re.compile(r"(5\.\d+\.\d+)")
    for line in f.text.splitlines():
        if "Latest Version:" in line:
            matched = myre.search(line)
            if matched:
                return matched.group(0)


def to_float(version):
    parts = version.split(".")
    return "%s.%s%s" % (parts[0], parts[1], parts[2])




if __name__ == "__main__":
    Plugin().execute()
