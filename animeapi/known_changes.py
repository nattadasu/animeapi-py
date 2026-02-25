from dataclasses import dataclass
from enum import Enum
from typing import List


class CType(Enum):
    ADDED = ADD = "added"
    REMOVED = REM = "removed"
    UPDATED = UP = "updated"
    DEPRECATED = DEP = "deprecated"


@dataclass
class Change:
    type_: CType
    field: str
    message: str


@dataclass
class Rev:
    timestamp: int
    changes: List[Change]


KNOWN_CHANGES = [
    Rev(
        1771033687,
        [
            Change(
                CType.ADD,
                "hikka",
                "Hikka is now added to the lookup",
            ),
            Change(
                CType.REM,
                "animeapi",
                "All platfrom-dedicated databases were deleted",
            ),
        ],
    ),
    Rev(
        1768814119,
        [
            Change(
                CType.UP,
                "server",
                "Fixed season path for Trakt, TMDB, and TVDB",
            ),
            Change(
                CType.REM,
                "animeapi",
                "All platform-dedicated endpoints were set to 410",
            ),
        ],
    ),
    Rev(
        1761762026,
        [
            Change(
                CType.ADD,
                "server",
                "`X-ANIMEAPI-VERSION`, `X-ANIMEAPI-UPDATED`, and `X-ANIMEAPI-SERVER-UPDATED` headers were now required for this library",
            ),
            Change(
                CType.UP,
                "letterboxd",
                "Slug, alphanumeric ID (used for official API), and internal numeric ID now are allowed for lookup",
            ),
            Change(CType.UP, "trakt", "Slug is allowed as lookup keyword on Trakt"),
            Change(
                CType.DEP,
                "animeapi",
                "Platform-dedicated object and list endpoints were deprecated, no further update",
            ),
        ],
    ),
]
