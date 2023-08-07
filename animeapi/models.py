from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Union


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
    """aniSearch"""
    ANNICT = "annict"
    """Annict"""
    IMDB = "imdb"
    """IMDb, only for v3 API or above"""
    KAIZE = KZ = "kaize"
    """Kaize"""
    KITSU = KT = "kitsu"
    """Kitsu"""
    LIVECHART = LC = "livechart"
    """LiveChart"""
    MYANIMELIST = MAL = "myanimelist"
    """MyAnimeList"""
    NOTIFYMOE = NOTIFY = NM = "notify"
    """Notify.moe"""
    OTAKOTAKU = OT = "otakotaku"
    """Otak Otaku"""
    SHIKIMORI = SH = "shikimori"
    """Shikimori"""
    SHOBOI = SYOBOI = SHOBOCAL = SYOBOCAL = "shoboi"
    """Shobocalendar"""
    SILVERYASHA = DBTI = "silveryasha"
    """SilverYasha Database Tontonan Indonesia"""
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
    themoviedb: Union[int, str, None] = None
    """TheMovieDB ID of the anime, only for movies"""
    trakt: Optional[int] = None
    """Trakt ID of the anime"""
    trakt_season: Optional[int] = None
    """Trakt Season ID of the anime, None if its a movie"""
    trakt_type: Optional[TraktMediaType] = None

    def to_dict(self) -> Dict[str, Union[str, int, None]]:
        """
        Converts the AnimeRelation object to a dictionary

        :return: The converted dictionary
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
        
        :param tz: The timezone to use
        :type tz: timezone
        :return: The datetime object
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
