import os
import click
from temmies.themis import Themis
from temmies.exceptions.illegal_action import IllegalAction

def init_assignment(year_course_assignment, path, search):
    """Initialize a new assignment."""
    # Authenticate the user
    user = input("Enter your Themis username: ")
    themis = Themis(user)

    if search:
        click.echo(f"Searching for assignment: {search}")
        # Use the temmies library to search for assignments
        assignment = search_assignment(themis, search)
        if not assignment:
            click.echo(f"Assignment '{search}' not found.", err=True)
            return
    elif year_course_assignment:
        try:
            year_str, course_name, assignment_name = year_course_assignment.split('/')
            start_year, end_year = map(int, year_str.split('-'))
            year = themis.get_year(start_year, end_year)
            course = get_course_by_name(year, course_name)
            assignment = get_assignment_by_name(course, assignment_name)
        except ValueError:
            click.echo("Invalid format. Please use {year}/{course}/{assignment}.", err=True)
            return
    else:
        click.echo("Either provide a year/course/assignment or use the -s option to search.", err=True)
        return

    # Download assignment files and set up directory
    assignment_path = os.path.join(path, assignment_name)
    os.makedirs(assignment_path, exist_ok=True)
    create_assignment_files(assignment, assignment_path, user)
    click.echo(f"Initialized assignment '{assignment_name}' in '{assignment_path}'.")

def search_assignment(themis, search_term):
    """Search for an assignment by name."""
    years = themis.all_years()
    for year in years:
        for course in year.get_courses():
            for assignment in course.get_assignments():
                if search_term.lower() in assignment.name.lower():
                    return assignment
    return None

def get_course_by_name(year, course_name):
    """Get a course by name from a year."""
    for course in year.get_courses():
        if course_name.lower() == course.name.lower():
            return course
    raise IllegalAction(f"Course '{course_name}' not found in year {year.start}-{year.end}.")

def get_assignment_by_name(course, assignment_name):
    """Get an assignment by name from a course."""
    for assignment in course.get_assignments():
        if assignment_name.lower() == assignment.name.lower():
            return assignment
    raise IllegalAction(f"Assignment '{assignment_name}' not found in course '{course.name}'.")

def create_assignment_files(assignment, assignment_path, user):
    """Download assignment files and save them to the specified path."""
    # Assuming the assignment object has a method to get files
    files = assignment.get_files()
    for file in files:
        file_content = file.download()
        file_path = os.path.join(assignment_path, file.name)
        with open(file_path, 'wb') as f:
            f.write(file_content)
        click.echo(f"Downloaded {file.name} to {file_path}")
    # Save assignment metadata
    metadata_path = os.path.join(assignment_path, '.temmies')
    with open(metadata_path, 'w') as f:
        f.write(f"username={user}\n")
        f.write(f"assignment_id={assignment.id}\n")
    click.echo(f"Created .temmies metadata file in {assignment_path}.")
