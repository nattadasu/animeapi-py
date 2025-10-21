"""
animeapi.base
-------------

This module contains the BaseAnimeAPI class, the base class for
the synchronous and asynchronous AnimeAPI classes.
"""

from enum import Enum
from typing import Any, Dict, Optional, Union

from animeapi import excepts, models


class BaseAnimeAPI:
    """The base class for the synchronous and asynchronous AnimeAPI classes"""

    def __init__(
        self,
        base_url: Union[models.Version, str] = models.Version.V3,
        timeout: Optional[int] = 100,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initializes the AnimeAPI class

        :param base_url: The base URL to use for requests, defaults to models.Version.V3
        :type base_url: Union[models.Version, str] (optional)
        :param timeout: The timeout for requests, defaults to 100
        :type timeout: int (optional)
        :param headers: The headers to use for requests, defaults to None
        :type headers: Dict[str, Any] (optional)
        """
        self.timeout = timeout
        self.headers = headers
        if isinstance(base_url, models.Version):
            self.base_url = base_url.value
        else:
            self.base_url = base_url

    def _build_path(
        self,
        title_id: Union[str, int],
        platform: Union[str, models.Platform],
        media_type: Union[
            models.TraktMediaType, models.TmdbMediaType, str, None
        ] = None,
        title_season: Optional[int] = None,
    ) -> str:
        """
        Builds the path for a request

        :param title_id: The ID of the anime
        :type title_id: Union[str, int]
        :param platform: The platform to get the relations from
        :type platform: Union[str, models.Platform]
        :param media_type: The media type to get the relations from, defaults to None
        :type media_type: Union[models.TraktMediaType, models.TmdbMediaType, str, None] (optional)
        :param title_season: The season of the anime in Trakt, defaults to None
        :type title_season: Optional[int] (optional)
        :return: The path for the request
        :rtype: str
        """
        if isinstance(platform, models.Platform):
            platform = platform.value
        if isinstance(media_type, Enum):
            media_type = media_type.value

        # check if platform is either IMDb or TMDB but using V2
        if (
            platform in ["imdb", "themoviedb"]
            and self.base_url == models.Version.V2.value
        ):
            raise excepts.UnsupportedVersion(
                f"{platform} is not supported on V2")

        if platform == "trakt":
            if media_type is None:
                raise excepts.MissingRequirement("Trakt requires a media type")
            if title_season == 0:
                raise ValueError(
                    "AnimeAPI does not support season 0 (specials) for Trakt shows"
                )
        elif platform == "themoviedb":
            if media_type is None:
                raise excepts.MissingRequirement("TMDB requires a media type")
        elif platform == "thetvdb":
            # THETVDB uses series/ID format
            pass

        # build path
        season = ""
        if platform == "trakt":
            if not f"{title_id}".isdigit():
                raise ValueError(
                    "Media ID of Trakt is not an integer ID. Please resolve it first before continuing"
                )
            title_id = f"{media_type}/{title_id}"
            if title_season is not None and media_type == "shows":
                season = f"/seasons/{title_season}"
        elif platform == "themoviedb":
            title_id = f"{media_type}/{title_id}"
            if title_season is not None and media_type == "tv":
                season = f"/season/{title_season}"
        elif platform == "thetvdb":
            title_id = f"series/{title_id}"
            if title_season is not None:
                season = f"/seasons/{title_season}"
        elif platform == "shikimori":
            title_id = str(title_id)
            if not title_id.isdigit():
                # drop any non-digit characters
                title_id = "".join([c for c in title_id if c.isdigit()])

        return f"/{platform}/{title_id}{season}"
