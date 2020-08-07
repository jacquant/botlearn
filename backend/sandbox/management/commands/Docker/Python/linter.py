import argparse  # noqa: DAR000
import io
from contextlib import redirect_stdout

import yaml
from flake8.api import legacy as flake8
from regex import multi_replace_regex


def lint(filename_to_lint, translate_to_french, errors):
    """Run in a sandbox and lint a code.

    :param errors: the errors to parse
    :type errors: list
    :param filename_to_lint: the name of the file to lint
    :type filename_to_lint: str
    :param translate_to_french: boolean value to translate output in french
    :type translate_to_french: bool
    """
    if errors:
        style_guide = flake8.get_style_guide(max_line_length=120, select=errors)
    else:
        style_guide = flake8.get_style_guide(max_line_length=120)
    output_redirection = io.StringIO()
    with redirect_stdout(output_redirection):
        style_guide.input_file(filename_to_lint)
    if translate_to_french:
        errors_warnings_codes = {}
        for file_to_open in ("errors.yaml", "warnings.yaml"):
            with open("rules/{0}".format(file_to_open), "r") as stream:
                try:
                    errors_warnings_codes = {
                        **errors_warnings_codes,
                        **yaml.safe_load(stream),
                    }
                except yaml.YAMLError as exc:
                    print(exc)
        print(
            multi_replace_regex(
                output_redirection.getvalue(), errors_warnings_codes
            ),
        )
    else:
        print(output_redirection.getvalue())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename", type=str, help="the name of the file to lint"
    )
    parser.add_argument(
        "-t",
        "--translate",
        help="translate the ouput in french",
        action="store_true",
    )
    parser.add_argument("-e", "--errors", nargs="+", help="<Required> List of code erreurs")
    args = parser.parse_args()
    lint(args.filename, args.translate, args.errors)
