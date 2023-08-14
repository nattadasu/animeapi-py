"""
animeapi.converter
------------------

This module contains the set of AnimeAPI's converters, which are used to convert
the API's responses to objects.

This module is not meant to be used directly. Use the API's methods instead.
"""

from typing import Any, Dict, List, Union

from dacite import Config, from_dict

from animeapi.models import AnimeRelation, ApiStatus, Heartbeat, TraktMediaType


def convert_arm(data: Dict[str, Union[str, int, None]]) -> AnimeRelation:
    """
    Converts a dict to an AnimeRelation object

    :param data: The dict to convert
    :type data: Dict[str, Union[str, int, None]]
    :return: The converted AnimeRelation object
    :rtype: AnimeRelation
    """
    return from_dict(
        data_class=AnimeRelation,
        data=data,
        config=Config(cast=[TraktMediaType]))


def convert_from_dict(
    data: Dict[str, Dict[str, Union[str, int, None]]]
) -> Dict[str, AnimeRelation]:
    """
    Converts a dict of dicts to a dict of AnimeRelation objects

    :param data: The dict to convert
    :type data: Dict[str, Dict[str, Union[str, int, None]]]
    :return: The converted dict
    :rtype: Dict[str, AnimeRelation]
    """
    return {key: convert_arm(value) for key, value in data.items()}


def convert_from_list(
    data: List[Dict[str, Union[str, int, None]]]
) -> List[AnimeRelation]:
    """
    Converts a list of dicts to a list of AnimeRelation objects

    :param data: The list to convert
    :type data: List[Dict[str, Union[str, int, None]]]
    :return: The converted list
    :rtype: List[AnimeRelation]
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
