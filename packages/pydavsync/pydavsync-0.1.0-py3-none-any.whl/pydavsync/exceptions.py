# coding: utf-8


class MissingDavAddress(ValueError):
    def __init__(self):
        super().__init__(
            "At least one WebDav address must be given (in either source or dest)"
        )


class LocalPathDoesNotExist(ValueError):
    def __init__(self, local_path):
        super().__init__(f"Given local path '{local_path}' does not exist.")


class WebDavPathDoesNotExist(ValueError):
    def __init__(self, webdav_path):
        super().__init__(f"Given webdav path '{webdav_path}' does not exist.")


class DirectoryToFileError(ValueError):
    def __init__(self):
        super().__init__(
            "Synchronization cannot be performed from a directory to a file."
        )
