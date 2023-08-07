from animeapi.animeapi import AnimeAPI
from animeapi.asyncaniapi import AsyncAnimeAPI
from animeapi.excepts import MissingRequirement, UnsupportedVersion
from animeapi.models import (AnimeRelation, ApiStatus, CountStruct, Heartbeat,
                           Platform, TraktMediaType, UpdatedStruct, Version)

__version__ = "3.0.1"

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
    "UpdatedStruct",
    "Version",
]
