"""
Displays the status of the current assignment, including detailed submission data if requested.
"""

from datetime import datetime
import click
from .utils import get_current_assignment


def status_overview(detail):
    """Show the current assignment's status."""
    try:
        assignment = get_current_assignment()
    except ValueError as e:
        click.echo(str(e), err=True)
        return

    status = assignment.get_status()

    if status:
        click.echo(f"Assignment: {assignment.title}")
        click.echo(f"- Status: {status.get('status', 'Unknown')}")
        if status.get('group'):
            click.echo(f"- Group: {status['group']}")
        if detail:
            click.echo("+ Leading submission:")
            extract_submission_info(status['leading'].get_info())
    else:
        click.echo("No status information available.")


def extract_submission_info(submission_data):
    """
    Extracts and click.echos the most important information from a submission dictionary.
    """
    important_info = {
        "Uploaded By": submission_data.get("uploaded_by"),
        "Created On": normalize_timestamp(submission_data.get("created_on")),
        "Updated On": normalize_timestamp(submission_data.get("updated_on")),
        "Status": (
            submission_data.get("status").split(": ")[1]
            if "status" in submission_data
            else None
        ),
        "Language": submission_data.get("language"),
        "Files": submission_data.get("files", []),
    }

    for key, value in important_info.items():
        if key == "Files":
            click.echo(f"   + {len(value)} files submitted:")
            for file_info in value:
                click.echo(f"       + {file_info[0]}")
            continue
        if value:
            click.echo(f"   + {key}: {value}")


def normalize_timestamp(timestamp: str) -> str:
    """
    Normalizes and formats a timestamp string to a readable format.
    Args:
        timestamp (str): The timestamp string to normalize.
    Returns:
        str: The normalized timestamp in "YYYY-MM-DD HH:MM:SS" format.
    """
    try:
        # Extract the datetime part before "GMT"
        timestamp_part = timestamp.split("GMT")[0].strip()
        # Parse the timestamp
        dt = datetime.strptime(timestamp_part, "%a %b %d %Y %H:%M:%S")
        # Return in "YYYY-MM-DD HH:MM:SS" format
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return f"Invalid timestamp: {timestamp}"
