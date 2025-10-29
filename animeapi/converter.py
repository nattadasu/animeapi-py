"""
animeapi.converter
------------------

This module contains the set of AnimeAPI's converters, which are used to convert
the API's responses to objects.

This module is not meant to be used directly. Use the API's methods instead.
"""

from typing import Any, Dict, List, Union

from dacite import Config, from_dict

from animeapi.models import (
    AnimeRelation,
    ApiStatus,
    Heartbeat,
    IdsMoeAnimeRelation,
    TmdbMediaType,
    TraktMediaType,
)


def convert_arm(
    data: Dict[str, Union[str, int, None]],
) -> Union[AnimeRelation, IdsMoeAnimeRelation]:
    """
    Converts a dict to an AnimeRelation or IdsMoeAnimeRelation object

    :param data: The dict to convert
    :type data: Dict[str, Union[str, int, None]]
    :return: The converted AnimeRelation or IdsMoeAnimeRelation object
    :rtype: Union[AnimeRelation, IdsMoeAnimeRelation]
    """
    if "data_hash" in data or "themoviedb_season" in data:
        data_class = IdsMoeAnimeRelation
    else:
        data_class = AnimeRelation
    return from_dict(
        data_class=data_class,
        data=data,
        config=Config(cast=[TraktMediaType, TmdbMediaType]),
    )


def convert_from_dict(
    data: Dict[str, Dict[str, Union[str, int, None]]],
) -> Dict[str, Union[AnimeRelation, IdsMoeAnimeRelation]]:
    """
    Converts a dict of dicts to a dict of AnimeRelation objects

    :param data: The dict to convert
    :type data: Dict[str, Dict[str, Union[str, int, None]]]
    :return: The converted dict
    :rtype: Dict[str, Union[AnimeRelation, IdsMoeAnimeRelation]]
    """
    return {key: convert_arm(value) for key, value in data.items()}


def convert_from_list(
    data: List[Dict[str, Union[str, int, None]]],
) -> List[Union[AnimeRelation, IdsMoeAnimeRelation]]:
    """
    Converts a list of dicts to a list of AnimeRelation objects

    :param data: The list to convert
    :type data: List[Dict[str, Union[str, int, None]]]
    :return: The converted list
    :rtype: List[Union[AnimeRelation, IdsMoeAnimeRelation]]
    """
    return [convert_arm(value) for value in data]


def convert_api_status(data: Dict[str, Union[str, Dict[str, Any]]]) -> ApiStatus:
    """
    Converts a dict to an ApiStatus object

    :param data: The dict to convert
    :type data: Dict[str, Union[str, Dict[str, Any]]]
    :return: The converted ApiStatus object
    :rtype: ApiStatus
    """
    return from_dict(data_class=ApiStatus, data=data)


def convert_heartbeat(data: Dict[str, Union[str, float, int]]) -> Heartbeat:
    """
    Converts a dict to a Heartbeat object

    :param data: The dict to convert
    :type data: Dict[str, Union[str, float, int]]
    :return: The converted Heartbeat object
    :rtype: Heartbeat
    """
    return from_dict(data_class=Heartbeat, data=data)
