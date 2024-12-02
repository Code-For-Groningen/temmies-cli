import os
import click
from temmies.themis import Themis
from temmies.exercise_group import ExerciseGroup
from .utils import load_metadata


def submit_file(files, quiet):
    """Submit file(s) to the relevant assignment."""
    metadata = load_metadata()
    if not metadata:
        return

    username = metadata.get('username')
    assignment_path = metadata.get('assignment_path')

    themis = Themis(username)
    assignment = ExerciseGroup(
        themis.session,
        assignment_path,
        title='',
        parent=None,
        submitable=True
    )

    # TODO: Test this
    
    submission = assignment.submit(list(files), silent=quiet)