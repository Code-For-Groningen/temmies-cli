"""
Submit command for temmies-cli.
Submits files to the assignment described in the .temmies metadata file.
"""

from .utils import get_current_assignment


def submit_file(files, quiet):
    """Submit file(s) to the relevant assignment."""
    get_current_assignment().submit(list(files), silent=quiet)
