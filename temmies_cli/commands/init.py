import os
import click
from temmies.themis import Themis
from temmies.exercise_group import ExerciseGroup
from .utils import parse_path, create_assignment_files
import tqdm


def init_assignment(year_course_assignment, path, search, test_folder, file_folder):
    """
    Initialize a new assignment or course.
    """
    # Authenticate the user
    user = input("Enter your Themis username: ")
    themis = Themis(user)

    if search:
        click.echo(f"Searching for assignment: {search}")
        assignment = search_assignment(themis, search)
        if not assignment:
            click.echo(f"Assignment '{search}' not found.", err=True)
            return
        is_course = False
    elif year_course_assignment:
        result = parse_path(themis, year_course_assignment)
        if not result:
            click.echo(
                "Invalid format. Use {startyear-endyear}/{courseTag} or {startyear-endyear}/{courseTag}/{assignment}.", err=True)
            return
        year, course, assignment = result
        is_course = assignment is None
    else:
        click.echo(
            "Provide a year/course/assignment or use -s to search.", err=True)
        return

    # Initialize the root path
    if is_course:
        root_path = os.path.join(path, course.title.lower().replace(" ", "_"))
        click.echo(f"Initializing entire course '{course.title}'...")
        create_assignment_files(course, root_path, user, test_folder, file_folder)
    else:
        root_path = os.path.join(
            path, assignment.title.lower().replace(" ", "_"))
        click.echo(f"Initializing assignment '{assignment.title}'...")
        create_assignment_files(assignment, root_path, user, test_folder, file_folder)

    click.echo(f"Initialized at '{root_path}'.")


def search_assignment(themis, search):
    """
    Search for an assignment by name across all years and courses.
    """
    for year in sorted(themis.all_years(), key=lambda x: x.year_path, reverse=True):
        for course in tqdm.tqdm(year.all_courses(), desc=f"Searching courses in {year.year_path}"):
            assignment = recursive_search(course, search)
            if assignment:
                click.echo(f"Found assignment: {assignment.title} in course: {
                           course.title}, year: {year.year_path}")
                return assignment
    return None


def recursive_search(group, search):
    """
    Recursively search for an assignment in a group and its subgroups.
    """
    if group.title.lower() == search.lower() and group.submitable:
        return group
    for item in group.get_items():
        # click.echo(item.title)
        if item.submitable and (search.lower() in item.title.lower()):
            return item
        elif not item.submitable:
            result = recursive_search(item, search)
            if result:
                return result
    return None
