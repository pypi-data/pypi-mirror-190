# coding: utf-8

import re
import shutil
import pathlib

from pydavsync.webdav import walk
from pydavsync.exceptions import (
    WebDavPathDoesNotExist,
    DirectoryToFileError,
)


def pull(
    webdav_client,
    remote_path,
    local_path,
    recursive=True,
    ignore=None,
    keep_tree=False,
    delete=False,
    dry=False,
    verbose=False,
):
    """Synchronization of a webdav path (dir or file) to a local path.

    Warning:
        At the moment, sync is only done based on names. An improvement is to take
        other parameters into acccount like hash or size.

    Args:
        webdav_client: (webdav4.client.Client) the webdav connection to use for sync.
        remote_path: (str|pathlib.Path) The remote path to sync. Can be a directory
            or a file.
        local_path: (str|pathlib.Path) The local path where to sync the remote_path.
            It does not necessarily exist as the tree leaf can be created.
        recursive: (bool) Whether to sync subdirectories as well.
        ignore: (regex str) a pattern to ignore some paths (matches the full path).
        keep_tree: (bool) If True, the whole directory path given in `remote_path`
            is created in `local_directory`. If False, only the leaf is
            synchronized. Default is False.
            Example:
                if `remote_path` is `/dir1/dir2/dir3/file`
                When keep_tree=True, the file is written on this local path:
                `<local_directory>/dir1/dir2/dir3/file`
                When keep_tree=False, the file is written on this local path:
                `<local_directory>/file`
        delete: (bool) (optional) If True, delete local files that are not on the
            remote filesystem. Default is False, nothing is deleted.
        dry: (bool) (optional) If True, do not actually download the files, but only
            display a list of actions that would be performed. Default is False.
        verbose: (bool) (optional) If True, display details. Default is False.

    Raises:
        NotADirectoryError if `local_directory` is not a local directory.
        FileNotFoundError if the `remote_path` points to nothing.
    """
    # Make sure to use pathlib objects
    remote_path = pathlib.PurePosixPath(remote_path)
    local_path = pathlib.Path(local_path)

    # Check remote path existence
    if not webdav_client.exists(str(remote_path)):
        raise WebDavPathDoesNotExist(remote_path)

    # Destination is not necessarily existing, as it can be created during download
    # If source path is a directory, the destination cannot be an existing file.
    if webdav_client.isdir(str(remote_path)) and local_path.is_file():
        raise DirectoryToFileError()

    # If remote_path is a file, just get it without walking
    if webdav_client.isfile(str(remote_path)):
        # the remote path is becoming the top-level path of the synchronization.
        # Only subdirectories of this path must be copied if keep_tree is False.
        # Hence the remote_root value.
        local_dir = build_local_dir(
            local_root=local_path,
            remote_root=remote_path.parent,
            remote_subdir="",
            keep_tree=keep_tree,
        )
        pull_file(
            webdav_client=webdav_client,
            remote_path=remote_path,
            local_path=local_dir.joinpath(remote_path.name),
            ignore=ignore,
            file_info=None,
            dry=dry,
            verbose=verbose,
        )
        return

    # If remote_path is a directory, walk
    for walked_path, dirs, files in walk(webdav_client, remote_path):
        local_dir = build_local_dir(
            local_root=local_path,
            remote_root=remote_path,
            remote_subdir=walked_path,
            keep_tree=keep_tree,
        )

        # Remove local files that are not on the remote
        if delete and local_dir.exists():
            delete_items(local_dir, files, dirs, dry, verbose)

        # Synchronize files
        for file in files:
            # Here, "file" is a dictionary containing the keys "filename" and "size"
            pull_file(
                webdav_client=webdav_client,
                remote_path=walked_path.joinpath(file["filename"]),
                local_path=local_dir.joinpath(file["filename"]),
                ignore=ignore,
                file_info=file,
                dry=dry,
                verbose=verbose,
            )

        # If sync is not recursive, just stop in the first loop
        if not recursive:
            if dry or verbose:
                print("Sync is not recursive. Stop here.")
            break


def pull_file(
    webdav_client,
    remote_path,
    local_path,
    ignore=None,
    file_info=None,
    dry=False,
    verbose=False,
):
    """Synchronize a single file.

    Args:
        webdav_client: (webdav4.client.Client) the webdav connection to use for sync.
        remote_path: (pathlib.Path) the path of the remote file to synchronize.
        local_path: (pathlib.Path) the local path being the destination of the
            download.
        ignore: (str) (optional) full-path-pattern pattern to ignore some files.
        file_info: (dict) (optional) Additional information about the file. It is used
            to determine if the file has changed and must be downloaded. For now, it
            can contain the key "size". If additional information is not provided, a
            request will be made to fetch it. Providing a dictionary avoids making
            additional requests, therefore improving performance efficiency. Future
            improvements: add other info about the file like the hash, or the last
            modification time.
        dry: (bool) (optional) If True, do not actually download the files, but only
            display a list of actions that would be performed. Default False.
        verbose: (bool) (optional) If True, display details. Default is False.

    Raises:
        FileNotFoundError if one of the requested files is not found on remote host.
    """

    # Ignore file from regex
    # The pattern can match anything in the path! Allows to ignore directories.
    if ignore is not None and re.search(ignore, str(remote_path)):
        return

    # Build file info if missing
    if file_info is None:
        file_info = {
            "size": webdav_client.content_length(str(remote_path)),
        }

    # Ignore if file exists and has not changed
    if (
        local_path.exists()
        and local_path.lstat().st_size == file_info["size"]
        and local_path.lstat().st_mtime > file_info["modified"].timestamp()
    ):
        if dry or verbose:
            print(f"✅ {local_path} is already synchronized.")
        return

    # Make the directory tree
    local_path.parent.mkdir(parents=True, exist_ok=True)

    # Download the file to the local file system
    if dry or verbose:
        print(f"⬇️  {webdav_client.base_url}/{remote_path} ––> {local_path}")
    if not dry:
        webdav_client.download_file(str(remote_path), str(local_path))


def build_local_dir(local_root, remote_root, remote_subdir, keep_tree):
    """Build the directory path on the local side.

    Args:
        local_root: (pathlib.Path) the top-level local directory to where the
            synchronization is performed.
        remote_root: (pathlib.Path) (optional) the top-level remote directory from where
            the synchronization is performed. Mandatory if `keep_tree` is `False`.
        remote_subdir: (pathlib.Path) the path of the remote sub-directory containing
            the file to synchronize.
        keep_tree: (bool) Whether to rebuild the full remote path on the local
            filesystem. If False (default), only the subpath below `remote_root` is
            copied on the local filesystem.

    Returns:
        (pathlib.Path) The path to the local file.
    """
    # Build the full path of the local directory
    if keep_tree:
        local_dir = local_root.joinpath(str(remote_subdir).lstrip("/"))
    else:
        if remote_root is None:
            raise ValueError(
                "keep_tree is False but remote_root is not given. "
                "Please read the docstring."
            )
        local_dir = local_root.joinpath(
            re.sub(str(remote_root), "", str(remote_subdir)).lstrip("/")
        )
    return local_dir


def delete_items(local_dir, files, dirs, dry=False, verbose=False):
    """Delete local items if they are missing from remote items.

    Content of "local_dir" is compared to the given list of files and directories.
    Any additional item on the local filesystem will be deleted.

    Args:
        local_dir: the local directory to list items.
        files: the remote files (dictionary with "filename" key)
        dirs: the remote directories.
        dry: (bool) (optional) If True, do not actually download the files, but only
            display a list of actions that would be performed. Default False.
        verbose: (bool) (optional) If True, display details. Default is False.
    """
    remote_items = set(f["filename"] for f in files) | set(dirs)
    local_items = set(str(p.name) for p in local_dir.iterdir())
    items_to_delete = local_items - remote_items
    for item in items_to_delete:
        itempath = local_dir.joinpath(item)
        if dry or verbose:
            print(f"🗑️  Deleting {itempath}")
            if dry:
                continue
        if itempath.is_file():
            itempath.unlink()
        else:
            shutil.rmtree(itempath)
