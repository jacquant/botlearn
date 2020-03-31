import argparse
import io
from contextlib import redirect_stdout

import yaml
from flake8.api import legacy as flake8
from utils import multi_replace_regex


def lint(filename_to_lint, translate_to_french):
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

    errors_warnings_codes = {**errors_codes, **warnings_codes}
    style_guide = flake8.get_style_guide(max_line_length=120)
    f = io.StringIO()
    with redirect_stdout(f):
        style_guide.input_file(filename_to_lint)
    if translate_to_french:
        print(multi_replace_regex(f.getvalue(), errors_warnings_codes))
    else:
        print(f.getvalue())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="the name of the file to lint")
    parser.add_argument("-t", "--translate", help="translate the ouput in french", action="store_true")
    args = parser.parse_args()
    lint(args.filename, args.translate)
