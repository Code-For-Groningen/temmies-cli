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
    submission = assignment.submit(list(files))
    if not quiet:
        click.echo("Submission results:")
        status = submission.get_status()
        click.echo(f"- Status: {status}")
        results = submission.get_results()
        if results:
            for case, result in results.items():
                status_text = "Passed" if result.get('passed') else "Failed"
                click.echo(f"Test Case {case}: {status_text}")
