# coding: utf-8

import pathlib
import tempfile

from pydavsync.webdav import connect_webdav, is_webdav_path
from pydavsync.pull import pull
from pydavsync.push import push
from pydavsync.tools import url_to_path
from pydavsync.exceptions import (
    MissingDavAddress,
    LocalPathDoesNotExist,
    DirectoryToFileError,
)


def sync(
    source,
    dest,
    src_user=None,
    src_pass=None,
    dst_user=None,
    dst_pass=None,
    insecure=False,
    delete=False,
    dry=False,
    verbose=False,
):
    """Entrypoint of pydavsync"""
    # TODO make custom exception for auth error, with details (src or dest?)
    if is_webdav_path(source):
        if is_webdav_path(dest):
            sync_from_webdav_to_webdav(
                source,
                dest,
                src_user,
                src_pass,
                dst_user,
                dst_pass,
                insecure,
                delete,
                dry,
                verbose,
            )
        else:
            sync_from_webdav_to_local(
                source, dest, src_user, src_pass, insecure, delete, dry, verbose
            )
    elif is_webdav_path(dest):
        if pathlib.Path(source).exists():
            sync_from_local_to_webdav(
                source, dest, dst_user, dst_pass, insecure, delete, dry, verbose
            )
        else:
            raise LocalPathDoesNotExist(source)
    else:
        raise MissingDavAddress()


def sync_from_local_to_webdav(
    source,
    dest,
    username=None,
    password=None,
    insecure=False,
    delete=False,
    dry=False,
    verbose=False,
):
    """Synchronization from a local path to a remote webdav server."""
    dst_client = connect_webdav(dest, username, password, insecure)
    src_path = pathlib.Path(source)
    dst_path = url_to_path(dest)
    push(dst_client, src_path, dst_path, delete=delete, dry=dry, verbose=verbose)


def sync_from_webdav_to_local(
    source,
    dest,
    username=None,
    password=None,
    insecure=False,
    delete=False,
    dry=False,
    verbose=False,
):
    """Synchronization from remote webdav server to a local path."""
    src_client = connect_webdav(source, username, password, insecure)
    src_path = url_to_path(source)
    dst_path = pathlib.Path(dest)
    pull(src_client, src_path, dst_path, delete=delete, dry=dry, verbose=verbose)


def sync_from_webdav_to_webdav(
    source,
    dest,
    src_user=None,
    src_pass=None,
    dst_user=None,
    dst_pass=None,
    insecure=False,
    delete=False,
    dry=False,
    verbose=False,
):
    """Synchronization between two remote webdav servers."""
    src_client = connect_webdav(source, src_user, src_pass, insecure)
    dst_client = connect_webdav(dest, dst_user, dst_pass, insecure)
    src_path = url_to_path(source)
    dst_path = url_to_path(dest)

    # Perform the following check before downloading anything, as would be useless.
    # If source path is a directory, the destination cannot be an existing file.
    if src_client.isdir(str(src_path)) and dst_client.isfile(str(dst_path)):
        raise DirectoryToFileError()

    with tempfile.TemporaryDirectory() as tmpdir:
        pull(src_client, src_path, tmpdir, delete=delete, dry=dry, verbose=verbose)
        push(dst_client, tmpdir, dst_path, delete=delete, dry=dry, verbose=verbose)
