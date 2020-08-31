import inspect
import json
import logging
import os
import re
import sys
import subprocess
import threading
from urllib import request
import socket
from multiprocessing import Process, Queue

def split(s, delim="\n"):
    return list(filter(None, [x.strip() for x in re.split(delim, s.strip())]))

def sf(string, *args, **kwargs):
    return string.format(*args, **kwargs)


def replace(heading):
    rep = "-".join(split(heading.lower(), r"\s+"))
    return sf('# <a name="{}" href="#{}">{}</a>', rep, rep, heading)

def gentoc(content):
    start = "<!-- toc -->"
    end = "<!-- tocstop -->"
    startIndex = content.index(start) + len(start)
    endIndex = content.index(end)
    r = re.compile(r'^#\s+<a\s+name\s*=\s*"[\w-]+"\s+href\s*=\s*"(#[\w-]+)">\s*([\w\s]+)\s*</a>', re.M)
    links = []
    for x in r.finditer(content):
        link = x.group(1)
        text = x.group(2)
        links.append(sf("- [{}]({})", text, link))
    toc = "\n".join(links)
    return content[:startIndex] + toc + "\n" + content[endIndex:]

def go(param):
    with open(param) as f:
        content = f.read()
        regex = r"^#\s+(\w.*)"
        r = re.compile(regex, re.M)
        content = r.sub(lambda m: replace(m.group(1)), content)
        content = gentoc(content)
    with open(param, "w") as f:
        f.write(content)


def main(params):
    go(os.path.abspath(os.path.expanduser(params[0])))


if __name__ == '__main__':
    method = 'main'
    num_args = len(sys.argv)
    if num_args == 1 or sys.argv[1] not in globals():
        main(sys.argv[1:])
    elif num_args == 2:
        globals()[sys.argv[1]]()
    else:
        globals()[sys.argv[1]](sys.argv[2:])
