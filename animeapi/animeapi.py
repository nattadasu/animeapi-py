from datetime import datetime, timezone
from typing import Any, Dict, Optional, Union, Literal, List

import requests

import animeapi.models as models
import animeapi.converter as conv
import animeapi.excepts as excepts


class AnimeAPI:
    """
    The main class for interacting with the aniapi API
    """

    def __init__(
            self,
            base_url: Union[models.Version, str] = models.Version.V3,
            timeout: Optional[int] = 10,
            headers: Optional[Dict[str, Any]] = None
        ) -> None:
        """
        Initializes the AnimeAPI class
        :param base_url: The base URL to use for requests, defaults to models.Version.V3
        :type base_url: Union[models.Version, str] (optional)
        :param timeout: The timeout for requests, defaults to 10
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

    def __enter__(self):
        """
        Allows the class to be used as a context manager
        """
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):  # type: ignore
        """
        Allows the class to be used as a context manager
        """
        pass

    def _get(self, endpoint: str) -> requests.Response:
        """
        Internal method for making GET requests

        :param endpoint: The endpoint to make the request to
        :type endpoint: str
        :return: The response from the API
        :rtype: requests.Response
        """
        return requests.get(f"{self.base_url}{endpoint}", timeout=self.timeout, headers=self.headers)

    def get_anime_relations(
            self,
            title_id: Union[str, int],
            platform: Union[str, models.Platform],
            media_type: Union[models.TraktMediaType, Literal["shows", "movies"], None] = None,
            title_season: Optional[int] = None,
        ) -> models.AnimeRelation:
        """
        Gets the relations for an anime

        :param title_id: The ID of the anime
        :type title_id: Union[str, int]
        :param platform: The platform to get the relations from
        :type platform: Union[str, models.Platform]
        :param media_type: The media type to get the relations from, defaults to None
        :type media_type: Union[models.TraktMediaType, Literal["shows", "movies"], None] (optional)
        :param title_season: The season of the anime in Trakt, defaults to None
        :type title_season: Optional[int] (optional)
        :return: The relations for the anime
        :rtype: models.AnimeRelation
        :raises excepts.MissingRequirement: Raised if the platform is trakt but no media_type is provided
        :raises excepts.UnsupportedVersion: Raised if the platform is IMDb or TMDB but using V2
        :raises ValueError: Raised if the platform is trakt but the title_season is 0
        """
        if isinstance(platform, models.Platform):
            platform = platform.value
        if isinstance(media_type, models.TraktMediaType):
            media_type = media_type.value

        # check if platform is either IMDb or TMDB but using V2
        if platform in ["imdb", "themoviedb"] and self.base_url == models.Version.V2.value:
            raise excepts.UnsupportedVersion(f"{platform} is not supported on V2")

        if platform == "trakt" and media_type is None:
            raise excepts.MissingRequirement("Trakt requires a media type")
        if platform == "trakt" and title_season == 0:
            raise ValueError("AnimeAPI does not support season 0 (specials) for Trakt shows")

        # build path
        if platform == "trakt":
            path = f"/{platform}/{media_type}/{title_id}"
            if title_season is not None and media_type == "shows":
                path += f"/seasons/{title_season}"
        elif platform == "shikimori":
            title_id = str(title_id)
            if not title_id.isdigit():
                # drop any non-digit characters
                title_id = "".join([c for c in title_id if c.isdigit()])
            path = f"/{platform}/{title_id}"
        elif platform == "kitsu":
            title_id = str(title_id)
            if not title_id.isdigit():
                # if its slug, try fetch from Kitsu to resolve the slug
                slug_req = requests.get(f"https://kitsu.io/api/edge/anime?filter[slug]={title_id}", timeout=self.timeout)
                if slug_req.status_code != 200:
                    slug_req.raise_for_status()
                title_id = slug_req.json()["data"][0]["id"]
            path = f"/{platform}/{title_id}"
        else:
            path = f"/{platform}/{title_id}"

        req = self._get(path)

        if req.status_code != 200:
            req.raise_for_status()
        
        return conv.convert_arm(req.json())

    def get_dict_anime_relations(
            self,
            platform: Union[str, models.Platform],
        ) -> Dict[str, models.AnimeRelation]:
        """
        Gets the relations for anime available on the platform as a dictionary

        :param platform: The platform to get the relations from
        :type platform: Union[str, models.Platform]
        :return: The relations for the anime
        :rtype: Dict[str, models.AnimeRelation]
        :raises excepts.UnsupportedVersion: Raised if the platform is IMDb or TMDB but using V2
        :raises ValueError: Raised if the platform is trakt but the title_season is 0
        """
        if isinstance(platform, models.Platform):
            platform = platform.value
        
        # check if platform is either IMDb or TMDB but using V2
        if platform in ["imdb", "themoviedb"] and self.base_url == models.Version.V2.value:
            raise excepts.UnsupportedVersion(f"{platform} is not supported on V2")
        
        req = self._get(f"/{platform}.json")

        if req.status_code not in [200, 302, 304]:
            req.raise_for_status()

        return conv.convert_from_dict(req.json())
    

    def get_list_anime_relations(
            self,
            platform: Union[str, models.Platform],
        ) -> List[models.AnimeRelation]:
        """
        Gets the relations for anime available on the platform as a list

        :param platform: The platform to get the relations from
        :type platform: Union[str, models.Platform]
        :return: The relations for the anime
        :rtype: List[models.AnimeRelation]
        :raises excepts.UnsupportedVersion: Raised if the platform is IMDb or TMDB but using V2
        :raises ValueError: Raised if the platform is trakt but the title_season is 0
        """
        if isinstance(platform, models.Platform):
            platform = platform.value

        # check if platform is either IMDb or TMDB but using V2
        if platform in ["imdb", "themoviedb"] and self.base_url == models.Version.V2.value:
            raise excepts.UnsupportedVersion(f"{platform} is not supported on V2")
        
        req = self._get(f"/{platform}%28%29.json")

        if req.status_code not in [200, 302, 304]:
            req.raise_for_status()

        return conv.convert_from_list(req.json())

    def get_list_index(self) -> List[models.AnimeRelation]:
        """
        Get AnimeAPI full list index of known anime in the database
        
        :return: The list index of known anime in the database
        :rtype: List[models.AnimeRelation]
        :raises requests.HTTPError: Raised if the request fails
        """
        return self.get_list_anime_relations("animeApi")

    def get_status(self) -> models.ApiStatus:
        """
        Gets the status of the API

        :return: The status of the API
        :rtype: models.Status
        :raises excepts.UnsupportedVersion: Raised if the base_url is V2
        :raises requests.HTTPError: Raised if the request fails
        """
        if self.base_url == models.Version.V2.value:
            raise excepts.UnsupportedVersion("Status is only supported on V3")

        req = self._get("/status")

        if req.status_code != 200:
            req.raise_for_status()
        
        return conv.convert_api_status(req.json())

    def get_heartbeat(self) -> models.Heartbeat:
        """
        Gets the heartbeat of the API

        :return: The heartbeat of the API
        :rtype: models.Heartbeat
        :raises excepts.UnsupportedVersion: Raised if the base_url is V2
        :raises requests.HTTPError: Raised if the request fails
        """
        if self.base_url == models.Version.V2.value:
            raise excepts.UnsupportedVersion("Heartbeat is only supported on V3")

        req = self._get("/heartbeat")

        if req.status_code != 200:
            req.raise_for_status()
        
        return conv.convert_heartbeat(req.json())

    def get_updated_time(self, use_datetime: bool = False) -> Union[str, datetime]:
        """
        Gets the time the database was last updated, a subset/simple request from /status endpoint

        :param use_datetime: Whether to return a datetime object or a string, defaults to False
        :type use_datetime: bool, optional
        :return: The time the database was last updated
        :rtype: Union[str, datetime]
        :raises requests.HTTPError: Raised if the request fails
        """
        req = self._get("/updated")

        if req.status_code != 200:
            req.raise_for_status()

        if use_datetime:
            time = datetime.strptime(req.text, "Updated on %d/%m/%Y %H:%M:%S UTC")
            time = time.replace(tzinfo=timezone.utc)
            return time
        else:
            return req.text
