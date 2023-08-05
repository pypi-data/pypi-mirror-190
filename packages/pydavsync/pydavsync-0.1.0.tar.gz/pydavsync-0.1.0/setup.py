# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydavsync']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'webdav4>=0.9.7,<0.10.0']

entry_points = \
{'console_scripts': ['pydavsync = pydavsync.cli:maincmd']}

setup_kwargs = {
    'name': 'pydavsync',
    'version': '0.1.0',
    'description': 'Synchronization command line for WebDav.',
    'long_description': '# pydavsync\n\nA command line to synchronize files with WebDav servers, written in Python.\n\n## Name\n\nThe foundational idea was to have a similar command line and behavior to\n[rsync](https://rsync.samba.org/), but for WebDav servers. `davsync` is the logical\nname. But I started to implement it in Rust, then in Python, and I decided to integrate\nthe development language in the name. Thus `pydavsync` for the Python implementation.\n\n## Description\n\n[rsync](https://rsync.samba.org/) allows to synchronize files over a SSH connection.\n[pydavsync](https://framagit.org/RomainTT/pydavsync/) has been developed to do the same\nover a WebDav connection.\n\nThe command line is not identical because compatibility is not a goal, and some new\nideas emerged while developing `pydavsync`.\n\nThe following operations can be done\xa0:\n- Synchronization from local filesystem to WebDav server\n- Synchronization from WebDav server to local filesystem\n- Synchronization from WebDav server to WebDav server (not necessarily the same)\n\nHere are some of the features\xa0:\n- dry run\n- verbose output\n- login/password given through command line options\n- synchronization based on modified time and file size\n- deletion when files disappear\n\n### Webdav?\n\n[Webdav](https://fr.wikipedia.org/wiki/WebDAV) is used to manage files on remote servers\nusing HTTP.\n\nThe primary motivation was to use `pydavsync` with [Nextcloud](https://nextcloud.com/)\nwhich is compatible with webdav. But there are many other services accepting webdav.\n\n## Installation\n\n`pydavsync` is available on [Pypi.org](https://pypi.org/project/pydavsync) and can be\ninstalled using `pip`. Many options are available to you, do as you please.\n\n```\npip install pydavsync\n```\n\n## Usage\n\nOnce installed, the program `pydavsync` should be available in your terminal.\n\nTo get help, use `pydavsyncc --help`.\n\nHere is an example to synchronize files from a webdav server to a local directory.\n\n```sh\n$ pydavsync --src-user Username --src-pass Password --verbose https://my-server.org/path/to/my/directory /path/to/local/directory\n```\n\n## Support\n\nIf you have a question or need help, please [open an issue](https://framagit.org/RomainTT/pydavsync/-/issues/new) and tag it with the ~support label.\n\n## Roadmap\n\nFuture developments:\n\n- Synchronization from local to webdav (and consequently from webdav to webdav)\n- Smarter synchronization if source and destination are both the same webdav server.\n- Better tests with mocks to simulate a webdav server.\n- A [man](https://www.man7.org/linux/man-pages/man1/man.1.html) page.\n- New and optional means to check if a file has changed or not.\n\n## Contributing\n\n- Firstly, you can open [a new issue](https://framagit.org/RomainTT/pydavsync/-/issues/new) if you find a bug or have an improvement idea.\n- Any help to test the tool on various systems and Webdav servers is appreciated, as I did not checked many of these myself.\n- If you feel like coding, please [fork](https://framagit.org/RomainTT/pydavsync/-/forks/new) the repository and do a [merge request](https://framagit.org/RomainTT/pydavsync/-/merge_requests). It will be reviewed. Don’t forget to mention issues in your comments if you fix some of them!\n\n## Authors and acknowledgment\n\nMain author: Romain TAPREST [✉](mailto:romain@taprest.fr)\n\n## License\n\nThis project is under the [Mozilla Public License Version 2.0](https://choosealicense.com/licenses/mpl-2.0/).\n\n## Project status\n\n🧡 This project is alive! Not frequent updates, but it is not abandoned.\n',
    'author': 'Romain TAPREST',
    'author_email': 'romain@taprest.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://framagit.org/RomainTT/pydavsync',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
