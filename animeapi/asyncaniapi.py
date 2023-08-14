"""
animeapi.asyncaniapi
--------------------

This module contains the asynchronous AnimeAPI class, the main class for
interacting with AnimeAPI through asynchronous requests.

Please refer to the documentation for more information and examples.
"""

from enum import Enum
from json import loads
from typing import Any, Dict, List, Optional, Union

import aiohttp

import animeapi.converter as conv
from animeapi import excepts, models


class AsyncAnimeAPI:
    """The main class for interacting with the aniapi API"""

    def __init__(
        self,
        base_url: Union[models.Version, str] = models.Version.V3,
        timeout: Optional[int] = 100,
        headers: Optional[Dict[str, Any]] = None
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
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Allows the class to be used as a context manager"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):  # type: ignore
        """Allows the class to be used as a context manager"""
        await self.close()

    async def close(self) -> None:
        """Closes the session"""
        if self.session is not None:
            await self.session.close()
        return

    async def get_anime_relations(
        self,
        title_id: Union[str, int],
        platform: Union[str, models.Platform],
        media_type: Union[models.TraktMediaType,
                          models.TmdbMediaType, str, None] = None,
        title_season: Optional[int] = None,
    ) -> models.AnimeRelation:
        """
        Gets the relations for an anime

        :param title_id: The ID of the anime
        :type title_id: Union[str, int]
        :param platform: The platform to get the relations from
        :type platform: Union[str, models.Platform]
        :param media_type: The media type to get the relations from, defaults to None
        :type media_type: Union[models.TraktMediaType, models.TmdbMediaType, str, None] (optional)
        :param title_season: The season of the anime in Trakt, defaults to None
        :type title_season: Optional[int] (optional)
        :return: The relations for the anime
        :rtype: models.AnimeRelation
        :raises aiohttp.ClientResponseError: Raised if the request to the API fails
        :raises excepts.MissingRequirement: Raised if the platform is trakt but no media_type is provided
        :raises excepts.UnsupportedVersion: Raised if the platform is IMDb or TMDB but using V2
        :raises RuntimeError: Raised if the session is not initialized
        :raises ValueError: Raised if the AnimeAPI does not support the feature
        """
        if self.session is None:
            raise RuntimeError("Session is not initialized")

        if isinstance(platform, models.Platform):
            platform = platform.value
        if isinstance(media_type, Enum):
            media_type = media_type.value

        # check if platform is either IMDb or TMDB but using V2
        if platform in ["imdb", "themoviedb"] and self.base_url == models.Version.V2.value:
            raise excepts.UnsupportedVersion(
                f"{platform} is not supported on V2")

        if platform == "trakt":
            if media_type is None:
                raise excepts.MissingRequirement("Trakt requires a media type")
            if title_season == 0:
                raise ValueError(
                    "AnimeAPI does not support season 0 (specials) for Trakt shows")
        elif platform == "themoviedb":
            if media_type is None:
                raise excepts.MissingRequirement("TMDB requires a media type")
            if media_type == "shows":
                raise ValueError(
                    "AnimeAPI does not support TMDB TV shows entry yet")

        # build path
        season = ""
        if platform == "trakt":
            if not f"{title_id}".isdigit():
                raise ValueError(
                    "Media ID of Trakt is not an integer ID. Please resolve it first before continuing")
            title_id = f"{media_type}/{title_id}"
            if title_season is not None and media_type == "shows":
                season = f"/seasons/{title_season}"
        elif platform == "themoviedb":
            title_id = f"{media_type}/{title_id}"
        elif platform == "shikimori":
            title_id = str(title_id)
            if not title_id.isdigit():
                # drop any non-digit characters
                title_id = "".join([c for c in title_id if c.isdigit()])
        elif platform == "kitsu":
            title_id = str(title_id)
            if not title_id.isdigit():
                async with self.session.get(
                    f"https://kitsu.io/api/edge/anime?filter[slug]={title_id}",
                        timeout=self.timeout) as slug_req:
                    if slug_req.status != 200:
                        raise aiohttp.ClientResponseError(
                            slug_req.request_info,
                            slug_req.history,
                            code=slug_req.status)
                    title_id = (await slug_req.json())["data"][0]["id"]

        path = f"/{platform}/{title_id}{season}"

        async with self.session.get(
            f"{self.base_url}{path}",
            timeout=self.timeout,
                headers=self.headers) as req:
            if req.status != 200:
                raise aiohttp.ClientResponseError(
                    req.request_info,
                    req.history,
                    code=req.status)
            return conv.convert_arm(loads(await req.text()))

    async def get_dict_anime_relations(
        self,
        platform: Union[str, models.Platform],
    ) -> Dict[str, models.AnimeRelation]:
        """
        Gets the relations for anime available on the platform as a dictionary

        :param platform: The platform to get the relations from
        :type platform: Union[str, models.Platform]
        :return: The relations for the anime
        :rtype: Dict[str, models.AnimeRelation]
        :raises aiohttp.ClientResponseError: Raised if the request to the API fails
        :raises excepts.UnsupportedVersion: Raised if the platform is IMDb or TMDB but using V2
        :raises RuntimeError: Raised if the session is not initialized
        :raises ValueError: Raised if the platform is trakt but the title_season is 0
        """
        if self.session is None:
            raise RuntimeError("Session is not initialized")

        if isinstance(platform, models.Platform):
            platform = platform.value

        # check if platform is either IMDb or TMDB but using V2
        if platform in ["imdb", "themoviedb"] and self.base_url == models.Version.V2.value:
            raise excepts.UnsupportedVersion(
                f"{platform} is not supported on V2")

        async with self.session.get(
            f"{self.base_url}/{platform}.json",
            timeout=self.timeout,
                headers=self.headers) as req:
            if req.status not in [200, 302, 304]:
                raise aiohttp.ClientResponseError(
                    req.request_info,
                    req.history,
                    code=req.status)
            return conv.convert_from_dict(loads(await req.text()))

    async def get_list_anime_relations(
        self,
        platform: Union[str, models.Platform],
    ) -> List[models.AnimeRelation]:
        """
        Gets the relations for anime available on the platform as a list

        :param platform: The platform to get the relations from
        :type platform: Union[str, models.Platform]
        :return: The relations for the anime
        :rtype: List[models.AnimeRelation]
        :raises aiohttp.ClientResponseError: Raised if the request to the API fails
        :raises excepts.UnsupportedVersion: Raised if the platform is IMDb or TMDB but using V2
        :raises RuntimeError: Raised if the session is not initialized
        :raises ValueError: Raised if the platform is trakt but the title_season is 0
        """
        if self.session is None:
            raise RuntimeError("Session is not initialized")

        if isinstance(platform, models.Platform):
            platform = platform.value

        # check if platform is either IMDb or TMDB but using V2
        if platform in ["imdb", "themoviedb"] and self.base_url == models.Version.V2.value:
            raise excepts.UnsupportedVersion(
                f"{platform} is not supported on V2")

        async with self.session.get(
            f"{self.base_url}/{platform}().json",
            timeout=self.timeout,
                headers=self.headers) as req:
            if req.status not in [200, 302, 304]:
                raise aiohttp.ClientResponseError(
                    req.request_info, req.history, code=req.status)
            return conv.convert_from_list(loads(await req.text()))

    async def get_list_index(self) -> List[models.AnimeRelation]:
        """
        Get AnimeAPI full list index of known anime in the database

        :return: The list index of known anime in the database
        :rtype: List[models.AnimeRelation]
        :raises aiohttp.ClientResponseError: Raised if the request to the API fails
        :raises RuntimeError: Raised if the session is not initialized
        """
        if self.session is None:
            raise RuntimeError("Session is not initialized")

        return await self.get_list_anime_relations("animeApi")

    async def get_status(self) -> models.ApiStatus:
        """
        Gets the status of the API

        :return: The status of the API
        :rtype: models.ApiStatus
        :raises aiohttp.ClientResponseError: Raised if the request to the API fails
        :raises excepts.UnsupportedVersion: Raised if the base_url is V2
        :raises RuntimeError: Raised if the session is not initialized
        """
        if self.session is None:
            raise RuntimeError("Session is not initialized")

        if self.base_url == models.Version.V2.value:
            raise excepts.UnsupportedVersion("Status is only supported on V3")

        async with self.session.get(
            f"{self.base_url}/status",
            timeout=self.timeout,
                headers=self.headers) as req:
            if req.status != 200:
                raise aiohttp.ClientResponseError(
                    req.request_info,
                    req.history,
                    code=req.status)
            return conv.convert_api_status(loads(await req.text()))

    async def get_heartbeat(self) -> models.Heartbeat:
        """
        Gets the heartbeat of the API

        :return: The heartbeat of the API
        :rtype: models.Heartbeat
        :raises aiohttp.ClientResponseError: Raised if the request to the API fails
        :raises excepts.UnsupportedVersion: Raised if the base_url is V2
        :raises RuntimeError: Raised if the session is not initialized
        """
        if self.session is None:
            raise RuntimeError("Session is not initialized")

        if self.base_url == models.Version.V2.value:
            raise excepts.UnsupportedVersion(
                "Heartbeat is only supported on V3")

        async with self.session.get(
            f"{self.base_url}/heartbeat",
            timeout=self.timeout,
                headers=self.headers) as req:
            if req.status != 200:
                raise aiohttp.ClientResponseError(
                    req.request_info,
                    req.history,
                    code=req.status)
            return conv.convert_heartbeat(loads(await req.text()))

    async def get_updated_time(self) -> models.Updated:
        """
        Gets the time the database was last updated, a subset/simple request from /status endpoint

        :return: The time the database was last updated
        :rtype: models.Updated
        :raises aiohttp.ClientResponseError: Raised if the request to the API fails
        :raises RuntimeError: Raised if the session is not initialized
        """
        if self.session is None:
            raise RuntimeError("Session is not initialized")

        async with self.session.get(
            f"{self.base_url}/updated",
            timeout=self.timeout,
                headers=self.headers) as req:
            if req.status != 200:
                raise aiohttp.ClientResponseError(
                    req.request_info,
                    req.history,
                    code=req.status)

            text = await req.text()
            return models.Updated(text)
