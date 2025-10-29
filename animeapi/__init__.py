"""
animeapi
========

A Python wrapper for the AnimeAPI by nattadasu with type hints and additional
async support.

:license: AGPL-3.0, see LICENSE for more details.
:author: nattadasu
"""

from animeapi.__version__ import __version__
from animeapi.animeapi import AnimeAPI
from animeapi.asyncaniapi import AsyncAnimeAPI
from animeapi.base import BaseAnimeAPI
from animeapi.excepts import MissingRequirement, UnsupportedVersion
from animeapi.models import (AnimeRelation, ApiStatus, CountStruct, Heartbeat,
                             Platform, TraktMediaType, Updated, UpdatedStruct,
                             Version)

__all__ = [
    "__version__",
    "AnimeAPI",
    "AnimeRelation",
    "ApiStatus",
    "AsyncAnimeAPI",
    "BaseAnimeAPI",
    "CountStruct",
    "Heartbeat",
    "MissingRequirement",
    "Platform",
    "TraktMediaType",
    "UnsupportedVersion",
    "Updated",
    "UpdatedStruct",
    "Version",
]
