"""
animeapi.excepts
~~~~~~~~~~~~~~~~

This module contains the set of AnimeAPI's exceptions.
"""


class MissingRequirement(Exception):
    """
    Raised if there is an error with the request
    """


class UnsupportedVersion(Exception):
    """
    Raised if the version is unsupported
    """
