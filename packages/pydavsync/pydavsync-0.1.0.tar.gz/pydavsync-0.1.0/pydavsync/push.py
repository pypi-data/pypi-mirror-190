# coding: utf-8

from pydavsync.exceptions import (
    LocalPathDoesNotExist,
    DirectoryToFileError,
)


def push(
    webdav_client,
    remote_path,
    local_path,
    delete=False,
    recursive=True,
    ignore=None,
    keep_tree=False,
    dry=False,
    verbose=False,
):
    if not local_path.exists():
        raise LocalPathDoesNotExist(local_path)

    # Destination is not necessarily existing, as it can be created during upload
    # If source path is a directory, the destination cannot be an existing file.
    if local_path.is_dir() and webdav_client.isfile(str(remote_path)):
        raise DirectoryToFileError()

    raise NotImplementedError
