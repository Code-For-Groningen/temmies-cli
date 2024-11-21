import os
import click
from temmies.themis import Themis
from temmies.exercise_group import ExerciseGroup
from tqdm import tqdm


def parse_path(themis, path_str):
    """
    Parse the path string into year, course, and target object (assignment or folder).
    Supports formats like <startyear-endyear>/<courseTag>/(<folder_or_assignment>).
    """
    parts = path_str.strip('/').split('/')
    if len(parts) >= 2:
        year_path, course_tag = parts[0], parts[1]
        remaining_parts = parts[2:]

        year = themis.get_year(
            int(year_path.split('-')[0]), int(year_path.split('-')[1]))
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


def download_items(session, base_url, items, destination_path, item_type):
    """
    Download items (e.g., files or test cases) to the specified destination with a progress bar.
    """
    if not items:
        click.echo(f"No {item_type} available for this assignment.")
        return

    os.makedirs(destination_path, exist_ok=True)
    with tqdm(total=len(items), desc=f"Downloading {item_type}", unit="file") as pbar:
        for item in items:
            item_url = f"{base_url}{item['path']}"
            response = session.get(item_url)
            if response.status_code == 200:
                file_path = os.path.join(destination_path, item['title'])
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            pbar.update(1)  # Update the progress bar
    click.echo(f"Downloaded {len(items)} {item_type} to '{destination_path}'.")


def download_test_cases(assignment, path, test_folder):
    """
    Download test cases for the assignment with a progress bar.
    """
    test_cases = assignment.get_test_cases()
    test_cases_path = os.path.join(path, test_folder)
    download_items(assignment.session, assignment.base_url,
                   test_cases, test_cases_path, "test cases")


def download_files(assignment, path, file_folder):
    """
    Download additional files for the assignment with a progress bar.
    """
    files = assignment.get_files()
    path = os.path.join(path, file_folder)
    download_items(assignment.session, assignment.base_url,
                   files, path, "additional files")


def download_assignment_files(assignment, path, test_folder, file_folder):
    """
    Download all necessary files and test cases for the assignment with progress bars.
    """
    os.makedirs(path, exist_ok=True)
    try:
        download_test_cases(assignment, path, test_folder)
        download_files(assignment, path, file_folder)
    except (ValueError, ConnectionError) as e:
        click.echo(str(e))


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


def create_assignment_files(group, root_path, user, test_folder, file_folder):
    """
    Download files and test cases for a group (folder or assignment) recursively.
    """
    os.makedirs(root_path, exist_ok=True)
    download_assignment_files(group, root_path, test_folder, file_folder)

    if group.submitable:
        # It's an assignment
        create_metadata_file(root_path, user, group.path)
    else:
        # It's a folder or course
        items = group.get_items()
        for item in items:
            item_path = os.path.join(
                root_path, item.title.lower().replace(" ", "_"))
            create_assignment_files(item, item_path, user, test_folder, file_folder)
