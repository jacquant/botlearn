import yaml
import re
from flake8.api import legacy as flake8

with open("errors.yaml", "r") as stream:
    try:
        errors_codes = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
with open("warnings.yaml", "r") as stream:
    try:
        warnings_codes = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
french_errors_codes_keys = errors_codes["french"].keys()
regex_french_errors = ".*|".join(french_errors_codes_keys)
print(regex_french_errors)
french_warnings_codes_keys = warnings_codes["french"].keys()
regex_french_warnings = ".*|".join(french_warnings_codes_keys)
print(regex_french_warnings)
print(errors_codes, warnings_codes)
style_guide = flake8.get_style_guide()
report = style_guide.input_file("to_lint.py")
print(report)
print(report.get_statistics("E"))
