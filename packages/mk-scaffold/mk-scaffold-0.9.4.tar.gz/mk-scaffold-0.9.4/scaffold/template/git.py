import atexit
import os
import shutil
import subprocess
import sys
import tempfile

from . import directory


def git_clone(url):
    # Create a temporary folder to be deleted at exit
    tmpdir = tempfile.mkdtemp(prefix="scaffold")

    def remove_tmpdir():
        shutil.rmtree(tmpdir)

    atexit.register(remove_tmpdir)

    try:
        git = shutil.which("git")
        subprocess.run([git, "clone", url, "repository"], cwd=tmpdir, check=True)

        template_dir = os.path.join(tmpdir, "repository")
        return directory.exact_match(template_dir)
    except subprocess.CalledProcessError:
        sys.exit(f'error: failed to clone remote repository "{url}"')


def exact_match(path):
    # Clone the repository
    git = shutil.which("git")
    if git is None:
        return False, False

    return git_clone(path)
