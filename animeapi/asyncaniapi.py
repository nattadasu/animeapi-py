"""
animeapi.asyncaniapi
--------------------

This module contains the asynchronous AnimeAPI class, the main class for
interacting with AnimeAPI through asynchronous requests.

Please refer to the documentation for more information and examples.
"""

from json import loads
from typing import Dict, List, Optional, Union

import aiohttp

import animeapi.converter as conv
from animeapi import models
from animeapi.base import BaseAnimeAPI


class AsyncAnimeAPI(BaseAnimeAPI):
    """The main class for interacting with the aniapi API"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
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

    async def get_anime_relations(
        self,
        title_id: Union[str, int],
        platform: Union[str, models.Platform],
        media_type: Union[
            models.TraktMediaType, models.TmdbMediaType, str, None
        ] = None,
        title_season: Union[int, None] = None,
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
        :raises RuntimeError: Raised if the session is not initialized
        :raises ValueError: Raised if the AnimeAPI does not support the feature
        """
        if self.session is None:
            raise RuntimeError("Session is not initialized")

        if isinstance(platform, models.Platform):
            platform_val = platform.value
        else:
            platform_val = platform

        if platform_val == "kitsu":
            title_id = str(title_id)
            if not title_id.isdigit():
                async with self.session.get(
                    f"https://kitsu.io/api/edge/anime?filter[slug]={title_id}",
                    timeout=self.timeout,
                ) as slug_req:
                    if slug_req.status != 200:
                        raise aiohttp.ClientResponseError(
                            slug_req.request_info,
                            slug_req.history,
                            code=slug_req.status,
                        )
                    title_id = (await slug_req.json())["data"][0]["id"]

        path = self._build_path(title_id, platform, media_type, title_season)

        async with self.session.get(
            f"{self.base_url}{path}", timeout=self.timeout, headers=self.headers
        ) as req:
            if req.status != 200:
                raise aiohttp.ClientResponseError(
                    req.request_info, req.history, code=req.status
                )
            self._check_server_version(dict(req.headers))
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
        :raises RuntimeError: Raised if the session is not initialized
        :raises ValueError: Raised if the platform is trakt but the title_season is 0
        """
        if self.session is None:
            raise RuntimeError("Session is not initialized")

        if isinstance(platform, models.Platform):
            platform = platform.value

        async with self.session.get(
            f"{self.base_url}/{platform}.json",
            timeout=self.timeout,
            headers=self.headers,
        ) as req:
            if req.status not in [200, 302, 304]:
                raise aiohttp.ClientResponseError(
                    req.request_info, req.history, code=req.status
                )
            self._check_server_version(dict(req.headers))
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
        :raises RuntimeError: Raised if the session is not initialized
        :raises ValueError: Raised if the platform is trakt but the title_season is 0
        """
        if self.session is None:
            raise RuntimeError("Session is not initialized")

        if isinstance(platform, models.Platform):
            platform = platform.value

        async with self.session.get(
            f"{self.base_url}/{platform}().json",
            timeout=self.timeout,
            headers=self.headers,
        ) as req:
            if req.status not in [200, 302, 304]:
                raise aiohttp.ClientResponseError(
                    req.request_info, req.history, code=req.status
                )
            self._check_server_version(dict(req.headers))
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
        :raises RuntimeError: Raised if the session is not initialized
        """
        if self.session is None:
            raise RuntimeError("Session is not initialized")

        async with self.session.get(
            f"{self.base_url}/status", timeout=self.timeout, headers=self.headers
        ) as req:
            if req.status != 200:
                raise aiohttp.ClientResponseError(
                    req.request_info, req.history, code=req.status
                )
            self._check_server_version(dict(req.headers))
            return conv.convert_api_status(loads(await req.text()))

    async def get_heartbeat(self) -> models.Heartbeat:
        """
        Gets the heartbeat of the API

        :return: The heartbeat of the API
        :rtype: models.Heartbeat
        :raises aiohttp.ClientResponseError: Raised if the request to the API fails
        :raises RuntimeError: Raised if the session is not initialized
        """
        if self.session is None:
            raise RuntimeError("Session is not initialized")

        async with self.session.get(
            f"{self.base_url}/heartbeat", timeout=self.timeout, headers=self.headers
        ) as req:
            if req.status != 200:
                raise aiohttp.ClientResponseError(
                    req.request_info, req.history, code=req.status
                )
            self._check_server_version(dict(req.headers))
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
            f"{self.base_url}/updated", timeout=self.timeout, headers=self.headers
        ) as req:
            if req.status != 200:
                raise aiohttp.ClientResponseError(
                    req.request_info, req.history, code=req.status
                )

            self._check_server_version(dict(req.headers))
            text = await req.text()
            return models.Updated(text)
