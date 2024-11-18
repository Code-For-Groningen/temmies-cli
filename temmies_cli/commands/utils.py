import os
import click
from temmies.themis import Themis
from temmies.exercise_group import ExerciseGroup


def parse_path(themis, path_str):
    """
    Parse the path string into year, course, and target object (assignment or folder).
    Supports formats like <startyear-endyear>/<courseTag>/(<folder_or_assignment>).
    """
    parts = path_str.strip('/').split('/')
    if len(parts) >= 2:
        year_path, course_tag = parts[0], parts[1]
        remaining_parts = parts[2:]

        year = themis.get_year(year_path)
        course = year.get_course_by_tag(course_tag)

        if remaining_parts:
            target = course
            for part in remaining_parts:
                target = target.get_item_by_title(part)
            return year, course, target
        else:
            return year, course, course
    else:
        return None


def navigate_to_assignment(group, assignment_name):
    """
    Navigate through groups to find the assignment by name.
    """
    for item in group.get_items():
        if (assignment_name in (item.title, item.path.split("/")[-1])) and item.submitable:
            return item
        elif not item.submitable:
            result = navigate_to_assignment(item, assignment_name)
            if result:
                return result
    return None


def download_assignment_files(assignment, path, test_folder):
    """
    Download files and test cases for an assignment.
    """
    os.makedirs(path, exist_ok=True)

    # Download test cases (if any)
    try:
        test_cases = assignment.get_test_cases()
        if test_cases:
            test_cases_path = os.path.join(path, test_folder)
            os.makedirs(test_cases_path, exist_ok=True)
            for tc in test_cases:
                tc_url = f"{assignment.base_url}{tc['path']}"
                tc_response = assignment.session.get(tc_url)
                if tc_response.status_code == 200:
                    tc_filename = os.path.join(test_cases_path, tc['title'])
                    with open(tc_filename, 'wb') as f:
                        f.write(tc_response.content)
            click.echo(f"Downloaded {len(test_cases)} test cases to '{
                       test_cases_path}'.")
        else:
            click.echo("No test cases available for this assignment.")
    except ValueError as ve:
        click.echo(str(ve))
    except ConnectionError as ce:
        click.echo(str(ce))

    # Download additional files (if any)
    try:
        files = assignment.get_files()
        if files:
            for file_info in files:
                file_url = f"{assignment.base_url}{file_info['path']}"
                file_response = assignment.session.get(file_url)
                if file_response.status_code == 200:
                    file_filename = os.path.join(path, file_info['title'])
                    with open(file_filename, 'wb') as f:
                        f.write(file_response.content)
            click.echo(f"Downloaded {
                       len(files)} additional files to '{path}'.")
    except ValueError as ve:
        click.echo(str(ve))
    except ConnectionError as ce:
        click.echo(str(ce))


def create_metadata_file(root_path, user, assignment_path):
    """
    Create the .temmies metadata file.
    """
    metadata_path = os.path.join(root_path, '.temmies')
    with open(metadata_path, 'w') as f:
        f.write(f"username={user}\n")
        f.write(f"assignment_path={assignment_path}\n")
    os.chmod(metadata_path, 0o600)
    click.echo(f"Created .temmies metadata file in '{root_path}'.")


def load_metadata():
    """
    Load assignment metadata from the .temmies file.
    """
    if not os.path.exists('.temmies'):
        click.echo(
            "No .temmies file found in the current directory. Please run 'temmies init' first.", err=True)
        return None
    # Load assignment metadata
    with open('.temmies', 'r') as f:
        metadata = dict(line.strip().split('=') for line in f if '=' in line)
    username = metadata.get('username')
    assignment_path = metadata.get('assignment_path')

    if not username or not assignment_path:
        click.echo("Missing assignment metadata in .temmies file.", err=True)
        return None
    return metadata


def create_assignment_files(group, root_path, user, test_folder):
    """
    Download files and test cases for a group (folder or assignment) recursively.
    """
    os.makedirs(root_path, exist_ok=True)
    if group.submitable:
        # It's an assignment
        download_assignment_files(group, root_path, test_folder)
        create_metadata_file(root_path, user, group.path)
    else:
        # It's a folder or course
        items = group.get_items()
        for item in items:
            item_path = os.path.join(
                root_path, item.title.lower().replace(" ", "_"))
            create_assignment_files(item, item_path, user, test_folder)
