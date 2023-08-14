"""
animeapi
========

A Python wrapper for the AnimeAPI by nattadasu with type hints and additional
async support.

:license: AGPL-3.0, see LICENSE for more details.
:author: nattadasu
"""

from animeapi.animeapi import AnimeAPI
from animeapi.asyncaniapi import AsyncAnimeAPI
from animeapi.excepts import MissingRequirement, UnsupportedVersion
from animeapi.models import (AnimeRelation, ApiStatus, CountStruct, Heartbeat,
                             Platform, TraktMediaType, Updated, UpdatedStruct,
                             Version)

__version__ = "3.2.1"

__all__ = [
    "AnimeAPI",
    "AnimeRelation",
    "ApiStatus",
    "AsyncAnimeAPI",
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
