import re


def multi_replace_regex(string, replacements):
    """Replace a string with all patterns and replacements.

    :param string: the string to update with patterns
    :type string: str
    :param replacements: a dictionary with all patterns to modify
    :type replacements: dict
    :return: the modified string
    :rtype: str
    """
    for _key, rule in replacements.items():
        string = re.sub(rule[0], rule[1], string)
    return string
