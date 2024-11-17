import click
from .commands.init import init_assignment
from .commands.submit import submit_file
from .commands.status import status_overview

@click.group()
def cli():
    """Temmies CLI - A command line tool for managing assignments using the Temmies library."""
    pass

@cli.command()
@click.argument('year_course_assignment', required=False)
@click.argument('path', required=False, default='.')
@click.option('-s', '--search', help='Search for an assignment by name.')
def init(year_course_assignment, path, search):
    """Initialize a new assignment."""
    init_assignment(year_course_assignment, path, search)

@cli.command()
@click.argument('files', nargs=-1, required=True)
@click.option('-q', '--quiet', is_flag=True, help="Quiet submission, don't wait for output.")
def submit(files, quiet):
    """Submit file(s) to the relevant assignment."""
    submit_file(files, quiet)

@cli.command()
@click.option('-d', '--detail', is_flag=True, help="Add more detail to the status overview.")
def status(detail):
    """Show the current assignment's status."""
    status_overview(detail)

if __name__ == '__main__':
    cli()
