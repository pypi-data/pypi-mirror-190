import codecs
import os.path
import re


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_all_versions() -> None:
    out = []
    for line in read("CHANGELOG.md").splitlines():
        match = re.search(r"## (\d{1,2}\.\d{1,2}\.\d{1,2})", line)
        if match:
            tmp = re.search(r"(\d{1,2})\.(\d{1,2})\.(\d{1,2})", match.group(1))
            next_tuple = (
                int(tmp.group(1)),
                int(tmp.group(2)),
                int(tmp.group(3)),
            )

            out.append(next_tuple)
    return out


def get_float_from_version(version: tuple[int, int, int]) -> float:
    factor = 1000
    major = version[0]
    minor = version[1]
    patch = version[2]

    return major * factor + minor + patch / factor


def check_order_of_versions() -> None:
    all_versions = get_all_versions()

    last_version = 0

    for version in reversed(all_versions):
        new_version = get_float_from_version(version)
        assert new_version > last_version, f"Problem with {version}"
        last_version = new_version


def check_increment_of_version() -> None:
    all_versions = get_all_versions()

    last_major, last_minor, last_patch = 0, 0, 0

    for major, minor, patch in reversed(all_versions):

        if major == last_major:
            if minor == last_minor:
                test = last_patch == patch - 1
            else:
                test = (minor == last_minor + 1) and patch == 0
        else:
            test = (major == last_major + 1) and minor == 0 and patch == 0

        last_major, last_minor, last_patch = major, minor, patch
        assert test, f"Incrementing problem with {major}.{minor}.{patch}"


def main() -> None:
    check_order_of_versions()
    check_increment_of_version()


if __name__ == "__main__":
    main()
