import json

import utils.logger.logger as log

def json_to_dict(json_string):
    """
    :Purpose: parse a json string and converts it into a dictionary
    :param: preferences_json: json string to parse
    :Return: dictionary of input json string
    :Author(s): Joe Lee
    """
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        log.error(f"Invalid JSON string: {json_string}. Resetting to empty.")
        return {}

def dict_to_json(dict):
    """
    :Purpose: converts a dictionary into a json string
    :param: dictionary: dictionary to convert
    :Return: json string of input dictionary
    :Author(s): Joe Lee
    """
    try:
        return json.dumps(dict)
    except (TypeError, ValueError):
        log.error(f"Invalid dictionary: {dict}. Resetting to empty.")
        return {}