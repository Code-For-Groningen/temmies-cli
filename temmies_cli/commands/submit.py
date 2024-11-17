def submit_file(files, quiet):
    """Submit file(s) to the relevant assignment."""
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

    # Submit each file
    for file in files:
        if not os.path.exists(file):
            click.echo(f"File '{file}' does not exist.", err=True)
            continue
        with open(file, 'rb') as f:
            content = f.read()
        click.echo(f"Submitting file: {file}")
        result = assignment.submit_file(file_name=file, content=content)
        if not quiet:
            click.echo(f"Submission result for {file}: {result}")
    click.echo("Submission complete.")
