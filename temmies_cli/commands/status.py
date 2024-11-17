def status_overview(detail):
    """Show the current assignment's status."""
    # Check for .temmies file
    if not os.path.exists('.temmies'):
        click.echo("No .temmies file found in the current directory. Please run 'temmies init' first.", err=True)
        return

    # Load assignment metadata
    with open('.temmies', 'r') as f:
        metadata = dict(line.strip().split('=') for line in f)
    assignment_id = metadata.get('assignment_id')
    user = metadata.get('username')
    if not assignment_id or not user:
        click.echo("Assignment ID or username not found in .temmies file.", err=True)
        return

    # Authenticate the user using the username from .temmies
    themis = Themis(user)

    # Retrieve the assignment object
    assignment = themis.get_assignment_by_id(assignment_id)
    if not assignment:
        click.echo("Assignment not found. Please ensure you're in the correct directory.", err=True)
        return

    # Fetch and display status
    status = assignment.get_status()
    click.echo(f"Assignment Status for '{assignment.name}':")
    click.echo(f"- Due Date: {assignment.due_date}")
    click.echo(f"- Submissions: {status['submission_count']}")
    click.echo(f"- Last Submission: {status['last_submission']}")
    if detail:
        click.echo("Detailed Status:")
        for detail_item in status['details']:
            click.echo(f"- {detail_item}")
