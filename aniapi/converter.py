from typing import Any, Dict, List, Union

from dacite import Config, from_dict

from aniapi.models import AnimeRelations, ApiStatus, Heartbeat, TraktMediaType


def convert_arm(data: Dict[str, Union[str, int, None]]) -> AnimeRelations:
    """
    Converts a dict to an AnimeRelations object

    :param data: The dict to convert
    :type data: Dict[str, Union[str, int, None]]
    :return: The converted AnimeRelations object
    :rtype: AnimeRelations
    """
    return from_dict(data_class=AnimeRelations, data=data, config=Config(cast=[TraktMediaType]))


def convert_from_dict(data: Dict[str, Dict[str, Union[str, int, None]]]) -> Dict[str, AnimeRelations]:
    """
    Converts a dict of dicts to a dict of AnimeRelations objects

    :param data: The dict to convert
    :type data: Dict[str, Dict[str, Union[str, int, None]]]
    :return: The converted dict
    :rtype: Dict[str, AnimeRelations]
    """
    return {key: convert_arm(value) for key, value in data.items()}


def convert_from_list(data: List[Dict[str, Union[str, int, None]]]) -> List[AnimeRelations]:
    """
    Converts a list of dicts to a list of AnimeRelations objects

    :param data: The list to convert
    :type data: List[Dict[str, Union[str, int, None]]]
    :return: The converted list
    :rtype: List[AnimeRelations]
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
