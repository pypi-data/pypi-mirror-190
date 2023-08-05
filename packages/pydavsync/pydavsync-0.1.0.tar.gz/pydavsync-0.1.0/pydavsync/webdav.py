# coding: utf-8

"""Module containing functions about webdav operations."""

import re
import pathlib
from urllib.parse import urlparse

import webdav4.client

from pydavsync.exceptions import WebDavPathDoesNotExist


def is_webdav_path(path):
    pattern = re.compile(r"^http(s)?://")
    return pattern.match(path) is not None


def connect_webdav(url, username=None, password=None, insecure=False):
    """Return a webdav4.client.Client object for the given webdav URL.

    Args:
        url: (str) URL of the webdav server. It can contain a file path or not (it will
            be ignored)
        username: (str) Username to connect to the server, if necessary.
        password: (str) password to connect to the server, if necessary.
        insecure: (bool) accept self-signed TLS certificates.
    """
    base_url = "{parts.scheme}://{parts.netloc}".format(parts=urlparse(url))
    auth = None if username is None or password is None else (username, password)
    return webdav4.client.Client(base_url, auth=auth, verify=not insecure)


def walk(webdav_client, remote_path):
    """Walk in a remote directory like os.walk, with webdav4 client.

    Args:
        remotepath: (str|pathlib.Path) the top directory to walk from.
            If it points to a file, it yields nothing and ends immediately.
            If it points to nothing, it raises an error.

    Yields:
        Same tuple than `os.walk`: (path, folders, files) but with the following
        exceptions:
            - files are not just strings (being the filenames), but dictionaries with
              keys `filename`, `size`, `modified`. That is useful to compare files in
              synchronization functions.

    Raise:
        WebDavPathDoesNotExist: if `remote_path` does not exist.
        StopIteration: when `remote_path` is a file or when there is no more files and
            directories to iterate.
    """
    path = pathlib.Path(remote_path)
    if not webdav_client.exists(str(path)):
        raise WebDavPathDoesNotExist(path)
    if webdav_client.isfile(str(path)):
        # Stop iteration
        return
    files = []
    folders = []
    for fattr in webdav_client.ls(str(path)):
        if fattr["type"] == "directory":
            # 'name' is actually the full path. Here only the name is extracted.
            folders.append(fattr["name"].split("/")[-1])
        else:
            # Do not append the name only, but the size as well
            files.append(
                {
                    "filename": fattr["name"].split("/")[-1],
                    # This is very specific for the webdav4 library,
                    # do not try to apply the same code to other clients
                    "size": fattr["content_length"],
                    # "modified" is a datetime.datetime object
                    "modified": fattr["modified"],
                }
            )
    yield path, folders, files
    for folder in folders:
        new_path = path.joinpath(folder)
        for new_tuple in walk(webdav_client, new_path):  # Recursivity for each dir
            yield new_tuple
