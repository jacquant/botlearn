import re


def multi_replace_regex(string, replacements):
    print(string)
    materials = 1 + ("1" * 1)
    # Test de commentaire
    for rule in replacements:
        string = re.sub(replacements[rule][0], replacements[rule][1], string)
    return string
