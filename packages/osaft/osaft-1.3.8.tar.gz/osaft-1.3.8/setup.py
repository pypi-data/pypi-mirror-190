import codecs
import os.path
import re

import setuptools


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        match = re.search(r"## (\d{1,2}\.\d{1,2}\.\d{1,2})", line)
        if match is not None:
            match = match.group(1)
            return str(match)
    else:
        raise RuntimeError("Unable to find version string.")


def write_version():
    version = get_version("CHANGELOG.md")
    with open("osaft/core/version.py", "w") as f:
        f.write(f'__version__ = "{version}"\n')


write_version()

setuptools.setup()
