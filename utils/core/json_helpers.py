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
    except json.JSONDecodeError:
        log.error(f"Invalid JSON string: {json_string}. Resetting to empty.")
        return {}