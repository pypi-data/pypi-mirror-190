# coding: utf-8

"""Module containing useful general functions"""

from pathlib import PurePath
from urllib.parse import urlparse


def url_to_path(url):
    """Take a raw url and return a PurePath, extracted from it"""
    return PurePath(urlparse(url, allow_fragments=False).path)
