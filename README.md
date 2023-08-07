<!-- omit in toc -->
# AnimeAPI Python Wrapper

animeapi-python is a Python wrapper for the [AnimeAPI][home] made by [nattadasu][gh-nattadasu].

The wrapper is released with type hints and async support in mind for ease of use
and is compatible with Python 3.6 or higher.

<!-- omit in toc -->
## Table of Contents

* [Installation](#installation)
  * [Requirements](#requirements)
* [Usage](#usage)
  * [Asyncronous Usage](#asyncronous-usage)
* [Documentation](#documentation)
  * [Available Methods](#available-methods)
    * [`get_anime_relations(title_id: str | int, platform: str | Platform, media_type: str | TraktMediaType | TmdbMediaType | None = None, title_season: int | None) -> AnimeRelation`](#get_anime_relationstitle_id-str--int-platform-str--platform-media_type-str--traktmediatype--tmdbmediatype--none--none-title_season-int--none---animerelation)
    * [`get_dict_anime_relations(platform: str | Platform) -> dict[str, AnimeRelation]`](#get_dict_anime_relationsplatform-str--platform---dictstr-animerelation)
    * [`get_list_anime_relations(platform: str | Platform) -> list[AnimeRelation]`](#get_list_anime_relationsplatform-str--platform---listanimerelation)
    * [`get_list_index() -> list[AnimeRelation]`](#get_list_index---listanimerelation)
    * [`get_status() -> ApiStatus`](#get_status---apistatus)
    * [`get_heartbeat() -> Heartbeat`](#get_heartbeat---heartbeat)
    * [`get_updated_time(self, use_datetime: bool = False) -> str | str`](#get_updated_timeself-use_datetime-bool--false---str--str)
* [License](#license)

## Installation

```sh
pip install animeapi
```

Depending on your system, you may need to use `pip3` instead of `pip`, or
`sudo pip` instead of `pip`.

### Requirements

* Python 3.6 or higher
* [requests](https://pypi.org/project/requests/)
* [aiohttp](https://pypi.org/project/aiohttp/) (for async support)
* [dacite](https://pypi.org/project/dacite/)

## Usage

```py
import animeapi

with animeapi.AnimeAPI() as api:
    # Get anime relation data for the anime with ID 1 on MyAnimeList
    mal = api.get_anime_relations(1, animeapi.Platform.MYANIMELIST)
    print(mal)

    # Get list of anime available on AniList
    anilist = api.get_list_anime_relations(animeapi.Platform.ANILIST)
    print(anilist[:2])  # Print first two results

    # Get dictionary of anime available on Kitsu
    kitsu = api.get_dict_anime_relations(animeapi.Platform.KITSU)
    print(kitsu['1'])  # Print data for Cowboy Bebop
```

We recommend using the `with` statement to create an instance of `AnimeAPI`
as we designed the wrapper to be easy to switch between sync and async, although
you can also use `AnimeAPI` directly on `sync` methods only.

### Asyncronous Usage

Similarly, for async, you just need to replace `AnimeAPI` with `AsyncAnimeAPI`
and use `await` on the methods.

```py
import animeapi

async with animeapi.AsyncAnimeAPI() as api:
    # Get anime relation data for the anime with ID 1 on MyAnimeList
    mal = await api.get_anime_relations(1, animeapi.Platform.MYANIMELIST)
    print(mal)

    # Get list of anime available on AniList
    anilist = await api.get_list_anime_relations(animeapi.Platform.ANILIST)
    print(anilist[:2])  # Print first two results

    # Get dictionary of anime available on Kitsu
    kitsu = await api.get_dict_anime_relations(animeapi.Platform.KITSU)
    print(kitsu['1'])  # Print data for Cowboy Bebop
```

## Documentation

<!-- You can find the documentation for the wrapper [here](https://animeapi-py.readthedocs.io/en/latest/). -->

### Available Methods

#### `get_anime_relations(title_id: str | int, platform: str | Platform, media_type: str | TraktMediaType | TmdbMediaType | None = None, title_season: int | None) -> AnimeRelation`

This method equals to the `/:platform/:title_id` endpoint on the API.

```py
# Get anime relation data for the anime with ID 1 on MyAnimeList
mal = api.get_anime_relations(1, animeapi.Platform.MYANIMELIST)
print(mal)
```

#### `get_dict_anime_relations(platform: str | Platform) -> dict[str, AnimeRelation]`

This method equals to the `/:platform` endpoint on the API. Use this method
if you want to get complete data for all anime available on a platform and
wanted to be able to access the data by the anime ID faster.

```py
# Get dictionary of anime available on Kitsu
kitsu = api.get_dict_anime_relations(animeapi.Platform.KITSU)
print(kitsu['1'])  # Print data for Cowboy Bebop
```

#### `get_list_anime_relations(platform: str | Platform) -> list[AnimeRelation]`

This method equals to the `/:platform()` endpoint on the API.

```py
# Get list of anime available on AniList
anilist = api.get_list_anime_relations(animeapi.Platform.ANILIST)
print(anilist[:2])  # Print first two results
```

#### `get_list_index() -> list[AnimeRelation]`

This method equals to the `/animeapi` endpoint on the API.

```py
# Get list of anime available on AnimeAPI
animeapi = api.get_list_index()
print(animeapi[:2])  # Print first two results
```

#### `get_status() -> ApiStatus`

This method equals to the `/status` endpoint on the API.

```py
# Get status of AnimeAPI
status = api.get_status()
print(status)
```

#### `get_heartbeat() -> Heartbeat`

This method equals to the `/heartbeat` endpoint on the API.

```py
# Get heartbeat of AnimeAPI
heartbeat = api.get_heartbeat()
print(heartbeat)
```

#### `get_updated_time(self, use_datetime: bool = False) -> str | str`

This method equals to the `/updated` endpoint on the API.

```py
# Get last updated time of AnimeAPI
updated = api.get_updated_time(True)
print(updated)
```

## License

`animeapi-py` is licensed under the [GNU Affero General Public License v3.0](LICENSE).

[home]: https://animeapi.my.id
[gh-nattadasu]: https://github.com/nattadasu
