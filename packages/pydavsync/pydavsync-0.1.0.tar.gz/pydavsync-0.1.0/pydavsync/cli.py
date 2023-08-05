#!/usr/bin/env python
# coding: utf-8

import click

from webdav4.client import HTTPError

from pydavsync.sync import sync
from pydavsync.exceptions import (
    LocalPathDoesNotExist,
    MissingDavAddress,
    DirectoryToFileError,
)


@click.command()
@click.argument("source")
@click.argument("dest")
@click.option(
    "--src-user",
    type=str,
    help="Username for source Webdav. Useless if SOURCE is a local path.",
)
@click.option(
    "--src-pass",
    type=str,
    help="Password for source Webdav. Useless if SOURCE is a local path.",
)
@click.option(
    "--dst-user",
    type=str,
    help="Username for destination Webdav. Useless if DEST is a local path.",
)
@click.option(
    "--dst-pass",
    type=str,
    help="Password for destination Webdav. Useless if DEST is a local path.",
)
@click.option(
    "--insecure",
    is_flag=True,
    default=False,
    help="Use this flag to disable certificate verification.",
)
@click.option(
    "--delete",
    is_flag=True,
    default=False,
    help="Use this flag to delete files that are not in the source anymore.",
)
@click.option(
    "--dry",
    is_flag=True,
    default=False,
    help="Use this flag to perform a dry run.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Verbose mode.",
)
def maincmd(
    source, dest, src_user, src_pass, dst_user, dst_pass, insecure, delete, dry, verbose
):
    """pydavsync commmand line.

    \b
    SOURCE: the source path (local or webdav) to sync from.
    DEST: the destination path (local or webdav) to sync to.

    \b
    Attention:
        - SOURCE and DEST cannot be both local. At least of them must be a webdav path.
        - A local path has not any special syntax. It can be absolute (`/my/path`) or
          relative (`./my/path` or `my/path`). No wildcards.
        - A webdav path is written like this: `http[s]://host[:port]/path/on/dav/server`
          Port is optionnal. No wildcards.
        - Paths can lead to directories or files but SOURCE and DEST must be
          consistent! (no dir to file for instance)
    """
    if dry:
        click.echo("[!] This is a DRY run, nothing will be downloaded/uploaded.")
    try:
        sync(
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
    except LocalPathDoesNotExist as e:
        raise click.BadParameter(str(e))
    except MissingDavAddress as e:
        raise click.UsageError(str(e))
    except DirectoryToFileError as e:
        raise click.UsageError(str(e))
    except HTTPError as exc:
        if "403" in str(exc):
            raise click.BadParameter("Missing or bad login for webdav server.")
        raise click.ClickException(f"Unexpected HTTP error: {exc}")
