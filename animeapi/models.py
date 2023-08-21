"""
animeapi.models
---------------

This module contains the dataclasses, enums, and other models used by the API.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Literal, Optional

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict  # type: ignore


class Version(Enum):
    """API Version Enum"""

    V2 = "https://aniapi.nattadasu.my.id"
    """Version 2"""
    V3 = "https://animeapi.my.id"
    """Version 3"""


class Platform(Enum):
    """Supported Platforms Enum"""

    ANIDB = ADB = "anidb"
    """AniDB"""
    ANILIST = AL = "anilist"
    """AniList"""
    ANIMEPLANET = AP = ANIPLA = "animeplanet"
    """Anime-Planet"""
    ANISEARCH = AS = "anisearch"
    """aniSearch, a German anime database"""
    ANNICT = "annict"
    """Annict, a Japanese anime database"""
    IMDB = "imdb"
    """IMDb, only for v3 API or above"""
    KAIZE = KZ = "kaize"
    """Kaize"""
    KITSU = KT = "kitsu"
    """Kitsu"""
    LIVECHART = LC = "livechart"
    """LiveChart, a TV schedule database"""
    MYANIMELIST = MAL = "myanimelist"
    """MyAnimeList"""
    NAUTILJON = NJ = "nautiljon"
    """Nautiljon, a French anime database"""
    NOTIFYMOE = NOTIFY = NM = "notify"
    """Notify.moe"""
    OTAKOTAKU = OT = "otakotaku"
    """Otak Otaku, an Indonesian anime database"""
    SHIKIMORI = SH = "shikimori"
    """Shikimori, a Russian anime database"""
    SHOBOI = SYOBOI = SHOBOCAL = SYOBOCAL = "shoboi"
    """Shobocalendar, a TV schedule database in Japanese"""
    SILVERYASHA = DBTI = "silveryasha"
    """SilverYasha Database Tontonan Indonesia, an Indonesian anime database for aggregated streaming links"""
    THEMOVIEDB = TMDB = "themoviedb"
    """TheMovieDB, only for v3 API or above"""
    TRAKT = "trakt"
    """Trakt"""


class TraktMediaType(Enum):
    """Trakt Media Type Enum"""

    SHOWS = "shows"
    """Show"""
    MOVIES = "movies"
    """Movie"""


class TmdbMediaType(Enum):
    """TheMovieDB Media Type Enum"""

    MOVIE = "movie"
    """Movie"""


class TypedAnimeRelationDict(TypedDict):
    """
    Typed Anime Relation Dictionary, used when user explicitly wants to use a
    dictionary using AnimeRelation.to_dict() method
    """

    title: str
    """Title of the anime"""
    anidb: Optional[int]
    """aniDB ID of the anime, without the prefix"""
    anilist: Optional[int]
    """AniList ID of the anime"""
    animeplanet: Optional[str]
    """Anime-Planet slug of the anime"""
    anisearch: Optional[int]
    """aniSearch ID of the anime"""
    annict: Optional[int]
    """Annict ID of the anime"""
    imdb: Optional[str]
    """IMDb ID of the anime, mostly for movies"""
    kaize: Optional[str]
    """Kaize slug of the anime"""
    kaize_id: Optional[int]
    """Kaize ID of the anime, used internally for the Kaize API"""
    kitsu: Optional[int]
    """Kitsu ID of the anime"""
    livechart: Optional[int]
    """LiveChart ID of the anime"""
    myanimelist: Optional[int]
    """MyAnimeList ID of the anime"""
    nautiljon: Optional[str]
    """Nautiljon slug in plus format of the anime"""
    nautiljon_id: Optional[int]
    """Nautiljon ID of the anime, used internally by Nautiljon"""
    notify: Optional[str]
    """Notify.moe Base64 of the anime"""
    otakotaku: Optional[int]
    """Otak Otaku ID of the anime"""
    shoboi: Optional[int]
    """Shoboi ID of the anime"""
    shikimori: Optional[int]
    """Shikimori ID of the anime, without the prefix"""
    silveryasha: Optional[int]
    """SilverYasha Database Tontonan Indonesia ID of the anime"""
    themoviedb: Optional[int]
    """TheMovieDB ID of the anime, only for movies"""
    trakt: Optional[int]
    """Trakt ID of the anime"""
    trakt_season: Optional[int]
    """Trakt Season ID of the anime, None if its a movie"""
    trakt_type: Optional[Literal['shows', 'movies']]
    """Trakt Media Type of the anime"""


@dataclass
class AnimeRelation:
    """Anime Relations Dataclass"""

    title: str
    """Title of the anime"""
    anidb: Optional[int] = None
    """aniDB ID of the anime, without the prefix"""
    anilist: Optional[int] = None
    """AniList ID of the anime"""
    animeplanet: Optional[str] = None
    """Anime-Planet slug of the anime"""
    anisearch: Optional[int] = None
    """aniSearch ID of the anime"""
    annict: Optional[int] = None
    """Annict ID of the anime"""
    imdb: Optional[str] = None
    """IMDb ID of the anime, mostly for movies"""
    kaize: Optional[str] = None
    """Kaize slug of the anime"""
    kaize_id: Optional[int] = None
    """Kaize ID of the anime, used internally for the Kaize API"""
    kitsu: Optional[int] = None
    """Kitsu ID of the anime"""
    livechart: Optional[int] = None
    """LiveChart ID of the anime"""
    myanimelist: Optional[int] = None
    """MyAnimeList ID of the anime"""
    nautiljon: Optional[str] = None
    """Nautiljon slug in plus format of the anime"""
    nautiljon_id: Optional[int] = None
    """Nautiljon ID of the anime, used internally by Nautiljon"""
    notify: Optional[str] = None
    """Notify.moe Base64 of the anime"""
    otakotaku: Optional[int] = None
    """Otak Otaku ID of the anime"""
    shoboi: Optional[int] = None
    """Shoboi ID of the anime"""
    shikimori: Optional[int] = None
    """Shikimori ID of the anime, without the prefix"""
    silveryasha: Optional[int] = None
    """SilverYasha Database Tontonan Indonesia ID of the anime"""
    themoviedb: Optional[int] = None
    """TheMovieDB ID of the anime, only for movies"""
    trakt: Optional[int] = None
    """Trakt ID of the anime"""
    trakt_season: Optional[int] = None
    """Trakt Season ID of the anime, None if its a movie"""
    trakt_type: Optional[TraktMediaType] = None
    """Trakt Media Type of the anime"""

    def to_dict(self) -> TypedAnimeRelationDict:
        """
        Converts the AnimeRelation object to a dictionary

        :return: The converted dictionary
        :rtype: TypedAnimeRelationDict
        """
        return {
            "title": self.title,
            "anidb": self.anidb,
            "anilist": self.anilist,
            "animeplanet": self.animeplanet,
            "anisearch": self.anisearch,
            "annict": self.annict,
            "imdb": self.imdb,
            "kaize": self.kaize,
            "kaize_id": self.kaize_id,
            "kitsu": self.kitsu,
            "livechart": self.livechart,
            "myanimelist": self.myanimelist,
            "nautiljon": self.nautiljon,
            "nautiljon_id": self.nautiljon_id,
            "notify": self.notify,
            "otakotaku": self.otakotaku,
            "shoboi": self.shoboi,
            "shikimori": self.shikimori,
            "silveryasha": self.silveryasha,
            "themoviedb": self.themoviedb,
            "trakt": self.trakt,
            "trakt_season": self.trakt_season,
            "trakt_type": self.trakt_type.value if self.trakt_type else None,
        }


@dataclass
class UpdatedStruct:
    """Updated Struct Dataclass"""

    timestamp: int
    """Timestamp of the update"""
    iso: str
    """ISO 8601 formatted timestamp of the update"""

    # add datetime object
    def datetime(self, tz: timezone = timezone.utc) -> datetime:
        """
        Returns a datetime object of the timestamp

        :param tz: The timezone to use, defaults to UTC
        :type tz: timezone = timezone.utc
        :return: The datetime object
        :rtype: datetime
        """
        return datetime.fromtimestamp(self.timestamp, tz=tz)


@dataclass
class CountStruct:
    """Count Struct Dataclass"""

    total: int
    """Total count"""
    anidb: Optional[int] = None
    """aniDB count"""
    anilist: Optional[int] = None
    """AniList count"""
    animeplanet: Optional[int] = None
    """Anime-Planet count"""
    anisearch: Optional[int] = None
    """aniSearch count"""
    annict: Optional[int] = None
    """Annict count"""
    imdb: Optional[int] = None
    """IMDb count"""
    kaize: Optional[int] = None
    """Kaize count"""
    kitsu: Optional[int] = None
    """Kitsu count"""
    livechart: Optional[int] = None
    """LiveChart count"""
    myanimelist: Optional[int] = None
    """MyAnimeList count"""
    nauitljon: Optional[int] = None
    """Nautiljon count"""
    notify: Optional[int] = None
    """Notify.moe count"""
    otakotaku: Optional[int] = None
    """Otak Otaku count"""
    shikimori: Optional[int] = None
    """Shikimori count"""
    shoboi: Optional[int] = None
    """Shoboi count"""
    silveryasha: Optional[int] = None
    """SilverYasha Database Tontonan Indonesia count"""
    themoviedb: Optional[int] = None
    """TheMovieDB count"""
    trakt: Optional[int] = None
    """Trakt count"""


@dataclass
class ApiStatus:
    """API Status Dataclass"""

    mainrepo: str
    """Main repository of the API"""
    updated: UpdatedStruct
    """Last updated of the API"""
    contributors: List[str]
    """List of contributors of the API"""
    sources: List[str]
    """List of sources used by the API"""
    license: str
    """License of the API"""
    website: str
    """Website of the API"""
    counts: CountStruct
    """Counts of the API"""
    endpoints: Dict[str, str]
    """Endpoints of the API"""


@dataclass
class Heartbeat:
    """Heartbeat Dataclass"""

    status: str
    """Status of the API"""
    code: int
    """Status code of the API"""
    response_time: str
    """Response time of the API"""
    request_time: str
    """Request time of the API"""
    request_epoch: float
    """Request epoch of the API"""

    def datetime(self, tz: timezone = timezone.utc) -> datetime:
        """
        Returns a datetime object of the heartbeat's request epoch

        :param tz: The timezone to use, defaults to timezone.utc
        :type tz: timezone
        :return: The datetime object
        :rtype: datetime
        """
        return datetime.fromtimestamp(self.request_epoch, tz=tz)


class Updated:
    """Class model for "Updated" path"""

    def __init__(self, message: str):
        self.message = message

    def __repr__(self):
        return f"{self.message}"

    def datetime(self) -> datetime:
        """
        Convert str response to datetime class

        :return: the datetime object
        :rtype: datetime
        """
        time = datetime.strptime(
            self.message, "Updated on %m/%d/%Y %H:%M:%S UTC")
        time = time.replace(tzinfo=timezone.utc)
        return time
