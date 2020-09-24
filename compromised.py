#!/usr/bin/env python
import plugins
import psutil
import re
import requests

# detect processes that aren't apache or php running under www-data or www-php users.
class Plugin(plugins.BasePlugin):
    __name__ = "compromised"

    def run(self, *_):
        results = {"compromised": len(list(compromised()))}
        return results # dict, values can only be float


def compromised():
    for process in processes_to_check():
        if process.name() not in ["php-fpm7.3", "php-fpm7.4", "apache2"]:
            yield process

def processes_to_check():
    for process in psutil.process_iter():
        if process.username() in ["www-data", "www-php"]:
            yield process


if __name__ == "__main__":
    Plugin().execute()
