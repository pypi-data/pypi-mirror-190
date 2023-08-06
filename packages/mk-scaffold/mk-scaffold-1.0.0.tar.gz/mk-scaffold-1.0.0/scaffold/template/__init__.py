import sys

import yaml

from ..constants import TEMPLATE_NAME
from . import directory, git


def get(args):
    """
    Find, fetch the template file and return it's contents
    """
    template_path = args["template"]
    for method in [directory.exact_match, git.exact_match]:
        file, path = method(template_path)
        if file and path:
            args["template_file"] = file
            args["template_dir"] = path
            break
    else:
        sys.exit(f'error: no "{TEMPLATE_NAME}" file found')

    with open(file, encoding="UTF-8") as fd:
        return yaml.safe_load(fd)
